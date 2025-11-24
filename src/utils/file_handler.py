# src/utils/file_handler.py

import os
import subprocess
import logging
import re
from pydub import AudioSegment # Cần cho việc cắt chunk, có thể dùng lại cho hàm get_duration nếu muốn

def extract_audio(video_path: str, workspace_dir: str) -> str | None:
    """
    Trích xuất audio từ một file video và lưu dưới dạng WAV, mono, 16kHz.
    
    Returns:
        str | None: Đường dẫn đến file audio đã trích xuất, hoặc None nếu có lỗi.
    """
    if not os.path.exists(video_path):
        logging.error(f"File video không tồn tại: {video_path}")
        return None

    try:
        audio_dir = os.path.join(workspace_dir, "extracted_audios")
        os.makedirs(audio_dir, exist_ok=True)
        
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        audio_output_path = os.path.join(audio_dir, f"{base_name}.wav")

        if os.path.exists(audio_output_path):
            logging.info(f"File audio đã tồn tại, bỏ qua trích xuất: {audio_output_path}")
            return audio_output_path
        
        logging.info(f"Đang trích xuất audio từ: {video_path}")
        command = [
            'ffmpeg', '-i', video_path,
            '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
            '-hide_banner', '-loglevel', 'error',
            audio_output_path
        ]
        subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info(f"Trích xuất audio thành công: {audio_output_path}")
        return audio_output_path
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Lỗi khi chạy ffmpeg cho file {video_path}: {e.stderr}")
        return None
    except Exception as e:
        logging.error(f"Lỗi không xác định khi trích xuất audio: {e}")
        return None


def extract_audio_pair(raw_video_path: str, edited_video_path: str, workspace_dir: str) -> tuple[str | None, str | None]:
    """Trích xuất audio cho cả 2 file video raw và edited."""
    logging.info("Bắt đầu trích xuất cặp audio...")
    raw_audio_path = extract_audio(raw_video_path, workspace_dir)
    edited_audio_path = extract_audio(edited_video_path, workspace_dir)
    return raw_audio_path, edited_audio_path


# def cut_video_segment(input_video_path: str, output_video_path: str, start_time: float, duration: float):
#     """Sử dụng ffmpeg để cắt một đoạn video từ file gốc."""
#     if os.path.exists(output_video_path):
#         return True # Trả về True nếu file đã tồn tại

#     try:
#         command = [
#             'ffmpeg',
#             '-ss', str(start_time),
#             '-i', input_video_path,
#             '-t', str(duration),
#             '-c:v', 'libx264', '-preset', 'fast', '-crf', '23', # Codec video phổ biến, chất lượng tốt
#             '-c:a', 'aac', '-b:a', '128k', # Codec audio phổ biến
#             '-movflags', '+faststart', # Tối ưu cho web streaming
#             '-hide_banner', '-loglevel', 'error',
#             output_video_path
#         ]
#         subprocess.run(command, check=True, capture_output=True, text=True)
#         return True
#     except subprocess.CalledProcessError as e:
#         logging.error(f"Lỗi khi cắt video {input_video_path}: {e.stderr}")
#         return False
#     except Exception as e:
#         logging.error(f"Lỗi không xác định khi cắt video: {e}")
#         return False


def sanitize_filename(name: str) -> str:
    """Làm sạch một chuỗi để nó trở thành một tên file/thư mục hợp lệ."""
    if not name:
        return ""
    # Chuyển thành chữ thường
    name = name.lower()
    name = re.sub(r'[^\w-]', '', name)
    # Giới hạn độ dài để tránh tên file quá dài trên một số hệ thống file
    return name[:50]
# Thêm import này vào đầu file file_handler.py
from pydub import AudioSegment

# ... (đặt hàm này ở cuối file) ...

def get_audio_duration(audio_path: str) -> float:
    """
    [Cách 1: Dùng Pydub] Lấy độ dài (duration) của một file audio tính bằng giây.
    
    Args:
        audio_path: Đường dẫn đến file audio.
        
    Returns:
        float: Độ dài của audio tính bằng giây. Trả về 0.0 nếu có lỗi.
    """
    try:
        if not os.path.exists(audio_path):
            logging.error(f"File audio không tồn tại để lấy duration: {audio_path}")
            return 0.0
            
        audio = AudioSegment.from_file(audio_path)
        duration_seconds = len(audio) / 1000.0
        return duration_seconds
    except Exception as e:
        logging.error(f"Không thể đọc độ dài file audio bằng Pydub: {audio_path}. Lỗi: {e}")
        return 0.0