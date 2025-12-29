# ingest.py (Refactored for Robustness and Performance)

import os
import glob
import logging
from dotenv import load_dotenv
import numpy as np
from pydub import AudioSegment
from tqdm import tqdm
import json

from src.utils import file_handler, fcpxml_parser
from src.analysis import transcriber, chunker
from src.ai import vectorizer
from src.database import db_manager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s', force=True)

def process_and_ingest_session(fcpxml_path: str, workspace_dir: str):
    """
    Hàm này xử lý MỘT session duy nhất từ đầu đến cuối,
    quản lý kết nối CSDL của riêng nó.
    """
    session_id = os.path.splitext(os.path.basename(fcpxml_path))[0]
    logging.info(f"\n--- Processing Session: {session_id} ---")
    
    conn = None # Khởi tạo conn là None
    try:
        # --- [PHẦN XỬ LÝ NẶNG - KHÔNG CẦN KẾT NỐI DB] ---
        
        # 1. Phân tích FCPXML
        logging.info("Step 1/4: Parsing FCPXML...")
        analysis_data = fcpxml_parser.extract_events_and_map(fcpxml_path)
        time_map = analysis_data["time_map"]
        edit_events = analysis_data["edit_events"]
        if not edit_events:
            logging.warning("No edit events found in FCPXML. Skipping.")
            return

        # 2. Chuẩn bị Audio
        logging.info("Step 2/4: Preparing audio files...")
        source_dir = os.path.dirname(fcpxml_path)
        raw_video_path = os.path.join(source_dir, f"{session_id}_raw.mp4")
        edited_video_path = os.path.join(source_dir, f"{session_id}_edited.mp4")
        raw_audio_path, edited_audio_path = file_handler.extract_audio_pair(
            raw_video_path, edited_video_path, workspace_dir
        )
        clean_audio = AudioSegment.from_wav(edited_audio_path)
        error_audio = AudioSegment.from_wav(raw_audio_path)

        # 3. Vector hóa các Edit Events (Bước tốn thời gian nhất)
        logging.info(f"Step 3/4: Processing {len(edit_events)} edit events (Chunking & Embedding)...")
        embedding_model = vectorizer.load_embedding_model() # Tải model
        output_chunk_dir = os.path.join(workspace_dir, "event_chunks")
        events_to_insert = []

        for event in tqdm(edit_events, desc=f"Processing Events for {session_id}"):
            clean_path, error_path = chunker.chunk_event(
                event, clean_audio, error_audio, time_map, output_chunk_dir, session_id
            )
            if clean_path and error_path:
                emb_clean = vectorizer.create_embedding(clean_path, embedding_model)
                emb_error = vectorizer.create_embedding(error_path, embedding_model)
                if emb_clean and emb_error:
                    events_to_insert.append((
                        # Dữ liệu sẽ được chèn
                        # Chúng ta cần source_id, sẽ lấy ở bước sau
                        int(event['start'] * 1000), int(event['end'] * 1000), 'FCPXML', 
                        event['type'], np.array(emb_clean), np.array(emb_error),
                        json.dumps(event['details']), 
                        os.path.relpath(clean_path, workspace_dir),
                        os.path.relpath(error_path, workspace_dir)
                    ))
        
        # --- [PHẦN GHI CSDL - KẾT NỐI NGẮN HẠN] ---
        if not events_to_insert:
            logging.warning("No events were successfully processed to be inserted into DB.")
            return
            
        logging.info("Step 4/4: Connecting to DB and ingesting data...")
        # MỞ KẾT NỐI NGAY TRƯỚC KHI CẦN
        conn = db_manager.get_db_connection()
        if not conn:
            logging.error("Failed to establish DB connection for ingestion.")
            return
        
        # Lấy source_id
        source_id = db_manager.get_or_create_source(conn, session_id)
        if source_id is None:
            logging.error(f"Could not get or create source_id for {session_id}.")
            return
            
        # Thêm source_id vào dữ liệu
        final_events_data = [(source_id, *data) for data in events_to_insert]
        
        # Chèn vào CSDL
        db_manager.insert_edit_events(conn, final_events_data)
        
        logging.info(f"--- Session {session_id} ingested successfully! ---")

    except Exception as e:
        logging.exception(f"A critical error occurred while processing session {session_id}.")
    finally:
        # ĐÓNG KẾT NỐI NGAY SAU KHI DÙNG XONG
        if conn:
            conn.close()
            logging.info("Database connection closed.")


def ingest_main(source_dir: str, workspace_dir: str):
    """Hàm điều phối chính, lặp qua các file FCPXML."""
    logging.info(f"===== STARTING INGESTION PIPELINE V3.0 on: {source_dir} =====")
    
    # Tải các model lớn một lần ở ngoài vòng lặp để tiết kiệm thời gian
    logging.info("Pre-loading AI models...")
    vectorizer.load_embedding_model()
    # (Sau này có thể thêm pre-loading cho WhisperX nếu cần)
    
    fcpxml_files = glob.glob(os.path.join(source_dir, "**", "*.fcpxml"), recursive=True)
    if not fcpxml_files:
        logging.error(f"No .fcpxml files found in '{source_dir}'.")
        return
        
    for fcpxml_path in fcpxml_files:
        process_and_ingest_session(fcpxml_path, workspace_dir)

    logging.info("===== INGESTION PIPELINE FINISHED FOR ALL SESSIONS =====")

if __name__ == "__main__":
    load_dotenv()
    SOURCE_DIR = "D:\\IA MEDIA\\Data\\Batch_02"
    WORKSPACE_DIR = "./workspace"
    ingest_main(source_dir=SOURCE_DIR, workspace_dir=WORKSPACE_DIR)