# src/ai/vectorizer.py

import os
from dotenv import load_dotenv
import logging
import torch
import torchaudio
# ==============================================================================
# MONKEY PATCH: SỬA LỖI XUNG ĐỘT PHIÊN BẢN (SpeechBrain vs Torchaudio)
# ==============================================================================

# 1. Ép Torchaudio sử dụng 'soundfile' làm backend. 
# Đây là backend ổn định nhất, không yêu cầu cài đặt ffmpeg/sox phức tạp ở tầng OS.
try:
    torchaudio.set_audio_backend("soundfile")
except Exception:
    # Fallback cho các phiên bản torchaudio mới không còn hàm set_audio_backend
    # Nó sẽ tự động ưu tiên soundfile nếu thư viện này đã được cài đặt.
    pass
# Vấn đề: SpeechBrain cũ gọi hàm 'list_audio_backends', nhưng Torchaudio mới đã xóa nó.
# Giải pháp: Chúng ta tự định nghĩa lại hàm này vào module torchaudio trước khi SpeechBrain chạy.
if not hasattr(torchaudio, 'list_audio_backends'):
    def _list_audio_backends():
        # Trả về danh sách backend giả lập để SpeechBrain vui vẻ
        return ['ffmpeg', 'sox'] 
    torchaudio.list_audio_backends = _list_audio_backends
    logging.warning("⚠️ Đã áp dụng bản vá nóng cho lỗi torchaudio.list_audio_backends")
# ==============================================================================
# Biến toàn cục để cache model, tránh tải lại nhiều lần
# This acts as a simple in-memory cache for the model.

from speechbrain.pretrained import EncoderClassifier

_model = None
_device = None

def _get_device():
    """Xác định thiết bị để chạy model (GPU nếu có, không thì CPU)."""
    global _device
    if _device is None:
        _device = "cuda" if torch.cuda.is_available() else "cpu"
        logging.info(f"Đã xác định thiết bị tính toán là: {_device.upper()}")
    return _device

def load_embedding_model():
    """
    Tải model embedding từ SpeechBrain (Hugging Face).
    Sử dụng cache để chỉ tải model một lần duy nhất.
    """
    global _model
    load_dotenv()
    
    # Nếu model đã được tải, trả về nó ngay lập tức
    if _model is not None:
        logging.info("Sử dụng model embedding đã được cache.")
        return _model
    
    model_name = os.getenv("EMBEDDING_MODEL", "speechbrain/spkrec-ecapa-voxceleb")
    logging.info(f"Bắt đầu tải model embedding: {model_name}...")
    logging.info("Quá trình này có thể mất vài phút cho lần chạy đầu tiên...")

    try:
        device = _get_device()
        # Tải model vào thiết bị đã chọn (GPU/CPU)
        classifier = EncoderClassifier.from_hparams(
            source=model_name, 
            run_opts={"device": device}
        )
        _model = classifier
        logging.info("Tải model embedding thành công.")
        return _model
    except Exception as e:
        logging.error(f"Lỗi khi tải model embedding: {e}")
        return None

def create_embedding(audio_path: str, model: EncoderClassifier) -> list | None:
    """
    Tạo một vector embedding từ một file audio chunk.

    Args:
        audio_path (str): Đường dẫn đến file audio .wav.
        model (EncoderClassifier): Model SpeechBrain đã được tải.

    Returns:
        list: Một list float đại diện cho vector embedding, hoặc None nếu có lỗi.
    """
    if not os.path.exists(audio_path):
        logging.warning(f"File audio không tồn tại, không thể tạo embedding: {audio_path}")
        return None

    try:
        device = _get_device()
        
        # 1. Tải và tiền xử lý tín hiệu audio
        signal, fs = torchaudio.load(audio_path)
        
        # Đảm bảo audio có đúng tần số mẫu (resample nếu cần)
        # Model này thường yêu cầu 16kHz
        if fs != 16000:
            # Logic resample sẽ cần thêm ở đây nếu cần thiết, tạm thời bỏ qua
            logging.warning(f"Tần số mẫu của file {audio_path} là {fs}Hz, không phải 16000Hz. Kết quả có thể không chính xác.")

        # 2. Dùng model để trích xuất embedding
        # Model của SpeechBrain nhận tín hiệu và độ dài tương đối của nó
        embeddings = model.encode_batch(signal.to(device))
        
        # 3. Chuẩn hóa và chuyển đổi kết quả
        # Kết quả thường có dạng [1, 1, N], cần reshape và chuyển thành list
        vector = embeddings.squeeze().cpu().numpy().tolist()
        
        return vector
        
    except Exception as e:
        logging.error(f"Lỗi khi tạo embedding cho file {audio_path}: {e}")
        return None
