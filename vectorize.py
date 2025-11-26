# vectorize.py

import os
import logging
from dotenv import load_dotenv
import pandas as pd
import numpy as np # Cần numpy để làm việc với vector

# Import các module chức năng từ thư mục src
from src.database import db_manager
from src.ai import vectorizer

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s', force=True)

def main_vectorize(chunk_dir: str):
    """
    Hàm chính điều phối pipeline vector hóa.
    Quét qua metadata, tạo embedding và chèn vào CSDL đa bảng.
    """
    logging.info(f"===== STARTING VECTORIZATION PIPELINE ON DIRECTORY: {chunk_dir} =====")

    # 1. Tìm và tải file metadata.csv
    metadata_path = os.path.join(chunk_dir, "metadata.csv")
    if not os.path.exists(metadata_path):
        logging.error(f"Metadata file not found at '{metadata_path}'. Cannot proceed. Stopping.")
        return

    try:
        df = pd.read_csv(metadata_path)
        # --- FIX QUAN TRỌNG: Chuyển đổi DataFrame thành List of Dictionaries ---
        # Điều này giúp chúng ta làm việc với biến chuẩn Python (str, int), 
        # tránh lỗi TypeError khi đưa vào os.path.join
        records = df.to_dict('records')
        logging.info(f"Step 1/5: Loaded metadata for {len(df)} chunk records.")
    except Exception as e:
        logging.error(f"Failed to read metadata.csv: {e}")
        return

    # 2. Khởi tạo model embedding
    logging.info("Step 2/5: Loading embedding model (this may take a while)...")
    embedding_model = vectorizer.load_embedding_model()
    if not embedding_model:
        logging.error("Failed to load embedding model. Stopping.")
        return

    # 3. Kết nối CSDL
    logging.info("Step 3/5: Connecting to the database...")
    conn = db_manager.get_db_connection()
    if not conn:
        logging.error("Failed to connect to the database. Stopping.")
        return

    # 4. Xử lý và Chèn dữ liệu
    # Do kiến trúc đa bảng, chúng ta cần xử lý theo từng video nguồn
    # để có thể lấy `source_id` và chèn vào các bảng con.
    
    processed_records = 0
    unique_videos = df['source_video'].unique()
    logging.info(f"Found {len(unique_videos)} unique video sources in metadata.")

    for video_name in unique_videos:
        logging.info(f"--- Processing source: {video_name} ---")
        
        # Lấy hoặc tạo source_id
        source_id = db_manager.get_or_create_source(conn, video_name)
        if source_id is None:
            logging.error(f"Could not get or create source_id for {video_name}. Skipping.")
            continue

        # Lọc dataframe cho video hiện tại
        video_df = df[df['source_video'] == video_name].copy()
        
        # --- TẠM THỜI BỎ QUA XỬ LÝ SENTENCES VÀ ANOMALIES TRONG DEMO NÀY ---
        # Chúng ta sẽ tập trung vào bảng `words` trước tiên

        # Chuẩn bị dữ liệu cho bảng `words`
        words_to_insert = []
        clean_chunks = video_df[video_df['label'] == 'clean'].set_index('start_ms_edited', drop=False)
        error_chunks = video_df[video_df['label'] == 'error'].set_index('start_ms_edited', drop=False)

        logging.info(f"Step 4/5: Generating embeddings for {len(clean_chunks)} word pairs...")
        for start_ms, clean_row in clean_chunks.iterrows():
            if start_ms in error_chunks.index:
                # --- SỬA LỖI Ở ĐÂY ---
                error_data = error_chunks.loc[start_ms]
                
                # Kiểm tra nếu kết quả trả về là DataFrame (do trùng index), chỉ lấy dòng đầu tiên
                if isinstance(error_data, pd.DataFrame):
                    error_row = error_data.iloc[0]
                else:
                    error_row = error_data
                # ---------------------

                # Đảm bảo ép kiểu string cho đường dẫn để tránh lỗi
                clean_rel_path = str(clean_row['audio_path'])
                error_rel_path = str(error_row['audio_path'])

                clean_audio_path = os.path.join(chunk_dir, clean_rel_path)
                error_audio_path = os.path.join(chunk_dir, error_rel_path)

                # Tạo embedding cho cả hai
                embedding_clean = vectorizer.create_embedding(clean_audio_path, embedding_model)
                embedding_error = vectorizer.create_embedding(error_audio_path, embedding_model)

                if embedding_clean is not None and embedding_error is not None:
                    words_to_insert.append((
                        1, # Tạm thời gán sentence_id = 1
                        clean_row['word_text'],
                        'vie', # Tạm thời gán language = 'vie'
                        int(clean_row['start_ms_edited']),
                        int(clean_row['end_ms_edited']),
                        np.array(embedding_clean),
                        np.array(embedding_error),
                        clean_rel_path,
                        error_rel_path,
                        clean_row['video_path'],
                        error_row['video_path']
                    ))
                    processed_records += 1
        
        # Chèn tất cả các bản ghi của video này vào CSDL
        if words_to_insert:
            logging.info(f"Step 5/5: Inserting {len(words_to_insert)} records into 'words' table for {video_name}...")
            # Chúng ta sẽ cần tạo hàm insert_words_data trong db_manager
            db_manager.insert_words_data(conn, words_to_insert)
        else:
            logging.warning(f"No valid word pairs found to insert for {video_name}.")

    conn.close()
    logging.info(f"\n===== VECTORIZATION PIPELINE FINISHED: Processed and prepared {processed_records} records. =====")


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