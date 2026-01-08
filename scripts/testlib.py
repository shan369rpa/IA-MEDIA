import torch
import torchaudio
from transformers import Wav2Vec2Model, Wav2Vec2FeatureExtractor
import logging

# Cấu hình log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_sota_model():
    print("✅ Đang kiểm tra môi trường...")
    # 1. Cấu hình thiết bị (M2 Ultra)
    if torch.backends.mps.is_available():
        device = torch.device("mps")
        print("🚀 Sử dụng thiết bị: MPS (Apple Metal)")
    else:
        device = torch.device("cpu")
        print("⚠️ Sử dụng thiết bị: CPU")

    model_name = "facebook/wav2vec2-large-xlsr-53"

    try:
        print(f"⏳ Đang tải Model Weights: {model_name}...")
        # 2. Tải Model (Cái này có file trên Hub nên sẽ tải được)
        model = Wav2Vec2Model.from_pretrained(model_name).to(device)
        model.eval() # Chế độ suy luận

        print("🛠️ Đang khởi tạo Feature Extractor thủ công...")
        # 3. KHỞI TẠO THỦ CÔNG (FIX LỖI THIẾU FILE CONFIG)
        # Thay vì tải from_pretrained, ta tạo mới với thông số chuẩn của Wav2Vec2
        processor = Wav2Vec2FeatureExtractor(
            feature_size=1,
            sampling_rate=16000,
            padding_value=0.0,
            do_normalize=True,
            return_attention_mask=True
        )
        
        print("✅ Đã tải thành công Model và Processor!")
        return model, processor, device

    except Exception as e:
        print(f"❌ Vẫn lỗi: {e}")
        return None, None, None

# --- CHẠY THỬ NGHIỆM ---
if __name__ == "__main__":
    model, processor, device = load_sota_model()
    
    if model:
        # Test với dữ liệu giả để đảm bảo pipeline chạy được
        print("\n🧪 Đang chạy thử một mẫu giả lập...")
        # Tạo 1 giây âm thanh giả (16000 mẫu)
        dummy_audio = torch.randn(16000).numpy() 
        
        # Xử lý qua Processor
        inputs = processor(dummy_audio, sampling_rate=16000, return_tensors="pt")
        input_values = inputs.input_values.to(device)
        
        # Chạy qua Model
        with torch.no_grad():
            outputs = model(input_values)
            
        # Lấy vector (Mean pooling)
        embeddings = torch.mean(outputs.last_hidden_state, dim=1)
        
        print(f"✅ Kết quả vector shape: {embeddings.shape}")
        print("🎉 CHÚC MỪNG! HỆ THỐNG ĐÃ SẴN SÀNG TRÊN M2 ULTRA.")