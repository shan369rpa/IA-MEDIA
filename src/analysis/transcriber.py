# src/analysis/transcriber.py
import whisper
import logging
import os
import torch
from dotenv import load_dotenv

_whisper_model = None

def get_word_timestamps(audio_path: str) -> list | None:
    global _whisper_model
    load_dotenv()

    if not os.path.exists(audio_path):
        logging.error(f"File audio không tồn tại, không thể phiên âm: {audio_path}")
        return None
    try:
        if _whisper_model is None:
            model_name = os.getenv("WHISPER_MODEL", "base")
            logging.info(f"Đang tải model Whisper: '{model_name}'...")
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logging.info(f"Whisper sẽ chạy trên thiết bị: {device.upper()}")
            _whisper_model = whisper.load_model(model_name, device=device)
            logging.info("Tải model Whisper thành công.")
        
        logging.info(f"Bắt đầu phiên âm file: {os.path.basename(audio_path)}...")
        
        # SỬ DỤNG PHƯƠNG PHÁP CHÍNH THỨC VÀ ĐÁNG TIN CẬY
        result = _whisper_model.transcribe(audio_path, word_timestamps=True)
        
        all_words = []
        # Trích xuất danh sách các từ từ kết quả
        for segment in result.get('segments', []):
            all_words.extend(segment.get('words', []))
        
        if not all_words:
             logging.warning("Whisper không tìm thấy từ nào trong file audio.")
             return []

        logging.info(f"Phiên âm thành công, tìm thấy {len(all_words)} từ.")
        return all_words

    except Exception as e:
        logging.exception(f"Lỗi không xác định trong quá trình phiên âm Whisper.")
        return None