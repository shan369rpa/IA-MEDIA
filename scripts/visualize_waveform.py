# scripts/visualize_waveform_fcp_aligned.py

import argparse
import os
import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy import signal

# --- CẤU HÌNH MÀU SẮC CHUẨN FCP ---
FCP_COLORS = {
    "BACKGROUND": "#1e1e1e",      
    "TRACK_BG": "#262626",        
    "TEXT": "#d1d1d1",            
    "GRID": "#3b3b3b",            
    "CLEAN": "#3cc2ea",           # Xanh ngọc
    "RAW": "#64d2ff",             # Xanh dương nhạt
    "ERROR": "#ff5e5e",           # Đỏ cam
}

def auto_align_audio(y_clean, y_raw):
    """
    Tự động đồng bộ hóa y_raw khớp với y_clean bằng Cross-Correlation.
    Trả về: y_raw_aligned (đã dịch chuyển), và độ lệch (lag).
    """
    # Dùng FFT để tính tương quan chéo nhanh hơn
    correlation = signal.correlate(y_raw, y_clean, mode='full', method='fft')
    lags = signal.correlation_lags(len(y_raw), len(y_clean), mode='full')
    
    # Tìm vị trí mà độ tương đồng cao nhất
    lag = lags[np.argmax(correlation)]

    print(f"🔄 Auto-Alignment: Detected offset of {lag} samples.")

    y_raw_aligned = np.zeros_like(y_clean)

    # Thực hiện dịch chuyển (Shift)
    if lag > 0:
        # Raw bị trễ (nằm sau Clean) -> Cần kéo về trước (cắt đầu)
        # Chỉ lấy phần khớp, đảm bảo không vượt quá độ dài
        take_len = min(len(y_raw) - lag, len(y_clean))
        y_raw_aligned[:take_len] = y_raw[lag : lag + take_len]
    else:
        # Raw bị sớm (nằm trước Clean) -> Cần đẩy ra sau (đệm đầu)
        start_idx = abs(lag)
        take_len = min(len(y_raw), len(y_clean) - start_idx)
        y_raw_aligned[start_idx : start_idx + take_len] = y_raw[:take_len]

    return y_raw_aligned, lag

def calculate_envelope(y, resolution=512):
    """Tính đường bao biên độ để vẽ waveform đặc."""
    hop_length = resolution
    # Lấy max tuyệt đối trong mỗi khung
    envelope = np.array([np.max(np.abs(y[i:i+hop_length])) for i in range(0, len(y), hop_length)])
    return envelope

def style_axis(ax, title):
    """Style tối giản Dark Mode."""
    ax.set_facecolor(FCP_COLORS["TRACK_BG"])
    ax.set_title(title, color=FCP_COLORS["TEXT"], loc='left', fontsize=10, fontweight='bold', pad=10)
    ax.tick_params(axis='x', colors=FCP_COLORS["TEXT"], labelsize=8)
    ax.tick_params(axis='y', colors=FCP_COLORS["TEXT"], labelsize=8)
    for spine in ax.spines.values(): spine.set_visible(False)
    ax.grid(True, axis='x', color=FCP_COLORS["GRID"], linestyle='-', linewidth=0.5)
    ax.grid(False, axis='y')
    ax.set_ylim(-1.0, 1.0)

def plot_fcp_waveform(ax, time, envelope, color):
    """Vẽ sóng đối xứng."""
    ax.fill_between(time, 0, envelope, color=color, alpha=0.9, linewidth=0)
    ax.fill_between(time, 0, -envelope, color=color, alpha=0.9, linewidth=0)
    ax.axhline(0, color=FCP_COLORS["GRID"], linewidth=1, alpha=0.5)

def plot_comparison_fcp(clean_path, error_path, output_path=None):
    # 1. Tải Audio Raw (Data gốc)
    try:
        y_clean, sr = librosa.load(clean_path, sr=None)
        y_raw, _ = librosa.load(error_path, sr=None)
    except Exception as e:
        print(f"❌ Lỗi tải file: {e}")
        return

    # 2. [MỚI] TỰ ĐỘNG ĐỒNG BỘ HÓA
    # Chúng ta chỉnh sửa y_raw để nó khớp với y_clean
    y_raw_aligned, lag = auto_align_audio(y_clean, y_raw)

    # 3. Tính toán Envelope để vẽ (trên dữ liệu đã đồng bộ)
    HOP_LENGTH = 512
    env_clean = calculate_envelope(y_clean, HOP_LENGTH)
    env_raw = calculate_envelope(y_raw_aligned, HOP_LENGTH) # Dùng raw đã align
    
    # Tạo trục thời gian
    frames = range(len(env_clean))
    t = librosa.frames_to_time(frames, sr=sr, hop_length=HOP_LENGTH)

    # 4. Tính Difference (Sự khác biệt thực sự sau khi đã align)
    # Cắt về cùng độ dài envelope để trừ
    min_len = min(len(env_clean), len(env_raw))
    env_diff = np.abs(env_raw[:min_len] - env_clean[:min_len])
    t_diff = t[:min_len]

    # --- VẼ GIAO DIỆN FCP ---
    plt.style.use('dark_background')
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8), sharex=True, gridspec_kw={'hspace': 0.3})
    fig.patch.set_facecolor(FCP_COLORS["BACKGROUND"])

    # Track 1: RAW (Đã Align để dễ so sánh)
    info_text = f"(Auto-aligned: {lag} samples)" if lag != 0 else "(Perfectly synced)"
    style_axis(ax1, f"▶ SOURCE (Raw Aligned): {os.path.basename(error_path)} {info_text}")
    plot_fcp_waveform(ax1, t[:min_len], env_raw[:min_len], FCP_COLORS["RAW"])

    # Track 2: EDITED
    style_axis(ax2, f"▶ PROJECT (Edited): {os.path.basename(clean_path)}")
    plot_fcp_waveform(ax2, t[:min_len], env_clean[:min_len], FCP_COLORS["CLEAN"])

    # Track 3: DIFFERENCE
    style_axis(ax3, "⚠ DIFFERENCE (After Auto-Alignment)")
    plot_fcp_waveform(ax3, t_diff, env_diff, FCP_COLORS["ERROR"])
    
    ax3.set_xlabel("Timecode (seconds)", color=FCP_COLORS["TEXT"], fontsize=9)
    plt.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.08)

    if output_path:
        plt.savefig(output_path, facecolor=fig.get_facecolor(), dpi=150)
        print(f"✅ Đã lưu ảnh FCP Style (Aligned) tại: {output_path}")
    else:
        plt.show()

# ... (Phần main và Single Mode giữ nguyên như cũ) ...
if __name__ == "__main__":
    # (Giữ nguyên phần parse arguments của phiên bản trước)
    parser = argparse.ArgumentParser(description="Vẽ Waveform FCP có tự động đồng bộ.")
    parser.add_argument("input_path", type=str)
    parser.add_argument("--compare", type=str, default=None)
    parser.add_argument("-o", "--output", type=str, default=None)
    args = parser.parse_args()

    if args.compare:
        plot_comparison_fcp(args.compare, args.input_path, args.output)
    else:
        print("Chế độ Single không hỗ trợ trong đoạn code rút gọn này, vui lòng copy hàm plot_single_fcp vào.")