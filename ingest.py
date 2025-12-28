# ingest.py

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

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s', force=True)

def ingest_pipeline(source_dir: str, workspace_dir: str):
    logging.info(f"===== STARTING INGESTION PIPELINE V3.0 on: {source_dir} =====")
    
    conn = db_manager.get_db_connection()
    if not conn:
        logging.error("Không thể kết nối CSDL. Dừng pipeline.")
        return
        
    embedding_model = vectorizer.load_embedding_model()
    if not embedding_model:
        logging.error("Không thể tải model embedding. Dừng pipeline.")
        return

    # Tìm tất cả các session để xử lý
    fcpxml_files = glob.glob(os.path.join(source_dir, "**", "*.fcpxml"), recursive=True)
    if not fcpxml_files:
        logging.error(f"No .fcpxml files found in '{source_dir}'.")
        return

    for fcpxml_path in fcpxml_files:
        session_id = os.path.splitext(os.path.basename(fcpxml_path))[0]
        logging.info(f"\n--- Processing Session: {session_id} ---")

        try:
            # 1. Trích xuất Events và Time Map từ FCPXML
            analysis_data = fcpxml_parser.extract_events_and_map(fcpxml_path)
            time_map = analysis_data["time_map"]
            edit_events = analysis_data["edit_events"]

            # 2. Chuẩn bị Audio
            raw_video_path = os.path.join(os.path.dirname(fcpxml_path), f"{session_id}_raw.mp4")
            edited_video_path = os.path.join(os.path.dirname(fcpxml_path), f"{session_id}_edited.mp4")
            raw_audio_path, edited_audio_path = file_handler.extract_audio_pair(
                raw_video_path, edited_video_path, workspace_dir
            )
            clean_audio = AudioSegment.from_wav(edited_audio_path)
            error_audio = AudioSegment.from_wav(raw_audio_path)

            # 3. Chèn 'source' vào DB và lấy ID
            source_id = db_manager.get_or_create_source(conn, session_id)
            if source_id is None: continue

            # 4. Xử lý và Chèn các Edit Events
            logging.info(f"Processing {len(edit_events)} edit events from FCPXML...")
            events_to_insert = []
            output_chunk_dir = os.path.join(workspace_dir, "event_chunks")

            for event in tqdm(edit_events, desc="Processing Events"):
                # Cắt cặp audio chunk cho event
                clean_path, error_path = chunker.chunk_event(
                    event, clean_audio, error_audio, time_map, output_chunk_dir, session_id
                )
                
                if clean_path and error_path:
                    # Tạo embedding cho cả 2
                    emb_clean = vectorizer.create_embedding(clean_path, embedding_model)
                    emb_error = vectorizer.create_embedding(error_path, embedding_model)

                    if emb_clean and emb_error:
                        events_to_insert.append((
                            source_id,
                            int(event['start'] * 1000),
                            int(event['end'] * 1000),
                            'FCPXML', # event_source
                            event['type'], # event_type
                            np.array(emb_clean),
                            np.array(emb_error),
                            json.dumps(event['details']),
                            os.path.relpath(clean_path, workspace_dir),
                            os.path.relpath(error_path, workspace_dir)
                        ))
            
            # Chèn hàng loạt vào CSDL
            db_manager.insert_edit_events(conn, events_to_insert)
            
            # --- Tạm thời bỏ qua xử lý WORDS cho gọn ---
            # (Logic chạy Whisper, cắt word, chèn vào bảng 'words' sẽ được thêm vào đây sau)

        except Exception as e:
            logging.exception(f"Lỗi nghiêm trọng khi xử lý session {session_id}.")

    conn.close()
    logging.info("===== INGESTION PIPELINE FINISHED =====")


if __name__ == "__main__":
    load_dotenv()
    
    SOURCE_DIR = "D:\\IA MEDIA\\Data\\Batch_02"
    WORKSPACE_DIR = "./workspace"

    ingest_pipeline(source_dir=SOURCE_DIR, workspace_dir=WORKSPACE_DIR)