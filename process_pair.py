"""
process_pair.py

Kịch bản này là bước đầu tiên trong pipeline IA MEDIA.
Nó thực hiện các công việc cốt lõi sau:
1.  Nhận đầu vào là một cặp video (raw và đã chỉnh sửa).
2.  Trích xuất âm thanh từ cả hai video sang định dạng WAV chuẩn (16kHz -> cần review lại tại sao 16kHz, mono).
3.  Sử dụng OpenAI Whisper để phiên âm file âm thanh đã chỉnh sửa và lấy
    timestamp chính xác cho từng từ.
4.  Dựa trên các timestamp này, cắt ra các cặp audio chunk vi mô (từng từ)
    từ cả hai file âm thanh (sạch và lỗi).
5.  Lưu các cặp chunk này vào một cấu trúc thư mục có tổ chức để chuẩn bị
    cho giai đoạn vector hóa.

Cách chạy:
    python process_pair.py
"""

import os
import subprocess
import whisper
from pydub import AudioSegment
import re
import logging
from dotenv import load_dotenv

load_dotenv() # Tải các biến từ file .env

# Cấu hình logging để hiển thị thông tin rõ ràng
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CẤU HÌNH ---
# Thay đổi các đường dẫn này cho phù hợp với file của bạn
RAW_VIDEO_PATH = os.getenv("RAW_VIDEO_PATH")
EDITED_VIDEO_PATH = os.getenv("EDITED_VIDEO_PATH")

# Thư mục làm việc để chứa các file tạm thời và kết quả
WORKSPACE_DIR = os.getenv("WORKSPACE_DIR")
CHUNK_OUTPUT_DIR = os.path.join(WORKSPACE_DIR, "phonetic_chunks")

# --- CÁC HÀM TIỆN ÍCH ---

