# src/analysis/signal_analyzer.py

import librosa
import numpy as np
import logging

# Cấu hình ngưỡng (Thresholds) - Cần tinh chỉnh thực tế
CLIPPING_THRESHOLD = 0.99  # Biên độ gần tối đa (1.0)
LOW_VOLUME_RMS = 0.01      # Ngưỡng năng lượng quá thấp
NOISE_DIFF_RATIO = 1.5     # Nếu RMS của error gấp 1.5 lần clean -> Khả năng cao là nhiễu

def analyze_audio_defects(clean_path: str, error_path: str) -> dict:
    """
    Phân tích và so sánh cặp audio clean/error để phát hiện các lỗi kỹ thuật.
    
    Returns:
        dict: Chứa 'label' (loại lỗi phát hiện được) và 'metrics' (các chỉ số).
    """
    result = {
        "label": "error", # Nhãn mặc định nếu không phát hiện lỗi kỹ thuật cụ thể
        "details": {}
    }

    try:
        # 1. Tải audio (librosa tải về dạng float32 từ -1 đến 1)
        # sr=None để giữ nguyên tần số mẫu gốc (thường là 16kHz)
        y_clean, sr_clean = librosa.load(clean_path, sr=None)
        y_error, sr_error = librosa.load(error_path, sr=None)

        # --- KIỂM TRA LỖI KỸ THUẬT TRÊN FILE ERROR ---

        # A. Kiểm tra Clipping (Vỡ tiếng)
        # Nếu có mẫu nào đạt biên độ tuyệt đối > 0.99
        max_amp = np.max(np.abs(y_error))
        if max_amp >= CLIPPING_THRESHOLD:
            result["label"] = "error_clipping"
            result["details"]["max_amplitude"] = float(max_amp)
            return result

        # B. Tính năng lượng trung bình (RMS - Root Mean Square)
        rms_clean = np.sqrt(np.mean(y_clean**2))
        rms_error = np.sqrt(np.mean(y_error**2))
        
        result["details"]["rms_clean"] = float(rms_clean)
        result["details"]["rms_error"] = float(rms_error)

        # C. Kiểm tra Âm lượng quá nhỏ (Low Volume)
        if rms_error < LOW_VOLUME_RMS:
            result["label"] = "error_low_volume"
            return result

        # D. So sánh chênh lệch năng lượng (Noise Spike)
        # Nếu file lỗi ồn hơn file sạch đáng kể
        if rms_clean > 0: # Tránh chia cho 0
            ratio = rms_error / rms_clean
            result["details"]["energy_ratio"] = float(ratio)
            
            if ratio > NOISE_DIFF_RATIO:
                result["label"] = "error_noise_spike"
                return result

        # E. Fallback: Nếu không dính lỗi kỹ thuật, ta tạm gán là lỗi phát âm
        # (Việc xác nhận lỗi phát âm chính xác sẽ do vector embedding đảm nhiệm sau này)
        result["label"] = "error_pronunciation"
        
        return result

    except Exception as e:
        logging.error(f"Lỗi khi phân tích tín hiệu audio: {e}")
        # Trả về mặc định nếu lỗi
        return result