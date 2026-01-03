# ingest.py (Final v3.0 - Full Event & Word Processing)

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

def process_and_ingest_session(fcpxml_path: str, workspace_dir: str):
    """
    Xử lý session: FCPXML -> Events (DB) -> Words (DB).
    Quản lý kết nối DB ngắt quãng để tránh timeout.
    """
    session_id = os.path.splitext(os.path.basename(fcpxml_path))[0]
    logging.info(f"\n--- Processing Session: {session_id} ---")
    
    try:
        # ==============================================================================
        # GIAI ĐOẠN 1: CHUẨN BỊ & XỬ LÝ SỰ KIỆN (EVENTS)
        # ==============================================================================
        
        # 1. Phân tích FCPXML
        logging.info("Step 1/6: Parsing FCPXML...")
        analysis_data = fcpxml_parser.extract_events_and_map(fcpxml_path)
        time_map = analysis_data["time_map"]
        edit_events = analysis_data["edit_events"]
        if not edit_events:
            logging.warning("No edit events found. Skipping.")
            return

        # 2. Chuẩn bị Audio
        logging.info("Step 2/6: Preparing audio files...")
        source_dir = os.path.dirname(fcpxml_path)
        # Tìm file raw/edited dựa trên quy ước đặt tên (giả sử _raw.mp4 và _edited.mp4)
        raw_video_path = os.path.join(source_dir, f"{session_id}_raw.mp4")
        edited_video_path = os.path.join(source_dir, f"{session_id}_edited.mp4")
        
        raw_audio_path, edited_audio_path = file_handler.extract_audio_pair(
            raw_video_path, edited_video_path, workspace_dir
        )
        if not raw_audio_path or not edited_audio_path:
            logging.error("Audio extraction failed. Skipping.")
            return

        clean_audio = AudioSegment.from_wav(edited_audio_path)
        error_audio = AudioSegment.from_wav(raw_audio_path)

        # 3. Vector hóa các Edit Events
        logging.info(f"Step 3/6: Processing {len(edit_events)} edit events (Chunking & Embedding)...")
        embedding_model = vectorizer.load_embedding_model()
        output_chunk_dir = os.path.join(workspace_dir, "event_chunks")
        
        # Danh sách chứa dữ liệu sự kiện để chèn (dùng dictionary cho dễ xử lý)
        events_payload = [] 

        for event in tqdm(edit_events, desc=f"Events: {session_id}"):
            clean_path, error_path = chunker.chunk_event(
                event, clean_audio, error_audio, time_map, output_chunk_dir, session_id
            )
            if clean_path and error_path:
                emb_clean = vectorizer.create_embedding(clean_path, embedding_model)
                emb_error = vectorizer.create_embedding(error_path, embedding_model)
                if emb_clean and emb_error:
                    events_payload.append({
                        "start_ms": int(event['start'] * 1000),
                        "end_ms": int(event['end'] * 1000),
                        "event_source": 'FCPXML',
                        "event_type": event['type'],
                        "embedding_clean": np.array(emb_clean),
                        "embedding_error": np.array(emb_error),
                        "details": json.dumps(event['details']),
                        "audio_path_clean": os.path.relpath(clean_path, workspace_dir),
                        "audio_path_error": os.path.relpath(error_path, workspace_dir),
                        # Lưu đường dẫn tuyệt đối tạm để dùng cho bước xử lý Words
                        "_abs_path_clean": clean_path,
                        "_abs_path_error": error_path
                    })

        if not events_payload:
            logging.warning("No valid events generated. Skipping DB ingestion.")
            return

        # ==============================================================================
        # GIAI ĐOẠN 2: GHI EVENTS VÀO DB (NHỊP 1)
        # ==============================================================================
        logging.info("Step 4/6: Inserting Events into DB...")
        
        event_id_map = {} # Map từ start_ms -> event_id
        source_id = None

        conn = db_manager.get_db_connection()
        if not conn: return

        try:
            # Lấy source_id
            source_id = db_manager.get_or_create_source(conn, session_id)
            if source_id:
                # Thêm source_id vào payload
                for e in events_payload: e["source_id"] = source_id
                
                # Chèn và lấy lại ID (Hàm này cần được định nghĩa trong db_manager)
                event_id_map = db_manager.insert_edit_events_and_get_ids(conn, events_payload)
        finally:
            conn.close() # ĐÓNG KẾT NỐI NGAY để tránh timeout khi chạy Whisper
            logging.info("DB Connection closed. Proceeding to Word processing...")

        if not event_id_map:
            logging.error("Failed to insert events or retrieve IDs. Skipping word processing.")
            return

        # ==============================================================================
        # GIAI ĐOẠN 3: XỬ LÝ TỪNG TỪ (WORDS) - CHẠY WHISPER (TỐN THỜI GIAN)
        # ==============================================================================
        logging.info("Step 5/6: Processing Words (WhisperX & Vectorization)...")
        words_to_insert = []
        
        # Thư mục tạm cho word chunks
        temp_word_dir = os.path.join(workspace_dir, "temp_word_chunks") 

        for event_data in tqdm(events_payload, desc=f"Words: {session_id}"):
            event_start_ms = event_data["start_ms"]
            event_id = event_id_map.get(event_start_ms)
            
            if not event_id: continue # Không tìm thấy ID trong DB, bỏ qua

            # Chạy WhisperX trên file chunk sự kiện (nhanh hơn chạy cả video)
            clean_event_path = event_data["_abs_path_clean"]
            error_event_path = event_data["_abs_path_error"]
            
            word_timestamps = transcriber.get_word_timestamps(clean_event_path)
            
            if not word_timestamps: continue

            # Tải audio sự kiện vào RAM để cắt nhỏ
            ev_audio_clean = AudioSegment.from_wav(clean_event_path)
            ev_audio_error = AudioSegment.from_wav(error_event_path)

            for word_info in word_timestamps:
                word_text = word_info.get('word', '').strip()
                if not word_text: continue

                # ID tạm để đặt tên file
                w_id = f"{session_id}_{event_id}_{int(word_info['start']*1000)}"
                
                # Cắt micro-chunk
                w_clean_path, w_error_path = chunker.chunk_word_from_event(
                    word_info, ev_audio_clean, ev_audio_error, temp_word_dir, w_id
                )

                if w_clean_path and w_error_path:
                    # Tạo embedding
                    w_emb_clean = vectorizer.create_embedding(w_clean_path, embedding_model)
                    w_emb_error = vectorizer.create_embedding(w_error_path, embedding_model)
                    
                    if w_emb_clean and w_emb_error:
                        # Tính timestamp tuyệt đối trên timeline video gốc
                        abs_start = event_start_ms + int(word_info['start'] * 1000)
                        abs_end = event_start_ms + int(word_info['end'] * 1000)

                        words_to_insert.append((
                            source_id,
                            event_id,
                            word_text,
                            abs_start,
                            abs_end,
                            'vie',
                            np.array(w_emb_clean),
                            np.array(w_emb_error)
                        ))
                    
                    # Dọn dẹp file tạm ngay để tiết kiệm ổ cứng
                    if os.path.exists(w_clean_path): os.remove(w_clean_path)
                    if os.path.exists(w_error_path): os.remove(w_error_path)

        # ==============================================================================
        # GIAI ĐOẠN 4: GHI WORDS VÀO DB (NHỊP 2)
        # ==============================================================================
        if words_to_insert:
            logging.info(f"Step 6/6: Connecting to DB to insert {len(words_to_insert)} words...")
            conn = db_manager.get_db_connection()
            if conn:
                try:
                    db_manager.insert_words_batch(conn, words_to_insert)
                    logging.info(f"--- Session {session_id} COMPLETED successfully! ---")
                finally:
                    conn.close()
        else:
            logging.info("No words found to insert.")

    except Exception as e:
        logging.exception(f"A critical error occurred while processing session {session_id}.")


