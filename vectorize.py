# vectorize.py

import os
import glob
import logging
from dotenv import load_dotenv
import pandas as pd

# Import các module chức năng từ thư mục src
from src.database import db_manager
from src.ai import vectorizer

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', force=True)

def main_vectorize(chunk_dir: str):
    """
    Hàm chính điều phối pipeline vector hóa.
    Quét qua thư mục chunk, tạo embedding và chèn vào CSDL.
    """
    logging.info(f"===== STARTING VECTORIZATION PIPELINE ON DIRECTORY: {chunk_dir} =====")

    # 1. Tìm file metadata.csv
    metadata_path = os.path.join(chunk_dir, "metadata.csv")
    if not os.path.exists(metadata_path):
        logging.error(f"Metadata file not found at '{metadata_path}'. Cannot proceed. Stopping.")
        return

    try:
        df = pd.read_csv(metadata_path)
        logging.info(f"Loaded metadata for {len(df)} chunks.")
    except Exception as e:
        logging.error(f"Failed to read metadata.csv: {e}")
        return

    # 2. Khởi tạo model embedding
    # Hàm này sẽ tải model (có thể mất thời gian lần đầu)
    embedding_model = vectorizer.load_embedding_model()
    if not embedding_model:
        logging.error("Failed to load embedding model. Stopping.")
        return

    # 3. Kết nối CSDL
    conn = db_manager.get_db_connection()
    if not conn:
        logging.error("Failed to connect to the database. Stopping.")
        return

    # 4. Lặp qua metadata, tạo embedding và chuẩn bị dữ liệu
    logging.info("Starting to generate embeddings for audio chunks...")
    data_to_insert = []
    total_chunks = len(df)

    for index, row in df.iterrows():
        # Chỉ tạo embedding cho các file audio
        if row['label'] in ['clean', 'error']: # Giả định chỉ có 2 nhãn này cho audio
            audio_path = os.path.join(chunk_dir, row['audio_path'])
            if os.path.exists(audio_path):
                # Tạo embedding
                embedding = vectorizer.create_embedding(audio_path, embedding_model)
                
                # TODO: Cập nhật cấu trúc bảng `words` để có 2 cột embedding
                # Tạm thời chúng ta sẽ chèn vào một bảng `audio_chunks` đơn giản hơn
                # Logic này cần được hoàn thiện sau khi chốt schema SQL cuối cùng
                
                # data_to_insert.append((...))
                pass # Placeholder
            else:
                logging.warning(f"Audio file not found, skipping: {audio_path}")
        
        if (index + 1) % 100 == 0:
            logging.info(f"Processed {index + 1}/{total_chunks} chunks...")

    logging.info("Embedding generation complete.")
    
    # 5. Chèn dữ liệu vào CSDL
    if data_to_insert:
        logging.info(f"Inserting {len(data_to_insert)} records into the database...")
        # db_manager.insert_chunk_data(conn, data_to_insert)
        pass # Placeholder
    else:
        logging.warning("No data was prepared for database insertion.")

    conn.close()
    logging.info("===== VECTORIZATION PIPELINE FINISHED =====")


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