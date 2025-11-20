# src/analysis/chunker.py

from pydub import AudioSegment
import os
import logging
from src.utils import fcpxml_parser # Import hàm chuyển đổi thời gian
from src.utils.file_handler import sanitize_filename # Import hàm làm sạch tên file

def create_and_save_chunks(
    clean_audio_path: str,
    error_audio_path: str,
    time_map: list,
    word_timestamps: list,
    output_dir: str
) -> int:
    """
    Duyệt qua danh sách word_timestamps, chuyển đổi thời gian sang file raw,
    sau đó cắt và lưu các cặp audio chunk (clean/error).

    Args:
        clean_audio_path (str): Đường dẫn đến file audio đã chỉnh sửa (sạch).
        error_audio_path (str): Đường dẫn đến file audio thô (lỗi).
        time_map (list): Bản đồ thời gian được phân tích từ FCPXML.
        word_timestamps (list): Danh sách các đối tượng từ từ Whisper.
        output_dir (str): Thư mục để lưu các chunk được tạo ra.

    Returns:
        int: Số lượng cặp chunk đã được tạo thành công.
    """
    logging.info("Bắt đầu quá trình cắt và lưu audio chunks...")
    
    try:
        clean_audio = AudioSegment.from_wav(clean_audio_path)
        error_audio = AudioSegment.from_wav(error_audio_path)
        logging.info("Đã tải thành công 2 file audio 'clean' và 'error'.")
    except Exception as e:
        logging.error(f"Không thể tải file audio bằng pydub: {e}")
        return 0

    chunk_count = 0
    os.makedirs(output_dir, exist_ok=True)

    for word_info in word_timestamps:
        word_text = word_info['word'].strip()
        start_time_edited_sec = word_info['start']
        end_time_edited_sec = word_info['end']

        # Bỏ qua các từ quá ngắn hoặc không có nội dung
        if (end_time_edited_sec - start_time_edited_sec < 0.150) or not word_text:
            continue

        # Chuyển đổi thời gian sang hệ quy chiếu của file raw
        start_time_raw_sec = fcpxml_parser.convert_edited_to_raw_time(start_time_edited_sec, time_map)
        
        # Chỉ xử lý nếu từ này nằm trong một clip được ánh xạ
        if start_time_raw_sec is not None:
            duration_sec = end_time_edited_sec - start_time_edited_sec
            end_time_raw_sec = start_time_raw_sec + duration_sec

            # Chuyển đổi sang mili giây cho pydub
            start_ms_edited = int(start_time_edited_sec * 1000)
            end_ms_edited = int(end_time_edited_sec * 1000)
            start_ms_raw = int(start_time_raw_sec * 1000)
            end_ms_raw = int(end_time_raw_sec * 1000)

            # Cắt chunk
            clean_chunk = clean_audio[start_ms_edited:end_ms_edited]
            error_chunk = error_audio[start_ms_raw:end_ms_raw]

            # Chuẩn bị đường dẫn lưu file
            sanitized_word = sanitize_filename(word_text)
            if not sanitized_word:
                continue
            
            word_dir = os.path.join(output_dir, sanitized_word)
            os.makedirs(word_dir, exist_ok=True)
            
            chunk_filename = f"{start_ms_edited}_{end_ms_edited}.wav"
            
            # Lưu các file chunk
            clean_chunk.export(os.path.join(word_dir, "clean_" + chunk_filename), format="wav")
            error_chunk.export(os.path.join(word_dir, "error_" + chunk_filename), format="wav")
            
            chunk_count += 1
    
    logging.info(f"Hoàn tất, đã xử lý và lưu được {chunk_count} cặp chunk.")
    return chunk_count