# --- [BỔ SUNG MỚI] ---
def create_sliding_window_embeddings(
    audio_path: str, 
    model: EncoderClassifier, 
    window_len: float = 0.1, # 100ms
    step: float = 0.05       # 50ms
) -> list | None:
    """
    Tạo một chuỗi các vector embedding bằng cách trượt cửa sổ trên file audio.
    Trả về danh sách các vector con.
    """
    if not os.path.exists(audio_path):
        return None
    try:
        device = _get_device()
        signal, fs = torchaudio.load(audio_path)
        
        if signal.shape[0] > 1:
            signal = signal.mean(dim=0, keepdim=True)
            
        if fs != 16000:
            resampler = torchaudio.transforms.Resample(fs, 16000).to(device)
            signal = resampler(signal.to(device))
        else:
            signal = signal.to(device)

        window_samples = int(window_len * 16000)
        step_samples = int(step * 16000)
        total_samples = signal.shape[1]

        if total_samples < window_samples:
            logging.debug(f"File quá ngắn, tạo 1 embedding duy nhất: {audio_path}")
            # Tái sử dụng `signal` đã có trong RAM
            embeddings = model.encode_batch(signal.to(_get_device()))
            vector = embeddings.squeeze().cpu().numpy().tolist()
            return [vector] # Trả về list chứa 1 vector duy nhất

        # Dùng unfold để tạo cửa sổ trượt cực nhanh trên Tensor
        try: 
            windows = signal.unfold(1, window_samples, step_samples)
            windows = windows.permute(1, 0, 2)
        
            # Xử lý theo batch để tiết kiệm VRAM
            batch_size = 128
            all_vectors = []
            for i in range(0, windows.size(0), batch_size):
                batch = windows[i:i+batch_size]
                with torch.no_grad(): # Tối ưu hóa, không cần tính gradient
                    embeddings = model.encode_batch(batch)
                vectors = embeddings.squeeze(1).cpu().numpy().tolist()
                all_vectors.extend(vectors)
                
            return all_vectors

        except RuntimeError as e:
            # Bắt chính xác lỗi RuntimeError liên quan đến padding
            if "padding" in str(e):
                logging.warning(f"Lỗi padding khi unfold file {os.path.basename(audio_path)}. Tạo 1 embedding duy nhất làm fallback.")
                # Giải pháp thay thế: Nếu unfold lỗi, chỉ tạo 1 vector cho cả từ
                embeddings = model.encode_batch(signal)
                vector = embeddings.squeeze().cpu().numpy().tolist()
                return [vector]
            else:
                # Nếu là lỗi RuntimeError khác, báo lỗi như bình thường
                raise e
                
    except Exception as e:
        logging.error(f"Lỗi xử lý audio sliding window cho {audio_path}: {e}")
        return None
if __name__ == '__main__':
    # Phần này để chạy test nhanh cho module
    print("Chạy test nhanh cho module vectorizer...")
    
    # Tạo một file audio giả để test
    SAMPLE_RATE = 16000
    dummy_signal = torch.randn(1, SAMPLE_RATE * 2) # Tín hiệu 2 giây
    dummy_path = "dummy_audio.wav"
    torchaudio.save(dummy_path, dummy_signal, SAMPLE_RATE)
    
    print(f"Đã tạo file audio giả: {dummy_path}")
    
    # Test tải model
    loaded_model = load_embedding_model()
    if loaded_model:
        # Test tạo embedding
        embedding_vector = create_embedding(dummy_path, loaded_model)
        if embedding_vector:
            print(f"Tạo embedding thành công! Kích thước Vector: {len(embedding_vector)}")
            # Model ecapa-voxceleb thường có kích thước 192, không phải 1024
            # Chúng ta cần cập nhật lại CSDL
            if len(embedding_vector) != 192:
                 print(f"CẢNH BÁO: Kích thước vector là {len(embedding_vector)}, không phải 192 như mong đợi.")
        else:
            print("Tạo embedding thất bại.")
    else:
        print("Tải model thất bại.")
        
    # Dọn dẹp
    if os.path.exists(dummy_path):
        os.remove(dummy_path)