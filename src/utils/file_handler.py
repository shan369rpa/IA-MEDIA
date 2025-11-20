# src/utils/file_handler.py
import os
import subprocess
import re

def extract_audio(video_path, audio_output_path):
    print(f"[Giả lập] Đang trích xuất audio từ {video_path}...")
    # Code ffmpeg sẽ nằm ở đây
    pass

def extract_audio_pair(raw_video_path, edited_video_path, workspace_dir):
    """Trích xuất audio cho cả 2 file video."""
    # ... Viết logic để gọi hàm extract_audio cho cả 2 file ...
    # Trả về đường dẫn của 2 file audio đã được trích xuất
    pass
    return None, None

def sanitize_filename(name: str) -> str:
    """
    Làm sạch một chuỗi để nó trở thành một tên thư mục/file hợp lệ.
    """
    name = name.lower()
    # Loại bỏ các ký tự đặc biệt, chỉ giữ lại chữ cái, số, và dấu gạch dưới/gạch ngang
    name = re.sub(r'[^\w-]', '', name)
    # Giới hạn độ dài để tránh tên file quá dài
    return name[:50]