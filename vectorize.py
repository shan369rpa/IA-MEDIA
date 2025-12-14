import os
import logging
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from tqdm import tqdm

from src.database import db_manager
from src.ai import vectorizer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s', force=True)

def main_vectorize(chunk_dir: str):
    logging.info(f"===== STARTING VECTORIZATION PIPELINE ON DIRECTORY: {chunk_dir} =====")

    # 1. Tải metadata
    metadata_path = os.path.join(chunk_dir, "metadata.csv")
    required_columns = ['source_video', 'label', 'start_ms', 'audio_path']

    if not os.path.exists(metadata_path):
        logging.error(f"Metadata file not found at '{metadata_path}'. Cannot proceed. Stopping.")
        return
    try:
        df = pd.read_csv(metadata_path)
        logging.info(f"Step 1/5: Loaded metadata for {len(df)} chunk records.")
    except Exception as e:
        logging.error(f"Failed to read metadata.csv: {e}")
        return

    # 2. Khởi tạo model embedding
    logging.info("Step 2/5: Loading embedding model...")
    embedding_model = vectorizer.load_embedding_model()
    if not embedding_model:
        return

    # 3. Kết nối CSDL
    logging.info("Step 3/5: Connecting to the database...")
    conn = db_manager.get_db_connection()
    if not conn:
        return

    # 4. Xử lý theo từng video nguồn
    unique_videos = df['source_video'].unique()
    logging.info(f"Found {len(unique_videos)} unique video sources to process.")

    for video_name in unique_videos:
        logging.info(f"--- Processing source: {video_name} ---")
        
        source_id = db_manager.get_or_create_source(conn, video_name)
        if source_id is None:
            continue

        video_df = df[df['source_video'] == video_name].copy()
        
        # --- [NÂNG CẤP] TẠM THỜI TẠO 1 SENTENCE CHA CHO TOÀN BỘ VIDEO ---
        # Sau này chúng ta sẽ có logic chunk câu thật sự
        sentence_id = db_manager.get_or_create_sentence(conn, source_id, f"Full transcript for {video_name}", 0, 9999999)
        if sentence_id is None: continue

        # Ghép cặp clean/error lại với nhau
        clean_chunks = video_df[video_df['label'] == 'clean'].set_index('start_ms')
        error_chunks = video_df[video_df['label'].str.startswith('error')].set_index('start_ms')

        words_to_insert = []
        
        logging.info(f"Step 4/5: Generating embeddings for {len(clean_chunks)} word pairs...")
        
        for start_ms, clean_row in tqdm(clean_chunks.iterrows(), total=len(clean_chunks), desc=f"Vectorizing {video_name}"):
            if start_ms in error_chunks.index:
                error_row = error_chunks.loc[start_ms]

                # Đảm bảo ép kiểu string cho đường dẫn để tránh lỗi
                clean_rel_path = str(clean_row['audio_path'])
                error_rel_path = str(error_row['audio_path'])

                clean_audio_path = os.path.join(chunk_dir, clean_rel_path)
                error_audio_path = os.path.join(chunk_dir, error_rel_path)

                # Tạo embedding cho cả hai
                embedding_clean = vectorizer.create_embedding(clean_audio_path, embedding_model)
                embedding_error = vectorizer.create_embedding(error_audio_path, embedding_model)

                if embedding_clean is not None and embedding_error is not None:
                    # --- [NÂNG CẤP] Thay đổi cấu trúc dữ liệu để chèn vào bảng `words` ---
                    words_to_insert.append({
                        "sentence_id": sentence_id,
                        "word_text": clean_row['word_text'],
                        "language": 'vie', # TODO: Tích hợp Language ID
                        "start_time_ms_edited": int(start_ms),
                        "end_time_ms_edited": int(clean_row['end_ms']),
                        "embedding_clean": np.array(embedding_clean),
                        "embedding_error": np.array(embedding_error),
                        "audio_path_clean": clean_rel_path,
                        "audio_path_error": error_rel_path,
                        # Giữ lại các cột video_path nếu có trong metadata, nếu không sẽ là None
                        "video_path_clean": clean_row.get('video_path'), 
                        "video_path_error": error_row.get('video_path'),
                    })

        # 5. Chèn dữ liệu vào CSDL
        logging.info(f"Step 5/5: Inserting data into database for {video_name}...")
        if words_to_insert:
            # --- [NÂNG CẤP] Gọi hàm chèn `words` và lấy lại ID ---
            word_ids_map = db_manager.insert_words_and_get_ids(conn, words_to_insert)
            
            # --- [LOGIC SLICING MỚI] ---
            if word_ids_map:
                logging.info("   - Starting sliding window analysis...")
                all_slices_to_insert = []
                for word_data in tqdm(words_to_insert, desc="Slicing words"):
                    word_id = word_ids_map.get(word_data["start_time_ms_edited"])
                    if not word_id: continue

                    # Slicing Clean Audio
                    clean_audio_path = os.path.join(chunk_dir, word_data['audio_path_clean'])
                    clean_slices_vecs = vectorizer.create_sliding_window_embeddings(clean_audio_path, embedding_model)
                    if clean_slices_vecs:
                        for i, vec in enumerate(clean_slices_vecs):
                            all_slices_to_insert.append((word_id, "clean", i, np.array(vec)))
                    
                    # Slicing Error Audio
                    error_audio_path = os.path.join(chunk_dir, word_data['audio_path_error'])
                    error_slices_vecs = vectorizer.create_sliding_window_embeddings(error_audio_path, embedding_model)
                    if error_slices_vecs:
                        for i, vec in enumerate(error_slices_vecs):
                            all_slices_to_insert.append((word_id, "error", i, np.array(vec)))
                
                if all_slices_to_insert:
                    logging.info(f"   - Inserting {len(all_slices_to_insert)} slices into 'word_slices' table...")
                    db_manager.insert_word_slices(conn, all_slices_to_insert)
        else:
            logging.warning(f"No valid data to insert for {video_name}.")

    conn.close()
    logging.info(f"\n===== VECTORIZATION PIPELINE FINISHED =====")
if __name__ == '__main__':
    # Phần này dùng để chạy test cục bộ trong Codespaces
    print("Running vectorize.py in local test mode...")
    load_dotenv()
    
    TEST_WORKSPACE_DIR = "./workspace"
    TEST_CHUNK_DIR = os.path.join(TEST_WORKSPACE_DIR, "datasets", "tnh_speech_v0.1")

    if os.path.exists(TEST_CHUNK_DIR):
        main_vectorize(chunk_dir=TEST_CHUNK_DIR)
    else:
        print(f"Test chunk directory not found: {TEST_CHUNK_DIR}")  