# src/analysis/chunker.py

from pydub import AudioSegment
import os
import logging
import pandas as pd
from src.utils import fcpxml_parser, file_handler
# [MỚI] Import module phân tích
from src.analysis import signal_analyzer 

def create_and_save_chunks(
    clean_audio_path: str,
    error_audio_path: str,
    clean_video_path: str, # Giữ tham số để tương thích, không dùng
    error_video_path: str, # Giữ tham số để tương thích, không dùng
    time_map: list,
    word_timestamps: list,
    output_dir: str,
    source_video_name: str
) -> int:
    """
    Cắt audio chunks và tự động gán nhãn lỗi kỹ thuật.
    """
    logging.info(f"Bắt đầu quá trình cắt và phân tích chunks cho: {source_video_name}")
    
    try:
        clean_audio = AudioSegment.from_wav(clean_audio_path)
        error_audio = AudioSegment.from_wav(error_audio_path)
    except Exception as e:
        logging.error(f"Không thể tải file audio: {e}")
        return 0

    metadata_records = []
    processed_word_count = 0
    
    # Tạo thư mục
    clean_audio_dir = os.path.join(output_dir, "clean", "audio", source_video_name)
    error_audio_dir = os.path.join(output_dir, "error", "audio", source_video_name)
    
    os.makedirs(clean_audio_dir, exist_ok=True)
    os.makedirs(error_audio_dir, exist_ok=True)

    for word_info in word_timestamps:
        word_text = word_info['word'].strip()
        start_time_edited_sec = word_info['start']
        end_time_edited_sec = word_info['end']

        # Bỏ 0.150s vì quá ngắn để phân tích
        if (end_time_edited_sec - start_time_edited_sec < 0.150) or not word_text:
            continue

        start_time_raw_sec = fcpxml_parser.convert_edited_to_raw_time(start_time_edited_sec, time_map)
        
        if start_time_raw_sec is not None:
            duration_sec = end_time_edited_sec - start_time_edited_sec
            
            sanitized_word = file_handler.sanitize_filename(word_text)
            start_ms_edited = int(start_time_edited_sec * 1000)
            end_ms_edited = int(end_time_edited_sec * 1000)
            base_chunk_filename = f"{start_ms_edited}_{end_ms_edited}_{sanitized_word}"

            # 1. Đường dẫn file
            clean_chunk_path = os.path.join(clean_audio_dir, f"{base_chunk_filename}.wav")
            error_chunk_path = os.path.join(error_audio_dir, f"{base_chunk_filename}.wav")

            # 2. Cắt và Lưu Audio
            clean_seg = clean_audio[start_ms_edited:end_ms_edited]
            clean_seg.export(clean_chunk_path, format="wav")

            start_ms_raw = int(start_time_raw_sec * 1000)
            end_ms_raw = int((start_time_raw_sec + duration_sec) * 1000)
            error_seg = error_audio[start_ms_raw:end_ms_raw]
            error_seg.export(error_chunk_path, format="wav")
            
            # 3. [MỚI] Phân tích Tín hiệu để Gán nhãn
            analysis_result = signal_analyzer.analyze_audio_defects(clean_chunk_path, error_chunk_path)
            detected_label = analysis_result["label"] # Ví dụ: 'error_clipping', 'error_pronunciation'
            analysis_details = analysis_result["details"]

            # 4. Lưu Metadata
            rel_clean_path = os.path.relpath(clean_chunk_path, output_dir)
            rel_error_path = os.path.relpath(error_chunk_path, output_dir)

            # Record cho Clean
            metadata_records.append({
                "source_video": source_video_name,
                "word_text": word_text,
                "start_ms": start_ms_edited,
                "end_ms": end_ms_edited,
                "label": "clean",
                "audio_path": rel_clean_path,
                "details": "" # Clean thì không cần details lỗi
            })
            
            # Record cho Error (với nhãn chi tiết)
            metadata_records.append({
                "source_video": source_video_name,
                "word_text": word_text,
                "start_ms": start_ms_edited, # Dùng time edited để mapping
                "end_ms": end_ms_edited,
                "label": detected_label, # <--- NHÃN CHI TIẾT Ở ĐÂY
                "audio_path": rel_error_path,
                "details": str(analysis_details) # Lưu các chỉ số RMS/MaxAmp để tham khảo
            })
            
            processed_word_count += 1
    
    if metadata_records:
        metadata_path = os.path.join(output_dir, "metadata.csv")
        # Thêm cột mới 'details' vào DataFrame
        df = pd.DataFrame(metadata_records)
        df.to_csv(metadata_path, index=False, mode='a', header=not os.path.exists(metadata_path))

    logging.info(f"Hoàn tất {source_video_name}: {processed_word_count} chunks.")
    return processed_word_count
# src/analysis/signal_analyzer.py

from pydub import AudioSegment
import logging

# Cấu hình ngưỡng (Thresholds)
CLIPPING_THRESHOLD_DB = -0.1      # Gần mức 0dB là vỡ tiếng
NOISE_DIFF_THRESHOLD_DB = 3.0     # Nếu đoạn lỗi to hơn đoạn sạch > 3dB -> Khả năng là tiếng ồn/gai âm
LOW_VOLUME_DIFF_THRESHOLD_DB = 5.0 # Nếu đoạn lỗi nhỏ hơn đoạn sạch > 5dB -> Khả năng là bị nhỏ tiếng/mất tiếng

def analyze_segment(clean_chunk: AudioSegment, error_chunk: AudioSegment) -> str:
    """
    Phân tích tín hiệu của error_chunk so với clean_chunk để xác định loại lỗi cụ thể.
    
    Priority (Thứ tự ưu tiên phát hiện):
    1. Clipping (Vỡ tiếng nghiêm trọng)
    2. Noise Spike (Tiếng ồn lớn đột ngột)
    3. Low Volume (Âm lượng quá nhỏ)
    4. Pronunciation (Mặc định - nếu tín hiệu kỹ thuật ổn nhưng vẫn bị đánh dấu là khác biệt)
    
    Returns:
        str: Nhãn lỗi ('error_clipping', 'error_noise_spike', 'error_low_volume', 'error_pronunciation')
    """
    
    # 1. Kiểm tra Clipping (Vỡ tiếng)
    # Pydub trả về max_dBFS (Decibels relative to Full Scale)
    if error_chunk.max_dBFS >= CLIPPING_THRESHOLD_DB:
        return "error_clipping"

    # Lấy độ lớn âm thanh trung bình (dBFS)
    clean_db = clean_chunk.dBFS
    error_db = error_chunk.dBFS

    # Tính chênh lệch năng lượng
    diff = error_db - clean_db

    # 2. Kiểm tra Noise Spike (Lỗi ồn, gai âm)
    # Nếu đoạn lỗi to hơn đoạn sạch đáng kể, thường là do tiếng ho, va đập, hoặc tiếng ồn nền tăng vọt
    if diff > NOISE_DIFF_THRESHOLD_DB:
        return "error_noise_spike"

    # 3. Kiểm tra Low Volume (Âm lượng nhỏ)
    # Nếu đoạn lỗi nhỏ hơn đoạn sạch đáng kể (clean > error)
    # Lưu ý: diff sẽ là số âm, nên ta so sánh clean - error
    if (clean_db - error_db) > LOW_VOLUME_DIFF_THRESHOLD_DB:
        return "error_low_volume"

    # 4. Nếu không dính các lỗi kỹ thuật tín hiệu trên
    # Thì sự khác biệt (do align map chỉ ra) khả năng cao nằm ở chất lượng giọng nói/phát âm
    return "error_pronunciation"