# scripts/benchmark_proof.py
import time
import numpy as np
import torch
import librosa
from scipy import signal
from transformers import Wav2Vec2Model, Wav2Vec2FeatureExtractor

# --- CẤU HÌNH ---
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"
SAMPLE_RATE = 16000
TEST_DURATION = 1.0 # 1 giây
NUM_SAMPLES = 64 # Giả lập 64 đoạn audio (tương đương 1 phút video)

print(f"🚀 BẮT ĐẦU BENCHMARK TRÊN {DEVICE.upper()}...")

# 1. TẠO DỮ LIỆU GIẢ LẬP (Lệch pha)
print("\n--- 1. KIỂM TRA AUTO-ALIGNMENT ---")
# Tạo tín hiệu gốc (Sóng sin)
t = np.linspace(0, TEST_DURATION, int(TEST_DURATION * SAMPLE_RATE))
y_clean = np.sin(2 * np.pi * 440 * t) # Note La
# Tạo tín hiệu lỗi (Lệch 50ms so với gốc)
shift_samples = int(0.05 * SAMPLE_RATE) # 50ms
y_error = np.roll(y_clean, shift_samples) 
# Thêm chút nhiễu thật vào y_error để mô phỏng lỗi
y_error += 0.1 * np.random.normal(0, 1, len(y_error))

# Tính Diff trước khi Align
diff_before = np.mean(np.abs(y_error - y_clean))
print(f"🔴 Sai số trung bình (Chưa Align): {diff_before:.4f}")

# Chạy Auto-Align (Code mới)
start_time = time.time()
correlation = signal.correlate(y_error, y_clean, mode='full', method='fft')
lags = signal.correlation_lags(len(y_error), len(y_clean), mode='full')
lag = lags[np.argmax(correlation)]
# Shift ngược lại
if lag > 0:
    y_aligned = y_error[lag:]
    y_clean_cut = y_clean[:len(y_aligned)]
else:
    y_aligned = y_error[:len(y_error)+lag]
    y_clean_cut = y_clean[-lag:]

# Tính Diff sau khi Align
diff_after = np.mean(np.abs(y_aligned - y_clean_cut))
print(f"🟢 Sai số trung bình (Đã Align):  {diff_after:.4f}")
print(f"⚡ Thời gian Align: {(time.time() - start_time)*1000:.2f} ms")

if diff_after < diff_before:
    print("=> KẾT LUẬN: Auto-Alignment hoạt động HIỆU QUẢ. Đã loại bỏ sai số do lệch thời gian.")
else:
    print("=> KẾT LUẬN: Auto-Alignment KHÔNG hiệu quả.")

# ---------------------------------------------------------

print("\n--- 2. KIỂM TRA TỐC ĐỘ BATCH PROCESSING (M2 ULTRA) ---")
# Tải Model
model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-large-xlsr-53").to(DEVICE)
feature_extractor = Wav2Vec2FeatureExtractor(feature_size=1, sampling_rate=16000, padding_value=0.0, do_normalize=True, return_attention_mask=True)

# Tạo 64 mẫu audio giả
batch_audio = [np.random.randn(16000) for _ in range(NUM_SAMPLES)]

# Cách 1: Chạy vòng lặp (Cách cũ)
print(f"⏳ Đang chạy Loop từng mẫu ({NUM_SAMPLES} mẫu)...")
start_loop = time.time()
for audio in batch_audio:
    inputs = feature_extractor(audio, sampling_rate=16000, return_tensors="pt")
    with torch.no_grad():
        model(inputs.input_values.to(DEVICE))
time_loop = time.time() - start_loop
print(f"🔴 Thời gian Loop: {time_loop:.2f} giây")

# Cách 2: Chạy Batch (Cách mới)
print(f"⏳ Đang chạy Batch ({NUM_SAMPLES} mẫu cùng lúc)...")
start_batch = time.time()
inputs = feature_extractor(batch_audio, sampling_rate=16000, return_tensors="pt", padding=True)
input_values = inputs.input_values.to(DEVICE)
with torch.no_grad():
    model(input_values)
time_batch = time.time() - start_batch
print(f"🟢 Thời gian Batch: {time_batch:.2f} giây")

speedup = time_loop / time_batch
print(f"\n=> KẾT LUẬN: Batch Processing nhanh gấp {speedup:.1f} LẦN.")

if speedup > 2.0:
    print("=> Nâng cấp này ĐÁNG GIÁ để triển khai.")
else:
    print("=> Không cần thiết nâng cấp.")