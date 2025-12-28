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

# Các hàm cũ có thể xóa hoặc giữ lại để tham khảo