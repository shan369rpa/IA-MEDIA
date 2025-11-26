# tests/test_analysis_pipeline.py
import os
from src.utils import file_handler
from src.analysis import transcriber
import pytest

# --- Test cho file_handler.py ---
def test_extract_audio(dummy_media_files, tmp_path):
    workspace_dir = tmp_path
    video_path = dummy_media_files["video_path"]
    audio_path = file_handler.extract_audio(video_path, workspace_dir)
    assert audio_path is not None
    assert os.path.exists(audio_path)

# def test_cut_video_segment(dummy_media_files, tmp_path):
#     video_path = dummy_media_files["video_path"]
#     output_path = tmp_path / "cut_segment.mp4"
#     success = file_handler.cut_video_segment(
#         input_video_path=video_path,
#         output_video_path=str(output_path),
#         start_time=1.0,
#         duration=2.0
#     )
#     assert success is True
#     assert os.path.exists(output_path)

# --- Test cho transcriber.py ---
def test_get_word_timestamps_mocked(mocker, dummy_media_files):
    """
    Kiểm tra transcriber bằng cách "giả mạo" (mock) hàm `transcribe`.
    """
    # 1. Chuẩn bị kết quả giả lập
    mock_result = {
        'segments': [{
            'words': [
                {'word': 'This', 'start': 0.0, 'end': 0.5},
                {'word': 'is', 'start': 0.6, 'end': 0.8},
                {'word': 'a', 'start': 0.9, 'end': 1.0},
                {'word': 'test', 'start': 1.1, 'end': 1.5}
            ]
        }]
    }

    # 2. Mock hàm `transcribe` của model Whisper
    # Chúng ta giả lập rằng model đã được tải và `transcribe` là một phương thức của nó
    mock_model = mocker.MagicMock()
    mock_model.transcribe.return_value = mock_result
    mocker.patch("whisper.load_model", return_value=mock_model)

    # 3. Gọi hàm của chúng ta
    audio_path = dummy_media_files["audio_path"]
    word_timestamps = transcriber.get_word_timestamps(audio_path)
    
    # 4. Kiểm tra kết quả
    assert word_timestamps is not None
    assert len(word_timestamps) == 4
    assert word_timestamps[0]['word'] == 'This'
    # Đảm bảo hàm `transcribe` đã được gọi với đúng tham số
    mock_model.transcribe.assert_called_once_with(audio_path, word_timestamps=True)