# src/analysis/transcriber.py
import whisper
import logging
import os

def get_word_timestamps(audio_path: str) -> list | None:
    """Sử dụng Whisper để phiên âm và trả về danh sách word timestamps."""
    model_name = os.getenv("WHISPER_MODEL", "base")
    logging.info(f"Đang tải model Whisper: {model_name}...")
    try:
        model = whisper.load_model(model_name)
        logging.info(f"Bắt đầu phiên âm file: {audio_path}")
        
        result = model.transcribe(audio_path, word_timestamps=True)
        
        all_words = []
        for segment in result['segments']:
            all_words.extend(segment['words'])

        logging.info(f"Phiên âm thành công, tìm thấy {len(all_words)} từ.")
        return all_words
    except Exception as e:
        logging.error(f"Lỗi trong quá trình phiên âm Whisper: {e}")
        return None