def ingest_main(source_dir: str, workspace_dir: str):
    """Hàm điều phối chính."""
    logging.info(f"===== STARTING INGESTION PIPELINE V3.0 on: {source_dir} =====")
    
    logging.info("Pre-loading AI models...")
    try:
        vectorizer.load_embedding_model()
        
        fcpxml_files = glob.glob(os.path.join(source_dir, "**", "*.fcpxml"), recursive=True)
        if not fcpxml_files:
            logging.error(f"No .fcpxml files found in '{source_dir}'.")
            return
            
        for fcpxml_path in fcpxml_files:
            process_and_ingest_session(fcpxml_path, workspace_dir)

        logging.info("===== INGESTION PIPELINE FINISHED FOR ALL SESSIONS =====")
    except Exception as e:
        logging.error(f"Global pipeline error: {e}")
    finally:
        # Đảm bảo đóng tunnel nếu có dùng sshtunnel
        if hasattr(db_manager, 'close_ssh_tunnel'):
            db_manager.close_ssh_tunnel()

if __name__ == "__main__":
    load_dotenv()
    # Ví dụ chạy local, nhớ sửa đường dẫn cho đúng máy của bạn
    SOURCE_DIR = "D:\\IA MEDIA\\Data\\Batch_02" 
    WORKSPACE_DIR = "./workspace"
    ingest_main(source_dir=SOURCE_DIR, workspace_dir=WORKSPACE_DIR)