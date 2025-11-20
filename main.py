# main.py
from dotenv import load_dotenv
import os
from src.utils import file_handler, fcpxml_parser

def run_pipeline():
    load_dotenv()
    # Lấy cấu hình từ .env
    raw_video = os.getenv("RAW_VIDEO_PATH")
    edited_video = os.getenv("EDITED_VIDEO_PATH")
    fcpxml_file = os.getenv("FCPXML_PATH")

    # Gọi các hàm đã được module hóa
    time_map = fcpxml_parser.parse_fcpxml_to_time_map(fcpxml_file)
    
    # ... các bước tiếp theo
    print("Pipeline đã chạy với cấu trúc khung.")

if __name__ == "__main__":
    run_pipeline()