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