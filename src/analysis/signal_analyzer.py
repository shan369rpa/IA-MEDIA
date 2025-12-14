# src/analysis/signal_analyzer.py

import librosa
import numpy as np
import logging

class SignalAnalyzer:
    def __init__(self, sample_rate=16000):
        self.sr = sample_rate

    def analyze_chunk(self, audio_path: str) -> dict:
        """
        Phân tích tín hiệu âm thanh để tìm các lỗi kỹ thuật.
        Trả về dictionary chứa các cờ lỗi và thông số.
        """
        result = {
            "is_clipping": False,
            "is_silence": False,
            "is_noise_spike": False,
            "rms_energy": 0.0,
            "max_amplitude": 0.0
        }

        try:
            # Tải audio (librosa load nhanh hơn cho phân tích tín hiệu)
            y, _ = librosa.load(audio_path, sr=self.sr)
            
            if len(y) == 0: return result

            # 1. Phân tích Clipping (Vỡ tiếng)
            max_amp = np.max(np.abs(y))
            result["max_amplitude"] = float(max_amp)
            # Ngưỡng clipping thường gần 1.0 (nếu float) hoặc 32767 (nếu int16)
            # Ở đây librosa load ra float [-1, 1]
            if max_amp >= 0.99: 
                result["is_clipping"] = True

            # 2. Phân tích Năng lượng (RMS)
            rms = librosa.feature.rms(y=y)[0]
            avg_rms = float(np.mean(rms))
            result["rms_energy"] = avg_rms

            # 3. Phân tích Khoảng lặng (Silence)
            # Ngưỡng im lặng tùy thuộc vào môi trường, ví dụ dưới 0.005
            if avg_rms < 0.005:
                result["is_silence"] = True

            # 4. Phân tích Noise Spike (Tiếng ồn đột ngột)
            # Nếu năng lượng đỉnh (peak) lớn gấp nhiều lần năng lượng trung bình
            if avg_rms > 0 and (np.max(rms) / avg_rms) > 5.0:
                result["is_noise_spike"] = True

        except Exception as e:
            logging.error(f"Lỗi phân tích tín hiệu {audio_path}: {e}")
        
        return result

# --- HÀM MODULE-LEVEL ĐƯỢC GỌI TỪ CHUNKER.PY ---

def analyze_audio_defects(clean_chunk_path: str, error_chunk_path: str) -> dict:
    """
    So sánh file clean và file error (raw) để xác định các lỗi cụ thể.
    Hàm này được gọi trực tiếp từ chunker.py.
    
    Returns:
        dict: Chứa các thông tin phân tích và cờ báo lỗi.
    """
    analyzer = SignalAnalyzer()
    
    # 1. Phân tích riêng lẻ từng file
    # File clean (đã sửa) dùng làm chuẩn
    clean_stats = analyzer.analyze_chunk(clean_chunk_path)
    # File error (raw) là file cần tìm lỗi
    error_stats = analyzer.analyze_chunk(error_chunk_path)
    
    analysis_report = {
        "rms_clean": clean_stats["rms_energy"],
        "rms_error": error_stats["rms_energy"],
        "max_amp_error": error_stats["max_amplitude"],
        "detected_defects": [] # Danh sách các lỗi phát hiện được
    }

    # 2. Logic so sánh để gán nhãn lỗi
    
    # Lỗi A: Clipping (Vỡ tiếng)
    # Chỉ đánh dấu lỗi nếu file Raw bị vỡ tiếng còn file Clean thì không (hoặc đỡ hơn)
    if error_stats["is_clipping"] and not clean_stats["is_clipping"]:
        analysis_report["detected_defects"].append("error_clipping")
        
    # Lỗi B: Noise Spike (Tiếng động lạ đột ngột: ho, va đập)
    # Nếu file Raw có gai nhiễu mà file Clean không có -> Editor đã cắt bỏ nó
    if error_stats["is_noise_spike"] and not clean_stats["is_noise_spike"]:
        analysis_report["detected_defects"].append("error_noise_spike")

    # Lỗi C: Low Volume (Âm lượng quá nhỏ)
    # Nếu năng lượng file Raw quá nhỏ so với ngưỡng chuẩn (ví dụ 0.02)
    # Và nhỏ hơn đáng kể so với file Clean (trường hợp editor đã gain volume lên)
    if error_stats["rms_energy"] < 0.02 and clean_stats["rms_energy"] > 0.05:
        analysis_report["detected_defects"].append("error_low_volume")

    # Lỗi D: Silence (Khoảng lặng bất thường)
    if error_stats["is_silence"] and not clean_stats["is_silence"]:
        analysis_report["detected_defects"].append("error_missing_audio")

    # Nếu không phát hiện lỗi kỹ thuật cụ thể nào, nhưng đây là cặp clean/error
    # Có thể để trống hoặc đánh dấu là 'potential_pronunciation_issue' ở bước vector hóa sau này
    
    return analysis_report