import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfilt, medfilt
from scipy.interpolate import interp1d
import pandas as pd

# ==========================================
# CẤU HÌNH THÔNG SỐ (PARAMS - GIỐNG TRÊN RX 11)
# ==========================================
SAMPLE_RATE = 44100
DURATION = 0.05          # 50ms (Zoom vào 1 đoạn ngắn để thấy rõ sóng)
SENSITIVITY = 7.0        # Độ nhạy (1-10)
CLICK_WIDENING_MS = 1.0  # Mở rộng vùng sửa (ms)
FREQ_SKEW = -5.0         # Âm: Ưu tiên sửa Bass (Vinyl) | Dương: Ưu tiên sửa Treble

# ==========================================
# 1. TẠO INPUT GIẢ LẬP (REALISTIC VINYL SIMULATION)
# ==========================================
t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION))

# A. Tín hiệu Nhạc (Bass trầm + Melody cao)
# Bass 100Hz (Kick drum body)
clean_bass = 0.8 * np.sin(2 * np.pi * 100 * t) 
# Melody 2000Hz
clean_high = 0.3 * np.sin(2 * np.pi * 2000 * t)
clean_signal = clean_bass + clean_high

# B. Tạo Lỗi (Clicks & Pops)
corrupted_signal = clean_signal.copy()

# Lỗi 1: Low Thump (Tiếng bụp trầm - Đặc trưng Vinyl)
click_pos_1 = int(len(t) * 0.3)
corrupted_signal[click_pos_1:click_pos_1+10] += 1.5 # Biên độ lớn, dài

# Lỗi 2: High Tick (Tiếng tách - Digital/Surface noise)
click_pos_2 = int(len(t) * 0.7)
corrupted_signal[click_pos_2:click_pos_2+3] += 0.8 # Ngắn, sắc

