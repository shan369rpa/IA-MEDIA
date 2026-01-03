# src/analysis/chunker.py

import os
import logging
from pydub import AudioSegment
from src.utils import file_handler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s', force=True)

def chunk_event(
    event: dict,
    clean_audio: AudioSegment,
    error_audio: AudioSegment,
    time_map: list,
    output_dir: str,
    source_video_name: str
) -> tuple[str | None, str | None]:
    """
    Cắt một cặp audio chunk dựa trên thông tin của một 'Edit Event'.
    Returns:
        Tuple chứa (đường dẫn clean chunk, đường dẫn error chunk).
    """
    try:
        start_ms = int(event['start'] * 1000)
        end_ms = int(event['end'] * 1000)
        event_type = event['type']
        
        # Tạo đường dẫn file
        base_filename = f"{start_ms}_{end_ms}_{event_type}.wav"
        clean_path = os.path.join(output_dir, "clean", source_video_name, base_filename)
        error_path = os.path.join(output_dir, "error", source_video_name, base_filename)
        os.makedirs(os.path.dirname(clean_path), exist_ok=True)
        os.makedirs(os.path.dirname(error_path), exist_ok=True)
        
        # Cắt chunk clean
        clean_chunk = clean_audio[start_ms:end_ms]
        clean_chunk.export(clean_path, format="wav")
        
        # Tìm và cắt chunk error tương ứng
        from src.utils import fcpxml_parser # Import local để tránh circular dependency
        raw_start_sec = fcpxml_parser.convert_edited_to_raw_time(event['start'], time_map)
        if raw_start_sec is not None:
            duration_sec = event['end'] - event['start']
            raw_start_ms = int(raw_start_sec * 1000)
            raw_end_ms = int((raw_start_sec + duration_sec) * 1000)
            
            error_chunk = error_audio[raw_start_ms:raw_end_ms]
            error_chunk.export(error_path, format="wav")
            
            return clean_path, error_path
        
        return clean_path, None

    except Exception as e:
        logging.error(f"Lỗi khi chunking event {event['type']}: {e}")
        return None, None

# Thêm vào src/analysis/chunker.py

def chunk_word_from_event(
    word_timestamp: dict,
    event_audio_clean: AudioSegment,
    event_audio_error: AudioSegment,
    workspace_dir: str,
    word_id_str: str # Một chuỗi định danh duy nhất cho từ
) -> tuple[str | None, str | None]:
    """
    Cắt một cặp audio chunk VI MÔ (từ) từ các chunk SỰ KIỆN lớn hơn.
    Lưu chúng vào một thư mục tạm để vector hóa.
    """
    try:
        temp_dir = os.path.join(workspace_dir, "temp_word_chunks")
        os.makedirs(temp_dir, exist_ok=True)
        
        start_ms = int(word_timestamp['start'] * 1000)
        end_ms = int(word_timestamp['end'] * 1000)

        # Cắt từ audio của sự kiện
        word_chunk_clean = event_audio_clean[start_ms:end_ms]
        word_chunk_error = event_audio_error[start_ms:end_ms]

        # Lưu ra file tạm
        clean_path = os.path.join(temp_dir, f"clean_{word_id_str}.wav")
        error_path = os.path.join(temp_dir, f"error_{word_id_str}.wav")
        
        word_chunk_clean.export(clean_path, format="wav")
        word_chunk_error.export(error_path, format="wav")
        
        return clean_path, error_path
    except Exception as e:
        logging.warning(f"Không thể chunk từ '{word_timestamp.get('word', '')}': {e}")
        return None, None