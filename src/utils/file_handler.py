# src/utils/file_handler.py

import os
import subprocess
import logging
import re

# ... (Hàm sanitize_filename giữ nguyên) ...
def sanitize_filename(name: str) -> str:
    if not name: return ""
    name = name.lower()
    name = re.sub(r'[^\w-]', '', name)
    return name[:50]

def extract_audio(video_path: str, workspace_dir: str) -> str | None:
    # ... (Nội dung hoàn chỉnh của hàm này như đã cung cấp trước đó) ...
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
            'ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
            '-hide_banner', '-loglevel', 'error', audio_output_path
        ]
        subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info(f"Trích xuất audio thành công: {audio_output_path}")
        return audio_output_path
    except Exception as e:
        logging.error(f"Lỗi khi trích xuất audio: {e}")
        return None

def extract_audio_pair(raw_video_path: str, edited_video_path: str, workspace_dir: str) -> tuple[str | None, str | None]:
    logging.info("Bắt đầu trích xuất cặp audio...")
    raw_audio = extract_audio(raw_video_path, workspace_dir)
    edited_audio = extract_audio(edited_video_path, workspace_dir)
    return raw_audio, edited_audio

def cut_video_segment(input_video_path: str, output_video_path: str, start_time: float, duration: float) -> bool:
    # ... (Nội dung hoàn chỉnh của hàm này như đã cung cấp trước đó) ...
    if os.path.exists(output_video_path): return True
    try:
        command = [
            'ffmpeg', '-ss', str(start_time), '-i', input_video_path, '-t', str(duration),
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23', '-c:a', 'aac', '-b:a', '128k',
            '-movflags', '+faststart', '-hide_banner', '-loglevel', 'error', output_video_path
        ]
        subprocess.run(command, check=True, capture_output=True, text=True)
        return True
    except Exception as e:
        logging.error(f"Lỗi khi cắt video: {e}")
        return False