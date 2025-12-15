# src/analysis/transcriber.py

import whisperx
import torch
import gc
from dotenv import load_dotenv
import os
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_word_timestamps(audio_path: str) -> list | None:
    """
    Sử dụng WhisperX để phiên âm và thực hiện Forced Alignment
    để lấy timestamp chính xác tuyệt đối cho từng từ.
    
    Args:
        audio_path (str): Đường dẫn file audio .wav (16kHz).
        
    Returns:
        list: Danh sách các từ với timestamp chính xác.
    """
    load_dotenv()
    
    if not os.path.exists(audio_path):
        logging.error(f"File audio không tồn tại: {audio_path}")
        return None

    # --- CẤU HÌNH ---
    # Dùng model lớn nhất vì bạn có GPU 4070 Ti (12GB VRAM đủ sức chạy large-v2)
    # large-v2 thường ổn định hơn large-v3 cho alignment ở thời điểm hiện tại
    model_size = os.getenv("WHISPER_MODEL", "large-v2") 
    device = "cuda" if torch.cuda.is_available() else "cpu"
    batch_size = 16 # Tăng tốc độ xử lý trên GPU
    compute_type = "float16" # Tối ưu cho GPU RTX 40 series

    logging.info(f"Đang chạy WhisperX trên thiết bị: {device.upper()}")

    try:
        # --- BƯỚC 1: TRANSCRIBE (Lấy văn bản) ---
        logging.info(f"1. Loading Whisper model ({model_size})...")
        model = whisperx.load_model(model_size, device, compute_type=compute_type)
        
        logging.info(f"   Bắt đầu phiên âm file: {os.path.basename(audio_path)}...")
        audio = whisperx.load_audio(audio_path)
        
        # initial_prompt giúp định hướng ngữ cảnh Phật giáo
        # prompt = "Pháp thoại của Thiền sư Thích Nhất Hạnh. Các từ khóa: chánh niệm, tưới tẩm, hạt giống, hạnh phúc, khổ đau, tăng thân, làng mai."
        
        result = model.transcribe(audio, batch_size=batch_size, language="vi"
        # , initial_prompt=prompt
        )
        logging.info(f"   Phiên âm thô hoàn tất. Đang giải phóng VRAM...")

        # Dọn dẹp model transcribe để lấy chỗ cho model align
        del model
        gc.collect()
        torch.cuda.empty_cache()

        # --- BƯỚC 2: FORCED ALIGNMENT (Căn chỉnh thời gian) ---
        logging.info("2. Loading Alignment model...")
        
        # WhisperX tự động chọn model alignment tốt nhất cho ngôn ngữ (thường là wav2vec2)
        # "facebook/wav2vec2-base" là một lựa chọn an toàn khác nếu model VinAI lỗi
        VINAUDIO_ALIGN_MODEL = "facebook/wav2vec2-large-960h-lv60-self"
        
        logging.info(f"   Using custom alignment model: {VINAUDIO_ALIGN_MODEL}")
        try:
            model_a, metadata = whisperx.load_align_model(
                language_code="vi", # Vẫn giữ language code là "vi"
                device=device,
                model_name=VINAUDIO_ALIGN_MODEL # Thêm tham số model_name
            )
            logging.info("   Đang căn chỉnh thời gian (Forced Alignment)...")
            aligned_result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
        except ValueError as e:
            # Fallback (Phòng hờ): Nếu model trên vẫn lỗi, dùng model mặc định của WhisperX
            logging.warning(f"Failed to load custom alignment model: {e}. Falling back to default.")
            model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
            aligned_result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

        # Dọn dẹp model align
        del model_a
        gc.collect()
        torch.cuda.empty_cache()

        # --- BƯỚC 3: TỔNG HỢP KẾT QUẢ ---
        all_words = []
        for segment in aligned_result["segments"]:
            if "words" in segment:
                all_words.extend(segment["words"])
        
        # Lọc bỏ các từ thiếu timestamp (trường hợp hiếm gặp)
        valid_words = [w for w in all_words if 'start' in w and 'end' in w]

        logging.info(f"Hoàn tất! Tìm thấy {len(valid_words)} từ với timestamp chính xác.")
        return valid_words

    except Exception as e:
        logging.error(f"Lỗi nghiêm trọng trong WhisperX: {e}")
        # In ra log chi tiết để debug
        import traceback
        traceback.print_exc()
        return None