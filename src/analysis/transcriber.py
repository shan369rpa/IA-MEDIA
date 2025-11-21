# src/analysis/transcriber.py

import whisper
import logging
import os
import torch
from dotenv import load_dotenv

# Biến toàn cục để cache model, tránh tải lại nhiều lần trong cùng một phiên chạy
_whisper_model = None

def get_word_timestamps(audio_path: str) -> list | None:
    """
    Sử dụng Whisper để phiên âm một file audio và trả về một danh sách (list)
    chi tiết của từng từ cùng với timestamp của nó.

    Args:
        audio_path (str): Đường dẫn đến file audio .wav (yêu cầu 16kHz).

    Returns:
        list | None: Một danh sách các dictionary, mỗi dictionary chứa thông tin
                     về một từ. Trả về None nếu có lỗi nghiêm trọng.
    """
    global _whisper_model
    load_dotenv()

    if not os.path.exists(audio_path):
        logging.error(f"File audio không tồn tại, không thể phiên âm: {audio_path}")
        return None

    try:
        # Tải model (chỉ trong lần gọi đầu tiên)
        if _whisper_model is None:
            model_name = os.getenv("WHISPER_MODEL", "base")
            logging.info(f"Đang tải model Whisper: '{model_name}'...")
            logging.info("Quá trình này có thể mất vài phút cho lần chạy đầu tiên...")
            
            # Xác định thiết bị (GPU nếu có)
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logging.info(f"Whisper sẽ chạy trên thiết bị: {device.upper()}")
            
            _whisper_model = whisper.load_model(model_name, device=device)
            logging.info("Tải model Whisper thành công.")
        
        # Thực hiện phiên âm
        logging.info(f"Bắt đầu phiên âm file: {os.path.basename(audio_path)}...")
        
        # Các tùy chọn để có kết quả tốt hơn
        # fp16=False nếu chạy trên CPU để tránh lỗi
        options = whisper.DecodingOptions(fp16=torch.cuda.is_available())

        result = whisper.decode(_whisper_model, whisper.load_audio(audio_path), options)

        # Trích xuất word timestamps từ kết quả
        # Cách lấy word timestamps có thể thay đổi tùy phiên bản whisper,
        # cách này thường ổn định hơn.
        # Lưu ý: Phiên bản mới của Whisper có thể trả về timestamps trực tiếp từ transcribe
        # result = _whisper_model.transcribe(audio_path, word_timestamps=True)
        # all_words = []
        # for segment in result.get('segments', []):
        #     all_words.extend(segment.get('words', []))

        # Tạm thời, để có được word_timestamps, chúng ta cần chạy lại alignment
        # Đây là một bước hơi thừa nhưng đảm bảo có word timestamps
        audio = whisper.load_audio(audio_path)
        aligned_result = whisper.align( _whisper_model, audio, result)
        word_segments = aligned_result["word_segments"]

        logging.info(f"Phiên âm thành công, tìm thấy {len(word_segments)} từ.")
        
        # Chuyển đổi định dạng cho nhất quán (nếu cần)
        # Định dạng trả về của align là list of dicts với 'word', 'start', 'end'
        return word_segments

    except Exception as e:
        logging.exception(f"Lỗi không xác định trong quá trình phiên âm Whisper.")
        return None