# ==========================================
# 2. KHỐI XỬ LÝ 1: PHÂN TÁCH DẢI TẦN (CROSSOVER)
# ==========================================
def butter_filter(data, cutoff, fs, btype='low', order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    sos = butter(order, normal_cutoff, btype=btype, output='sos')
    return sosfilt(sos, data)

# Tách thành Low Band và High Band tại điểm cắt 1000Hz
CROSSOVER_FREQ = 1000
low_band = butter_filter(corrupted_signal, CROSSOVER_FREQ, SAMPLE_RATE, 'low')
high_band = butter_filter(corrupted_signal, CROSSOVER_FREQ, SAMPLE_RATE, 'high')

# ==========================================
# 3. KHỐI XỬ LÝ 2: PHÂN TÍCH & PHÁT HIỆN (DETECTION CORE)
# ==========================================
def detect_clicks(signal, sensitivity, skew_val, band_type):
    """
    Thuật toán phát hiện dựa trên Năng lượng trung bình & Skew
    """
    # 1. Tính Envelope (Năng lượng nền)
    # Dùng cửa sổ trượt 2ms để tính RMS cục bộ
    window = int(SAMPLE_RATE * 0.002) 
    abs_sig = np.abs(signal)
    local_env = pd.Series(abs_sig).rolling(window=window, center=True, min_periods=1).mean().values
    
    # 2. Tính Threshold Factor dựa trên Sensitivity
    # Sensitivity càng cao -> Base Factor càng thấp (dễ bắt lỗi)
    base_factor = 12.0 - sensitivity 
    
    # 3. Áp dụng Frequency Skew (Logic quan trọng của Advanced)
    # Nếu Skew Âm -> Giảm Threshold của Low Band (Nhạy hơn với Bass)
    # Nếu Skew Dương -> Giảm Threshold của High Band
    skew_modifier = 0
    if band_type == 'low' and skew_val < 0:
        skew_modifier = skew_val * 0.5 # Làm Threshold thấp xuống
    elif band_type == 'high' and skew_val > 0:
        skew_modifier = -skew_val * 0.5 
        
    final_threshold_factor = max(1.1, base_factor + skew_modifier)
    dynamic_threshold = local_env * final_threshold_factor
    
    # 4. Xác định vị trí lỗi
    is_click = abs_sig > dynamic_threshold
    return is_click, dynamic_threshold

# Chạy detection cho từng band
low_click_mask, low_thresh = detect_clicks(low_band, SENSITIVITY, FREQ_SKEW, 'low')
high_click_mask, high_thresh = detect_clicks(high_band, SENSITIVITY, FREQ_SKEW, 'high')

# ==========================================
# 4. KHỐI XỬ LÝ 3: KHOANH VÙNG (LOCALIZATION & WIDENING)
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

# Mở rộng vùng lỗi
low_repair_mask = apply_widening(low_click_mask, CLICK_WIDENING_MS, SAMPLE_RATE)
high_repair_mask = apply_widening(high_click_mask, CLICK_WIDENING_MS, SAMPLE_RATE)

# ==========================================
# 5. KHỐI XỬ LÝ 4: NỘI SUY & HỒI PHỤC (INTERPOLATION)
# ==========================================
def repair_band(signal, mask, time_array):
    if np.sum(mask) == 0: return signal # Không có lỗi thì trả về nguyên vẹn
    
    # Dữ liệu sạch (Training data)
    valid_x = time_array[~mask]
    valid_y = signal[~mask]
    
    # Dữ liệu cần sửa (Target data)
    target_x = time_array[mask]
    
    # Thuật toán Cubic Spline (Mô phỏng RX Interpolation)
    interpolator = interp1d(valid_x, valid_y, kind='cubic', fill_value="extrapolate")
    repaired_segment = interpolator(target_x)
    
    # Ghép lại
    output = signal.copy()
    output[mask] = repaired_segment
    return output

repaired_low = repair_band(low_band, low_repair_mask, t)
repaired_high = repair_band(high_band, high_repair_mask, t)

# ==========================================
# 6. KHỐI XỬ LÝ 5: TỔNG HỢP (RECONSTRUCTION)
# ==========================================
final_output = repaired_low + repaired_high

# ==========================================
# 7. TRỰC QUAN HÓA (VISUALIZATION DASHBOARD)
# ==========================================
fig, ax = plt.subplots(4, 1, figsize=(12, 14), sharex=True)

# Plot 1: Input & Crossover
ax[0].set_title(f"BƯỚC 1: INPUT & CROSSOVER SPLIT (Freq Skew: {FREQ_SKEW})")
ax[0].plot(t, corrupted_signal, 'k', alpha=0.3, label='Hỗn hợp gốc (Lỗi)')
ax[0].plot(t, low_band, 'b', label='Dải Trầm (Low Band)')
ax[0].plot(t, high_band, 'orange', label='Dải Cao (High Band)')
ax[0].legend(loc='upper right')

# Plot 2: Detection Logic (Low Band focus due to Negative Skew)
ax[1].set_title("BƯỚC 2: PHÂN TÍCH NGƯỠNG ĐỘNG (Focus: Low Band)")
ax[1].plot(t, np.abs(low_band), 'b', alpha=0.6, label='Biên độ Low Band')
ax[1].plot(t, low_thresh, 'r--', linewidth=2, label='Ngưỡng Động (Đã tính Skew)')
# Tô màu vùng bị phát hiện vượt ngưỡng
ax[1].fill_between(t, 0, 1, where=low_click_mask, color='red', alpha=0.3, transform=ax[1].get_xaxis_transform(), label='Phát hiện Lỗi (Detected)')
ax[1].legend(loc='upper right')

# Plot 3: Widening & Removal
ax[2].set_title(f"BƯỚC 3: KHOANH VÙNG & MỞ RỘNG (Widening: {CLICK_WIDENING_MS}ms)")
ax[2].plot(t, low_band, 'k', alpha=0.3, label='Low Band Gốc')
# Vẽ những điểm dữ liệu bị xóa
removed_data = low_band.copy()
removed_data[~low_repair_mask] = np.nan
ax[2].plot(t, removed_data, 'r.', markersize=5, label='Mẫu bị xóa (Removed Samples)')
ax[2].legend(loc='upper right')

# Plot 4: Final Result Comparison
ax[3].set_title("BƯỚC 4 & 5: NỘI SUY & KẾT QUẢ CUỐI CÙNG")
ax[3].plot(t, clean_signal, 'g--', alpha=0.5, label='Clean Reference (Lý tưởng)')
ax[3].plot(t, corrupted_signal, 'r', alpha=0.3, label='Input Lỗi')
ax[3].plot(t, final_output, 'b', linewidth=1.5, label='RX Final Output')
ax[3].legend(loc='upper right')

plt.tight_layout()
plt.show()