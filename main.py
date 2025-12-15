# main.py
# ==============================================================================
# BƯỚC 0: CẤU HÌNH MÔI TRƯỜNG - PHẢI LÀ ĐIỀU ĐẦU TIÊN ĐƯỢC THỰC HIỆN
# ==============================================================================
import sys
import os
# Thêm đường dẫn gốc vào sys.path một cách an toàn
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from src.utils.environment import setup_environment
setup_environment()
# ==============================================================================

# BÂY GIỜ MỚI IMPORT CÁC THƯ VIỆN CÒN LẠI
import glob
import logging
from dotenv import load_dotenv

from src.utils import file_handler, fcpxml_parser
from src.analysis import transcriber, chunker
# Di chuyển cấu hình logging ra ngoài để có thể tái sử dụng
# force=True rất quan trọng khi chạy trong môi trường như Colab, nơi logging có thể đã được cấu hình trước
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s', force=True)

def process_single_session(fcpxml_path: str, source_dir: str, workspace_dir: str) -> bool:
    """
    Xử lý một session (bài pháp thoại) duy nhất, bao gồm 1 cặp video và 1 file FCPXML.

    Returns:
        bool: True nếu xử lý thành công, False nếu có lỗi.
    """
    try:
        # 1. Trích xuất Session ID từ tên file FCPXML
        session_id = os.path.splitext(os.path.basename(fcpxml_path))[0]
        logging.info(f"--- PROCESSING SESSION: {session_id} ---")

        # 2. Xây dựng đường dẫn và kiểm tra sự tồn tại của các file video
        raw_video_path = os.path.join(source_dir, f"{session_id}_raw.mp4") # Giả định phần mở rộng là .mp4
        edited_video_path = os.path.join(source_dir, f"{session_id}_edited.mp4")

        if not os.path.exists(raw_video_path):
            logging.warning(f"SKIPPING: Raw video file not found at '{raw_video_path}'")
            return False
        if not os.path.exists(edited_video_path):
            logging.warning(f"SKIPPING: Edited video file not found at '{edited_video_path}'")
            return False

        # 3. Phân tích FCPXML để tạo bản đồ thời gian
        logging.info("Step 1/5: Parsing FCPXML file...")
        time_map = fcpxml_parser.parse_fcpxml_to_time_map(fcpxml_path)
        if not time_map:
            logging.error("Failed to create time map. Skipping session.")
            return False

        # 4. Trích xuất audio từ video
        logging.info("Step 2/5: Extracting audio from videos...")
        raw_audio_path, edited_audio_path = file_handler.extract_audio_pair(
            raw_video_path, edited_video_path, workspace_dir
        )
        if not all([raw_audio_path, edited_audio_path]):
            logging.error("Failed to extract audio. Skipping session.")
            return False

        # 5. Phiên âm audio đã chỉnh sửa để lấy word-timestamps
        logging.info("Step 3/5: Transcribing audio with Whisper (this may take a while)...")
        word_timestamps = transcriber.get_word_timestamps(edited_audio_path)
        if not word_timestamps:
            logging.error("Failed to get word timestamps. Skipping session.")
            return False

        # 6. Cắt và lưu các cặp audio/video chunk
        logging.info("Step 4/5: Chunking media files...")
        dataset_version = "tnh_speech_v0.1" # Có thể đưa ra file config sau
        output_dir = os.path.join(workspace_dir, "datasets", dataset_version)
        
        chunk_count = chunker.create_and_save_chunks(
            clean_audio_path=edited_audio_path,
            error_audio_path=raw_audio_path,
            clean_video_path=edited_video_path,
            error_video_path=raw_video_path,
            time_map=time_map,
            word_timestamps=word_timestamps,
            output_dir=output_dir,
            source_video_name=session_id
        )
        
        logging.info(f"Step 5/5: Session processing complete. Created {chunk_count} chunk pairs.")
        logging.info(f"--- FINISHED SESSION: {session_id} ---")
        return True

    except Exception as e:
        logging.exception(f"An unexpected and critical error occurred while processing session defined by {fcpxml_path}.")
        return False


def main_pipeline(source_dir: str, workspace_dir: str):
    """
    Hàm chính điều phối pipeline cho cả một thư mục (batch).
    Nó sẽ tự động tìm các session dựa trên các file .fcpxml.
    """
    logging.info(f"===== STARTING CORE ANALYSIS PIPELINE ON DIRECTORY: {source_dir} =====")
    
    # Tìm tất cả các file FCPXML trong thư mục nguồn để xác định các session
    fcpxml_files = glob.glob(os.path.join(source_dir, "*.fcpxml"))
    
    if not fcpxml_files:
        logging.error(f"No .fcpxml files found in '{source_dir}'. Nothing to process. Stopping.")
        return

    total_sessions = len(fcpxml_files)
    success_count = 0
    
    logging.info(f"Found {total_sessions} session(s) to process: {[os.path.basename(f) for f in fcpxml_files]}")

    for i, fcpxml_path in enumerate(fcpxml_files):
        logging.info(f"\n>>> Processing session {i+1}/{total_sessions}...")
        success = process_single_session(fcpxml_path, source_dir, workspace_dir)
        if success:
            success_count += 1
            
    logging.info(f"\n===== PIPELINE FINISHED: Successfully processed {success_count}/{total_sessions} sessions. =====")


if __name__ == '__main__':
    # Phần này dùng để chạy test cục bộ trong Codespaces
    # Nó sẽ không được gọi khi chạy từ Colab
    print("Running main.py in local test mode...")
    load_dotenv()
    
    # Giả định bạn có một thư mục `data/Batch_01` để test
    # và các file bên trong tuân thủ quy ước đặt tên.
    TEST_SOURCE_DIR = "./data/Batch_01" 
    TEST_WORKSPACE_DIR = "./workspace"

    if os.path.exists(TEST_SOURCE_DIR):
        # Tạo các thư mục cần thiết trước khi chạy
        os.makedirs(TEST_WORKSPACE_DIR, exist_ok=True)
        main_pipeline(source_dir=TEST_SOURCE_DIR, workspace_dir=TEST_WORKSPACE_DIR)
    else:
        print(f"Test directory not found: {TEST_SOURCE_DIR}")
        print("Please create it and add test data (raw/edited video, fcpxml) to run locally.")