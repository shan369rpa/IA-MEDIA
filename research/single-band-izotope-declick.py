import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd

# ==========================================
# CẤU HÌNH THÔNG SỐ (SINGLE-BAND SETTINGS)
# ==========================================
SAMPLE_RATE = 44100
DURATION = 0.03          # 30ms (Rất ngắn để soi kỹ lỗi Digital)
SENSITIVITY = 5.0        # Độ nhạy trung bình
CLICK_WIDENING_MS = 0.5  # Digital click thường gọn, không cần widening lớn

# ==========================================
# 1. TẠO INPUT GIẢ LẬP (DIGITAL GLITCH SCENARIO)
# ==========================================
t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION))

# A. Tín hiệu Nhạc (Mô phỏng 1 cú Kick Drum + High Hat)
# Kick Drum (Tần số thấp, biên độ lớn, giảm dần)
kick_transient = 0.8 * np.sin(2 * np.pi * 60 * t) * np.exp(-t * 50)
# High Hat (Tần số cao, biên độ nhỏ)
hat_noise = 0.1 * np.random.normal(0, 1, len(t))
clean_signal = kick_transient + hat_noise

# B. Tạo Lỗi Digital (Spikes)
corrupted_signal = clean_signal.copy()

# Lỗi: Digital Spike (Gai nhọn, thẳng đứng, không có đuôi trầm)
# Đây là đặc trưng của lỗi Clock hoặc Buffer dropout
click_pos = int(len(t) * 0.5)
corrupted_signal[click_pos] = 1.0       # Gai dương
corrupted_signal[click_pos+1] = -1.0    # Gai âm (Zero crossing error)

# ==========================================
# 2. KHỐI XỬ LÝ: PHÂN TÍCH & PHÁT HIỆN (BROADBAND DETECTION)
# ==========================================
# KHÔNG CÓ BƯỚC TÁCH DẢI TẦN (CROSSOVER) Ở ĐÂY

def detect_single_band(signal, sensitivity):
    """
    Thuật toán Single-band: Soi trên toàn dải
    """
    # 1. Tính Envelope (Năng lượng nền toàn dải)
    # Cửa sổ trượt nhanh (0.5ms) để bắt kịp các gai nhọn
    window = int(SAMPLE_RATE * 0.0005) 
    abs_sig = np.abs(signal)
    
    # Tính RMS cục bộ
    local_env = pd.Series(abs_sig).rolling(window=window, center=True, min_periods=1).mean().values
    
    # 2. Tính Threshold Factor
    # Base factor
    thresh_factor = 12.0 - sensitivity
    
    # Ngưỡng động
    dynamic_threshold = local_env * thresh_factor
    
    # Bảo vệ mức sàn (Noise floor protection)
    # Để tránh bắt nhầm noise nền nhỏ xíu thành click
    dynamic_threshold = np.maximum(dynamic_threshold, 0.05)
    
    # 3. Xác định vị trí lỗi
    # Logic: Chỉ bắt khi biên độ vượt ngưỡng
    is_click = abs_sig > dynamic_threshold
    
    return is_click, dynamic_threshold

click_mask, threshold_line = detect_single_band(corrupted_signal, SENSITIVITY)

# ==========================================
# 3. KHỐI XỬ LÝ: KHOANH VÙNG (WIDENING)
# ==========================================
def apply_widening(mask, widening_ms, fs):
    widening_samples = int((widening_ms / 1000) * fs)
    indices = np.where(mask)[0]
    new_mask = np.zeros_like(mask)
    
    if len(indices) == 0: return new_mask
    
    for idx in indices:
        start = max(0, idx - widening_samples)
        end = min(len(mask), idx + widening_samples + 1)
        new_mask[start:end] = True
    return new_mask

repair_mask = apply_widening(click_mask, CLICK_WIDENING_MS, SAMPLE_RATE)

# ==========================================
# 4. KHỐI XỬ LÝ: NỘI SUY (INTERPOLATION)
# ==========================================
def repair_signal(signal, mask, time_array):
    if np.sum(mask) == 0: return signal
    
    valid_x = time_array[~mask]
    valid_y = signal[~mask]
    target_x = time_array[mask]
    
    # Cubic Spline Interpolation
    interpolator = interp1d(valid_x, valid_y, kind='cubic', fill_value="extrapolate")
    repaired_segment = interpolator(target_x)
    
    output = signal.copy()
    output[mask] = repaired_segment
    return output

final_output = repair_signal(corrupted_signal, repair_mask, t)

# ==========================================
# 5. TRỰC QUAN HÓA (SINGLE-BAND DASHBOARD)
# ==========================================
fig, ax = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# Plot 1: Input & The Problem
ax[0].set_title("BƯỚC 1: INPUT TOÀN DẢI (BROADBAND INPUT)")
ax[0].plot(t, corrupted_signal, 'k', label='Tín hiệu Lỗi')
ax[0].plot(t, clean_signal, 'g--', alpha=0.5, label='Nhạc sạch (Kick Drum)')
ax[0].annotate('Digital Spike', xy=(t[click_pos], 1.0), xytext=(t[click_pos]+0.005, 0.8),
             arrowprops=dict(facecolor='red', shrink=0.05))
ax[0].legend(loc='upper right')

# Plot 2: Detection Logic
ax[1].set_title(f"BƯỚC 2: PHÁT HIỆN LỖI (Sensitivity: {SENSITIVITY})")
ax[1].plot(t, np.abs(corrupted_signal), 'b', alpha=0.3, label='Biên độ tuyệt đối')
ax[1].plot(t, threshold_line, 'r-', linewidth=2, label='Ngưỡng Động (Dynamic Threshold)')
# Tô màu vùng lỗi
ax[1].fill_between(t, 0, 1.2, where=click_mask, color='red', alpha=0.5, label='Bị Bắt (Detected)')
ax[1].legend(loc='upper right')

# Plot 3: Result
ax[2].set_title("BƯỚC 3: KẾT QUẢ SAU NỘI SUY")
ax[2].plot(t, clean_signal, 'g--', alpha=0.6, label='Gốc')
ax[2].plot(t, final_output, 'b-', alpha=0.8, label='Single-band Output')
ax[2].plot(t, corrupted_signal, 'r:', alpha=0.4, label='Lỗi cũ')
ax[2].legend(loc='upper right')

plt.tight_layout()
plt.show()