# tests/conftest.py

import pytest
import os
import torch
import torchaudio

@pytest.fixture(scope="session")
def dummy_media_files(tmp_path_factory):
    """
    Tạo ra các file video và audio giả để làm đầu vào cho các bài test.
    `tmp_path_factory` là một fixture của pytest để tạo thư mục tạm.
    """
    source_dir = tmp_path_factory.mktemp("source_data")
    
    # Tạo file audio giả
    sample_rate = 16000
    dummy_signal = torch.sin(2 * torch.pi * 440 * torch.linspace(0, 1, sample_rate)) # Âm thanh 1 giây
    dummy_audio_path = source_dir / "dummy_audio.wav"
    torchaudio.save(dummy_audio_path, dummy_signal.unsqueeze(0), sample_rate)
    
    # Tạo file video câm giả từ file audio
    dummy_video_path = source_dir / "dummy_video.mp4"
    ffmpeg_cmd = [
        "ffmpeg", "-f", "lavfi", "-i", f"anullsrc=r={sample_rate}:cl=mono",
        "-f", "lavfi", "-i", "testsrc=size=128x72:rate=10",
        "-i", str(dummy_audio_path),
        "-c:v", "libx264", "-c:a", "aac",
        "-t", "5", # Video dài 5 giây
        "-shortest",
        str(dummy_video_path)
    ]
    os.system(" ".join(ffmpeg_cmd))
    
    return {
        "source_dir": source_dir,
        "video_path": str(dummy_video_path)
    }