import os
import random
import numpy as np
import librosa
import soundfile as sf
import pandas as pd
import scipy.signal

# Cấu hình đường dẫn (Lấy từ backend_core nếu có, hoặc định nghĩa lại)
DATA_FOLDER = "collected_data"
BG_BANK_FOLDER = "background_bank"
DIFF_BANK_FOLDER = "diff_bank" # Nơi chứa các file Diff được trích xuất từ Tab 2

# Tạo thư mục nếu chưa có
for d in [BG_BANK_FOLDER, DIFF_BANK_FOLDER]:
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

# --- 1. CÔNG CỤ XỬ LÝ BACKGROUND ---

def check_audio_quality(y, sr, mode="quiet"):
    """
    Kiểm tra chất lượng đoạn audio để lọc Background.
    """
    rms = np.sqrt(np.mean(y**2))
    
    # Ngưỡng (cần tinh chỉnh tùy vào video gốc)
    if mode == "quiet":
        # Lấy đoạn tĩnh: Không quá to (tiếng nói) và không tắt hẳn (mute)
        return 0.0001 < rms < 0.02 
    elif mode == "speech":
        # Lấy đoạn có tiếng nói
        return rms > 0.02
    return True

def extract_background_samples(video_path, clip_duration=1.0, max_samples=50, mode="quiet"):
    """
    Cắt video dài thành các mẫu nền nhỏ.
    """
    saved_paths = []
    try:
        # Load audio (mono, 16k)
        y, sr = librosa.load(video_path, sr=16000, mono=True)
        
        total_samples = len(y)
        chunk_samples = int(clip_duration * sr)
        
        # Bước nhảy ngẫu nhiên để lấy mẫu đa dạng, hoặc tuần tự
        # Ở đây dùng tuần tự có bước nhảy để tránh trùng lặp
        step = chunk_samples 
        
        count = 0
        for i in range(0, total_samples - chunk_samples, step):
            if count >= max_samples: break
            
            chunk = y[i : i + chunk_samples]
            
            if check_audio_quality(chunk, sr, mode):
                # Lưu file
                base_name = os.path.basename(video_path).rsplit('.', 1)[0]
                filename = f"bg_{base_name}_{i}.wav"
                save_path = os.path.join(BG_BANK_FOLDER, filename)
                
                sf.write(save_path, chunk, sr)
                saved_paths.append(save_path)
                count += 1
                
        return saved_paths, f"Đã khai thác thành công {len(saved_paths)} mẫu nền."
    except Exception as e:
        return [], f"Lỗi khai thác nền: {e}"

# --- 2. CÁC THUẬT TOÁN BIẾN ĐỔI (AUGMENTATION) ---

def algo_time_stretch(y, rate=None):
    """Co giãn thời gian (nhanh/chậm)."""
    if rate is None: rate = random.uniform(0.8, 1.2)
    try:
        return librosa.effects.time_stretch(y, rate=rate)
    except: return y # Fallback nếu lỗi

def algo_pitch_shift(y, sr=16000, n_steps=None):
    """Dịch chuyển cao độ (trầm/bổng)."""
    if n_steps is None: n_steps = random.uniform(-2, 2)
    try:
        return librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)
    except: return y

def algo_mix_add(bg, error, snr_db):
    """
    Trộn cộng tín hiệu (Additive Mixing) với SNR kiểm soát.
    """
    # 1. Cắt/Pad cho bằng độ dài nền
    target_len = len(bg)
    if len(error) > target_len:
        error = error[:target_len]
    elif len(error) < target_len:
        # Random vị trí xuất hiện của lỗi trong nền
        start = random.randint(0, target_len - len(error))
        error = np.pad(error, (start, target_len - len(error) - start), 'constant')

    # 2. Tính năng lượng
    rms_bg = np.sqrt(np.mean(bg**2)) + 1e-9
    rms_err = np.sqrt(np.mean(error**2)) + 1e-9

    # 3. Tính hệ số scale để đạt SNR mong muốn
    # SNR = 20 * log10(RMS_Signal / RMS_Noise)
    # Ở đây ta coi Error là Signal cần nghe thấy, BG là Noise nền
    # Target_RMS_Error = RMS_BG * 10^(SNR/20)
    target_rms = rms_bg * (10**(snr_db / 20))
    scale = target_rms / rms_err
    
    mixed = bg + (error * scale)
    
    # Chuẩn hóa chống clipping
    max_val = np.max(np.abs(mixed))
    if max_val > 1.0:
        mixed = mixed / max_val
        
    return mixed

def algo_feature_grafting(bg, error, strength=0.5):
    """
    [CAO CẤP] Cấy ghép đặc trưng trên miền tần số (Spectral Grafting).
    Thay thế các tần số mạnh của lỗi vào nền, giữ nguyên pha của nền để tự nhiên hơn.
    """
    # Đảm bảo độ dài bằng nhau
    min_len = min(len(bg), len(error))
    bg = bg[:min_len]
    error = error[:min_len]
    
    # STFT
    n_fft = 2048
    hop = 512
    S_bg = librosa.stft(bg, n_fft=n_fft, hop_length=hop)
    S_err = librosa.stft(error, n_fft=n_fft, hop_length=hop)
    
    # Tách Magnitude và Phase
    mag_bg, phase_bg = librosa.magphase(S_bg)
    mag_err, _ = librosa.magphase(S_err)
    
    # Grafting: Lấy max năng lượng tại mỗi điểm tần số
    # (Giống chế độ hòa trộn 'Lighten' trong Photoshop)
    mag_mix = np.maximum(mag_bg, mag_err * strength)
    
    # Tái tạo với pha của nền (giúp âm thanh 'hòa' vào không gian nền hơn)
    S_mix = mag_mix * phase_bg
    
    # ISTFT
    mixed = librosa.istft(S_mix, hop_length=hop)
    return mixed

# --- 3. SYNTHESIS ENGINE (TRÌNH ĐIỀU PHỐI) ---

def synthesize_sample(bg_path, diff_path, algo_type="Mix", snr=0):
    """
    Hàm chính để sinh mẫu giả lập.
    """
    try:
        # Load data
        bg, sr = librosa.load(bg_path, sr=16000)
        err, _ = librosa.load(diff_path, sr=16000)
        
        # Tiền xử lý lỗi (Biến dạng)
        if algo_type == "Time Stretch":
            err = algo_time_stretch(err)
        elif algo_type == "Frequency Shift":
            err = algo_pitch_shift(err)
        elif algo_type == "Shuffle":
            if random.random() > 0.5: err = algo_time_stretch(err)
            if random.random() > 0.5: err = algo_pitch_shift(err)
            
        # Trộn
        if algo_type == "Feature Grafting":
            # Grafting không dùng SNR theo cách cộng, mà dùng strength
            # Convert SNR -10..10 thành strength 0.1..2.0
            strength = 1.0 + (snr / 10.0) 
            mixed = algo_feature_grafting(bg, err, strength)
        else:
            # Các thuật toán còn lại dùng phép cộng Mix chuẩn
            mixed = algo_mix_add(bg, err, snr)
            
        return mixed, bg, sr
        
    except Exception as e:
        print(f"Lỗi sinh mẫu: {e}")
        return None, None, None