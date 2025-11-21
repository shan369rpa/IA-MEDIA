# tests/test_analysis_pipeline.py

import os
from src.utils import file_handler
from src.analysis import transcriber # Cần mock transcriber
import pytest

# --- Test cho file_handler.py ---

def test_extract_audio(dummy_media_files, tmp_path):
    """Kiểm tra chức năng trích xuất audio."""
    workspace_dir = tmp_path
    video_path = dummy_media_files["video_path"]
    
    audio_path = file_handler.extract_audio(video_path, workspace_dir)
    
    assert audio_path is not None
    assert os.path.exists(audio_path)
    assert audio_path.endswith(".wav")

def test_cut_video_segment(dummy_media_files, tmp_path):
    """Kiểm tra chức năng cắt video."""
    video_path = dummy_media_files["video_path"]
    output_path = tmp_path / "cut_segment.mp4"
    
    success = file_handler.cut_video_segment(
        input_video_path=video_path,
        output_video_path=str(output_path),
        start_time=1.0,
        duration=2.0
    )
    
    assert success is True
    assert os.path.exists(output_path)
    # TODO: Có thể dùng ffprobe để kiểm tra độ dài video cắt ra có đúng là 2 giây không

# --- Test cho transcriber.py ---

# Việc test transcriber khó hơn vì nó phụ thuộc vào model Whisper nặng.
# Chúng ta sẽ sử dụng kỹ thuật "mocking" để giả lập kết quả trả về của Whisper.
# Cần cài đặt: pip install pytest-mock

def test_get_word_timestamps_mocked(mocker, dummy_media_files):
    """
    Kiểm tra transcriber bằng cách "giả mạo" (mock) model Whisper.
    Chúng ta không muốn tải model thật chỉ để chạy unit test.
    """
    # 1. Giả lập các hàm của Whisper
    mock_load_model = mocker.patch("whisper.load_model", return_value="dummy_model")
    mock_load_audio = mocker.patch("whisper.load_audio", return_value="dummy_audio")
    
    mock_decode_result = {"text": "This is a test."}
    mock_decode = mocker.patch("whisper.decode", return_value=mock_decode_result)
    
    mock_align_result = {
        "word_segments": [
            {'word': 'This', 'start': 0.0, 'end': 0.5},
            {'word': 'is', 'start': 0.6, 'end': 0.8},
            {'word': 'a', 'start': 0.9, 'end': 1.0},
            {'word': 'test', 'start': 1.1, 'end': 1.5}
        ]
    }
    mock_align = mocker.patch("whisper.align", return_value=mock_align_result)

    # 2. Gọi hàm của chúng ta
    audio_path = str(dummy_media_files["source_dir"] / "dummy_audio.wav") # Giả sử có file audio
    word_timestamps = transcriber.get_word_timestamps(audio_path)
    
    # 3. Kiểm tra kết quả
    assert mock_load_model.called_once() # Đảm bảo model được gọi để tải
    assert word_timestamps is not None
    assert len(word_timestamps) == 4
    assert word_timestamps[0]['word'] == 'This'