def extract_audio(video_path, audio_output_path):
    """
    Trích xuất audio từ file video và chuyển đổi sang định dạng WAV, mono, 16kHz
    sử dụng ffmpeg. Sẽ bỏ qua nếu file audio đã tồn tại.
    """
    if os.path.exists(audio_output_path):
        logging.info(f"File audio đã tồn tại, bỏ qua bước trích xuất: {audio_output_path}")
        return True
    
    logging.info(f"Bắt đầu trích xuất audio từ: {video_path}")
    command = [
        'ffmpeg',
        '-i', video_path,
        '-vn',             # Bỏ qua video
        '-acodec', 'pcm_s16le', # Định dạng WAV chuẩn
        '-ar', '16000',    # Tần số mẫu 16kHz, chuẩn cho các mô hình giọng nói
        '-ac', '1',        # 1 kênh (mono)
        '-hide_banner',    # Ẩn thông tin banner của ffmpeg
        '-loglevel', 'error', # Chỉ hiển thị lỗi
        audio_output_path
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info(f"Đã trích xuất audio thành công: {audio_output_path}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Lỗi khi chạy ffmpeg cho file {video_path}:")
        logging.error(e.stderr)
        return False

def sanitize_filename(word):
    """
    Làm sạch một từ để nó trở thành một tên thư mục/file hợp lệ.
    Chuyển thành chữ thường và loại bỏ các ký tự đặc biệt.
    """
    # Chuyển thành chữ thường
    word = word.lower()
    # Loại bỏ các ký tự không phải là chữ cái, số, hoặc dấu gạch dưới/gạch ngang
    word = re.sub(r'[^a-z0-9\-_]', '', word)
    return word

def main():
    """Hàm chính điều phối toàn bộ quy trình."""
    logging.info("===== BẮT ĐẦU QUY TRÌNH XỬ LÝ CẶP VIDEO =====")

    # --- BƯỚC 0: TẠO THƯ MỤC LÀM VIỆC ---
    os.makedirs(CHUNK_OUTPUT_DIR, exist_ok=True)
    logging.info(f"Thư mục làm việc và đầu ra đã được chuẩn bị tại: {WORKSPACE_DIR}")

    # --- BƯỚC 1: TRÍCH XUẤT AUDIO TỪ VIDEO ---
    base_name_raw = os.path.splitext(os.path.basename(RAW_VIDEO_PATH))[0]
    base_name_edited = os.path.splitext(os.path.basename(EDITED_VIDEO_PATH))[0]
    
    raw_audio_path = os.path.join(WORKSPACE_DIR, f"{base_name_raw}.wav")
    edited_audio_path = os.path.join(WORKSPACE_DIR, f"{base_name_edited}.wav")

    if not extract_audio(RAW_VIDEO_PATH, raw_audio_path): return
    if not extract_audio(EDITED_VIDEO_PATH, edited_audio_path): return

    # --- BƯỚC 2: ĐỒNG BỘ HÓA AUDIO (ALIGNMENT) ---
    # LƯU Ý QUAN TRỌNG: Đây là một bước phức tạp đòi hỏi các thuật toán riêng.
    # Trong bản demo đầu tiên này, chúng ta TẠM GIẢ ĐỊNH rằng hai file audio
    # đã được căn chỉnh tương đối về mặt thời gian (không có sự cắt xén lớn
    # ở đầu hoặc cuối). Chúng ta sẽ cải thiện bước này sau.
    logging.warning("Bỏ qua bước đồng bộ hóa audio trong bản demo này. Giả định hai file đã được căn chỉnh.")
    aligned_raw_audio_path = raw_audio_path 

    # --- BƯỚC 3: PHIÊN ÂM VÀ LẤY WORD-TIMESTAMPS ---
    logging.info("Đang tải mô hình Whisper (có thể mất vài phút cho lần đầu tiên)...")
    model = whisper.load_model("base") # Sử dụng 'base' cho tốc độ, có thể nâng cấp lên 'small'/'medium' để chính xác hơn

    logging.info(f"Bắt đầu phiên âm file audio đã chỉnh sửa: {edited_audio_path}")
    # Chúng ta phiên âm file EDITED vì nó là nguồn "sạch" và thời gian chuẩn xác nhất.
    result = model.transcribe(edited_audio_path, word_timestamps=True)
    logging.info("Phiên âm và lấy timestamp thành công.")

    # --- BƯỚC 4: CẮT VÀ LƯU CÁC CẶP AUDIO CHUNK ---
    logging.info("Đang tải các file audio vào bộ nhớ để cắt...")
    try:
        clean_audio = AudioSegment.from_wav(edited_audio_path)
        error_audio = AudioSegment.from_wav(aligned_raw_audio_path)
    except Exception as e:
        logging.error(f"Không thể tải file audio bằng pydub: {e}")
        return

    logging.info("Bắt đầu trích xuất các cặp chunk âm vị...")
    chunk_count = 0
    for segment in result['segments']:
        for word_info in segment['words']:
            word_text = word_info['word'].strip()
            start_time_ms = int(word_info['start'] * 1000) # pydub làm việc với mili giây
            end_time_ms = int(word_info['end'] * 1000)

            # Bỏ qua các từ quá ngắn hoặc không có nội dung
            if (end_time_ms - start_time_ms < 150) or not word_text:
                continue

            sanitized_word = sanitize_filename(word_text)
            if not sanitized_word:
                continue

            # Tạo thư mục cho từng từ nếu chưa có
            word_dir = os.path.join(CHUNK_OUTPUT_DIR, sanitized_word)
            os.makedirs(word_dir, exist_ok=True)

            # Cắt chunk từ audio "sạch" (clean) và "lỗi" (error)
            clean_chunk = clean_audio[start_time_ms:end_time_ms]
            error_chunk = error_audio[start_time_ms:end_time_ms]

            # Tạo tên file duy nhất dựa trên timestamp để tránh ghi đè
            chunk_filename = f"{start_time_ms}_{end_time_ms}.wav"
            
            # Lưu các file chunk
            clean_chunk.export(os.path.join(word_dir, "clean_" + chunk_filename), format="wav")
            error_chunk.export(os.path.join(word_dir, "error_" + chunk_filename), format="wav")
            chunk_count += 1

    logging.info(f"Hoàn tất! Đã trích xuất thành công {chunk_count} cặp chunk.")
    logging.info(f"Kết quả được lưu tại: {CHUNK_OUTPUT_DIR}")
    logging.info("===== KẾT THÚC QUY TRÌNH =====")


if __name__ == "__main__":
    main()