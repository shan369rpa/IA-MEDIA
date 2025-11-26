# tests/conftest.py

import pytest
import os
import torch
import torchaudio
import numpy as np
from scipy.io.wavfile import write as write_wav # Import hàm ghi file WAV từ scipy

@pytest.fixture(scope="session")
def dummy_media_files(tmp_path_factory):
    """
    Tạo ra các file video và audio giả để làm đầu vào cho các bài test.
    `tmp_path_factory` là một fixture của pytest để tạo thư mục tạm.
    """
    source_dir = tmp_path_factory.mktemp("source_data")
    
    # Tạo tín hiệu audio giả
    sample_rate = 16000
    # Tạo tín hiệu sine 1 giây ở tần số 440Hz
    t = np.linspace(0., 1., sample_rate)
    amplitude = np.iinfo(np.int16).max * 0.5
    data = amplitude * np.sin(2. * np.pi * 440. * t)
    
    dummy_audio_path = source_dir / "dummy_audio.wav"

    # --- SỬA ĐỔI CHÍNH NẰM Ở ĐÂY ---
    # Sử dụng scipy để ghi file WAV, cực kỳ đáng tin cậy
    write_wav(dummy_audio_path, sample_rate, data.astype(np.int16))
    
    # Tạo file video câm giả từ file audio
    dummy_video_path = source_dir / "dummy_video.mp4"
    ffmpeg_cmd = [
        "ffmpeg", "-y", # -y để tự động ghi đè file
        "-i", str(dummy_audio_path),
        "-f", "lavfi", "-i", "testsrc=size=128x72:rate=10:duration=5",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        str(dummy_video_path)
    ]
    # Chạy lệnh trong im lặng để không làm rối output của pytest
    os.system(" ".join(ffmpeg_cmd) + " > /dev/null 2>&1")
    
    return {
        "source_dir": source_dir,
        "video_path": str(dummy_video_path),
        "audio_path": str(dummy_audio_path)
    }