# scripts/organize_media_files.py

import os
import shutil
import glob
import argparse
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

def organize_files(source_dir: str, output_dir: str):
    """
    Quét thư mục nguồn, tìm các session media, và sắp xếp chúng lại vào thư mục
    đầu ra theo đúng cấu trúc yêu cầu của pipeline.
    """
    logging.info(f"Bắt đầu quét thư mục nguồn: {source_dir}")
    logging.info(f"Dữ liệu đã sắp xếp sẽ được lưu tại: {output_dir}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Sử dụng glob để tìm tất cả các file video trong thư mục gốc.
    # Chúng ta sẽ lọc ra các file "edited" từ danh sách này.
    source_videos = glob.glob(os.path.join(source_dir, "*.mp4"))
    
    edited_files = [f for f in source_videos if '_edited' in f.lower() or '_raw' not in f.lower()]
    
    if not edited_files:
        logging.warning("Không tìm thấy file video 'edited' nào trong thư mục nguồn.")
        return

    logging.info(f"Tìm thấy {len(edited_files)} file 'edited' tiềm năng để xử lý.")
    
    success_count = 0
    error_count = 0

    for edited_path in edited_files:
        try:
            logging.info(f"\n--- Đang xử lý: {os.path.basename(edited_path)} ---")
            
            # 1. Trích xuất Session ID từ tên file edited
            # Giả định tên file có dạng {Session-ID}_edited.mp4 hoặc {Session-ID}.mp4
            session_id = os.path.basename(edited_path).lower().replace('_edited.mp4', '').replace('.mp4', '')
            logging.info(f"   - Session ID được xác định: {session_id}")
            
            # 2. Tạo thư mục đích cho session
            session_output_dir = os.path.join(output_dir, session_id)
            os.makedirs(session_output_dir, exist_ok=True)
            
            # --- Xử lý file EDITED ---
            edited_dest_path = os.path.join(session_output_dir, f"{session_id}_edited.mp4")
            shutil.copy2(edited_path, edited_dest_path)
            logging.info(f"   - Đã sao chép EDITED: {edited_dest_path}")
            
            # --- Xử lý file RAW ---
            raw_source_dir = os.path.join(source_dir, session_id)
            if not os.path.isdir(raw_source_dir):
                raise FileNotFoundError(f"Không tìm thấy thư mục con cho file raw: {raw_source_dir}")
            
            # Tìm bất kỳ file video nào trong thư mục raw
            raw_video_files = glob.glob(os.path.join(raw_source_dir, "*.mp4")) + glob.glob(os.path.join(raw_source_dir, "*.mov"))
            if not raw_video_files:
                raise FileNotFoundError(f"Không tìm thấy file video raw nào trong: {raw_source_dir}")
                
            raw_source_path = raw_video_files[0] # Lấy file đầu tiên tìm được
            raw_dest_path = os.path.join(session_output_dir, f"{session_id}_raw.mp4")
            shutil.copy2(raw_source_path, raw_dest_path)
            logging.info(f"   - Đã sao chép RAW: {raw_dest_path}")
            
            # --- Xử lý file FCPXML ---
            # Tìm thư mục .fcpxmld
            fcpxmld_dirs = glob.glob(os.path.join(raw_source_dir, "*.fcpxmld"))
            if not fcpxmld_dirs:
                raise FileNotFoundError(f"Không tìm thấy thư mục *.fcpxmld trong: {raw_source_dir}")
            
            fcpxml_source_path = os.path.join(fcpxmld_dirs[0], "Info.fcpxml")
            if not os.path.exists(fcpxml_source_path):
                raise FileNotFoundError(f"Không tìm thấy file Info.fcpxml trong: {fcpxmld_dirs[0]}")
            
            fcpxml_dest_path = os.path.join(session_output_dir, f"{session_id}.fcpxml")
            shutil.copy2(fcpxml_source_path, fcpxml_dest_path)
            logging.info(f"   - Đã sao chép FCPXML: {fcpxml_dest_path}")

            success_count += 1
            
        except FileNotFoundError as e:
            logging.error(f"LỖI xử lý session '{session_id}': {e}. Bỏ qua session này.")
            error_count += 1
        except Exception as e:
            logging.error(f"LỖI không xác định khi xử lý session '{session_id}': {e}")
            error_count += 1
            
    logging.info(f"\n--- HOÀN TẤT ---")
    logging.info(f"Thành công: {success_count} sessions")
    logging.info(f"Thất bại: {error_count} sessions")


if __name__ == "__main__":
    # Sử dụng argparse để nhận tham số từ dòng lệnh
    parser = argparse.ArgumentParser(description="Sắp xếp lại các file media từ Media Team vào cấu trúc pipeline chuẩn.")
    parser.add_argument("source_directory", type=str, help="Đường dẫn đến thư mục gốc chứa dữ liệu lộn xộn (ví dụ: 'PT Test AI(đã chỉnh sửa)').")
    parser.add_argument("output_directory", type=str, help="Đường dẫn đến thư mục sẽ chứa dữ liệu đã được sắp xếp (ví dụ: './data/Batch_01').")
    
    args = parser.parse_args()
    
    # Chuyển đổi đường dẫn thành đường dẫn tuyệt đối để tránh lỗi
    abs_source_dir = os.path.abspath(args.source_directory)
    abs_output_dir = os.path.abspath(args.output_directory)

    organize_files(abs_source_dir, abs_output_dir)