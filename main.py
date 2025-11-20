# main.py

import os
from dotenv import load_dotenv
import logging

# Giả định chúng ta sẽ tạo các module này
from src.utils import file_handler, fcpxml_parser
from src.analysis import transcriber, chunker

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main_pipeline():
    """
    Hàm chính điều phối toàn bộ pipeline:
    Video & FCPXML -> Audio Chunks.
    """
    logging.info("===== BẮT ĐẦU PIPELINE PHÂN TÍCH LÕI =====")

    # 1. Tải cấu hình từ file .env
    load_dotenv()
    raw_video_path = os.getenv("RAW_VIDEO_PATH")
    edited_video_path = os.getenv("EDITED_VIDEO_PATH")
    fcpxml_path = os.getenv("FCPXML_PATH")
    workspace_dir = os.getenv("WORKSPACE_DIR")

    if not all([raw_video_path, edited_video_path, fcpxml_path, workspace_dir]):
        logging.error("Thiếu cấu hình trong file .env. Vui lòng kiểm tra các biến: RAW_VIDEO_PATH, EDITED_VIDEO_PATH, FCPXML_PATH, WORKSPACE_DIR.")
        return

    logging.info("Cấu hình đã được tải thành công.")

    # 2. Phân tích FCPXML để tạo bản đồ thời gian
    time_map = fcpxml_parser.parse_fcpxml_to_time_map(fcpxml_path)
    if not time_map:
        logging.error("Không thể tạo bản đồ thời gian từ file FCPXML. Dừng pipeline.")
        return

    # 3. Trích xuất audio từ video
    # Chúng ta sẽ cần tạo module file_handler với hàm này
    raw_audio_path, edited_audio_path = file_handler.extract_audio_pair(
        raw_video_path, edited_video_path, workspace_dir
    )
    if not all([raw_audio_path, edited_audio_path]):
        logging.error("Lỗi khi trích xuất audio. Dừng pipeline.")
        return

    # 4. Phiên âm audio đã chỉnh sửa để lấy word-timestamps
    # Chúng ta sẽ cần tạo module transcriber với hàm này
    word_timestamps = transcriber.get_word_timestamps(edited_audio_path)
    if not word_timestamps:
        logging.error("Không thể lấy được word timestamps từ Whisper. Dừng pipeline.")
        return

    # 5. Cắt và lưu các cặp audio chunk
    # Chúng ta sẽ cần tạo module chunker với hàm này
    chunk_count = chunker.create_and_save_chunks(
        clean_audio_path=edited_audio_path,
        error_audio_path=raw_audio_path, # Giả định file raw đã được align
        time_map=time_map,
        word_timestamps=word_timestamps,
        output_dir=os.path.join(workspace_dir, "phonetic_chunks")
    )

    if chunk_count > 0:
        logging.info(f"Hoàn tất! Đã tạo và lưu thành công {chunk_count} cặp audio chunk.")
    else:
        logging.warning("Pipeline đã chạy xong nhưng không tạo ra được chunk nào. Vui lòng kiểm tra lại dữ liệu đầu vào và log.")

    logging.info("===== KẾT THÚC PIPELINE PHÂN TÍCH LÕI =====")


if __name__ == "__main__":
    main_pipeline()