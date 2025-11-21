# src/analysis/chunker.py

from pydub import AudioSegment
import os
import logging
import pandas as pd # Sử dụng pandas để làm việc với file CSV dễ dàng hơn

# Import các hàm tiện ích từ các module khác
from src.utils import fcpxml_parser, file_handler

def create_and_save_chunks(
    clean_audio_path: str,
    error_audio_path: str,
    clean_video_path: str,
    error_video_path: str,
    time_map: list,
    word_timestamps: list,
    output_dir: str,
    source_video_name: str
) -> int:
    """
    Duyệt qua danh sách word_timestamps, chuyển đổi thời gian sang file raw,
    sau đó cắt và lưu các cặp audio/video chunk (clean/error).
    Đồng thời tạo một file metadata.csv.

    Returns:
        int: Số lượng cặp chunk (từ) đã được xử lý và tạo ra.
    """
    logging.info(f"Bắt đầu quá trình cắt và lưu chunks cho video: {source_video_name}")
    
    try:
        clean_audio = AudioSegment.from_wav(clean_audio_path)
        error_audio = AudioSegment.from_wav(error_audio_path)
        logging.info("Đã tải thành công 2 file audio 'clean' và 'error' vào bộ nhớ.")
    except Exception as e:
        logging.error(f"Không thể tải file audio bằng pydub: {e}")
        return 0

    metadata_records = []
    processed_word_count = 0
    
    # Tạo các thư mục con cần thiết
    clean_audio_dir = os.path.join(output_dir, "clean", "audio", source_video_name)
    error_audio_dir = os.path.join(output_dir, "error", "audio", source_video_name)
    clean_video_dir = os.path.join(output_dir, "clean", "video", source_video_name)
    error_video_dir = os.path.join(output_dir, "error", "video", source_video_name)
    
    for d in [clean_audio_dir, error_audio_dir, clean_video_dir, error_video_dir]:
        os.makedirs(d, exist_ok=True)

    for word_info in word_timestamps:
        word_text = word_info['word'].strip()
        start_time_edited_sec = word_info['start']
        end_time_edited_sec = word_info['end']

        # Bỏ qua các từ quá ngắn hoặc không có nội dung
        if (end_time_edited_sec - start_time_edited_sec < 0.150) or not word_text:
            continue

        # Chuyển đổi thời gian sang hệ quy chiếu của file raw
        start_time_raw_sec = fcpxml_parser.convert_edited_to_raw_time(start_time_edited_sec, time_map)
        
        # Chỉ xử lý nếu từ này nằm trong một clip được ánh xạ trong FCPXML
        if start_time_raw_sec is not None:
            duration_sec = end_time_edited_sec - start_time_edited_sec
            
            # --- TÍNH TOÁN TÊN FILE VÀ ĐƯỜDẪN ---
            sanitized_word = file_handler.sanitize_filename(word_text)
            start_ms_edited = int(start_time_edited_sec * 1000)
            end_ms_edited = int(end_time_edited_sec * 1000)
            base_chunk_filename = f"{start_ms_edited}_{end_ms_edited}_{sanitized_word}"

            # Đường dẫn file vật lý
            clean_audio_chunk_path = os.path.join(clean_audio_dir, f"{base_chunk_filename}.wav")
            clean_video_chunk_path = os.path.join(clean_video_dir, f"{base_chunk_filename}.mp4")
            error_audio_chunk_path = os.path.join(error_audio_dir, f"{base_chunk_filename}.wav")
            error_video_chunk_path = os.path.join(error_video_dir, f"{base_chunk_filename}.mp4")

            # --- CẮT AUDIO ---
            clean_chunk = clean_audio[start_ms_edited:end_ms_edited]
            clean_chunk.export(clean_audio_chunk_path, format="wav")

            start_ms_raw = int(start_time_raw_sec * 1000)
            end_ms_raw = int((start_time_raw_sec + duration_sec) * 1000)
            error_chunk = error_audio[start_ms_raw:end_ms_raw]
            error_chunk.export(error_audio_chunk_path, format="wav")
            
            # --- CẮT VIDEO ---
            file_handler.cut_video_segment(
                input_video_path=clean_video_path,
                output_video_path=clean_video_chunk_path,
                start_time=start_time_edited_sec,
                duration=duration_sec
            )
            file_handler.cut_video_segment(
                input_video_path=error_video_path,
                output_video_path=error_video_chunk_path,
                start_time=start_time_raw_sec,
                duration=duration_sec
            )

            # --- THÊM METADATA VÀO DANH SÁCH ---
            # Lưu đường dẫn tương đối để dễ dàng di chuyển bộ dữ liệu
            relative_clean_audio_path = os.path.relpath(clean_audio_chunk_path, output_dir)
            relative_error_audio_path = os.path.relpath(error_audio_chunk_path, output_dir)
            relative_clean_video_path = os.path.relpath(clean_video_chunk_path, output_dir)
            relative_error_video_path = os.path.relpath(error_video_chunk_path, output_dir)

            # TODO: Tích hợp logic gán nhãn lỗi chi tiết ở đây
            # Tạm thời gán nhãn mặc định
            
            metadata_records.append({
                "source_video": source_video_name,
                "word_text": word_text,
                "start_ms_edited": start_ms_edited,
                "end_ms_edited": end_ms_edited,
                "duration_ms": int(duration_sec * 1000),
                "label": "clean",
                "audio_path": relative_clean_audio_path,
                "video_path": relative_clean_video_path
            })
            metadata_records.append({
                "source_video": source_video_name,
                "word_text": word_text,
                "start_ms_edited": start_ms_edited, # Giữ timestamp của edited để dễ đối chiếu
                "end_ms_edited": end_ms_edited,
                "duration_ms": int(duration_sec * 1000),
                "label": "error", # Tạm thời
                "audio_path": relative_error_audio_path,
                "video_path": relative_error_video_path
            })
            
            processed_word_count += 1
    
    # --- GHI FILE METADATA.CSV ---
    if metadata_records:
        metadata_path = os.path.join(output_dir, "metadata.csv")
        df = pd.DataFrame(metadata_records)
        
        # Ghi file, ghi đè nếu file đã tồn tại hoặc nối thêm nếu muốn xử lý nhiều video
        # Ở đây chúng ta sẽ ghi đè cho mỗi lần chạy pipeline video
        # Cần một cơ chế tổng hợp metadata ở cấp cao hơn (trong main.py)
        df.to_csv(metadata_path, index=False, mode='a', header=not os.path.exists(metadata_path))
        logging.info(f"Đã ghi/nối {len(metadata_records)} bản ghi vào {metadata_path}")

    logging.info(f"Hoàn tất, đã xử lý và tạo ra {processed_word_count} cặp chunk.")
    return processed_word_count