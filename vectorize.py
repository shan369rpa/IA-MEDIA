# vectorize.py
import os
from dotenv import load_dotenv
import logging

# Giả định chúng ta sẽ tạo các module này
from src.database import db_manager
from src.ai import vectorizer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main_vectorize():
    """
    Hàm chính điều phối pipeline:
    Audio Chunks -> Vector Embeddings in Database.
    """
    logging.info("===== BẮT ĐẦU PIPELINE VECTOR HÓA =====")

    # 1. Tải cấu hình
    load_dotenv()
    workspace_dir = os.getenv("WORKSPACE_DIR")
    chunk_dir = os.path.join(workspace_dir, "phonetic_chunks")

    # 2. Lấy danh sách tất cả các file chunk cần xử lý
    # Chúng ta sẽ cần hàm này
    # chunk_files = get_all_chunk_files(chunk_dir)
    
    # 3. Khởi tạo model embedding
    # Chúng ta sẽ cần module vectorizer
    # model = vectorizer.load_embedding_model()

    # 4. Kết nối CSDL
    conn = db_manager.get_db_connection()
    if not conn:
        logging.error("Không thể kết nối CSDL. Dừng pipeline.")
        return

    # 5. Lặp qua các chunk, vector hóa và chuẩn bị dữ liệu để chèn
    # data_to_insert = []
    # for file_path in chunk_files:
    #     vector = vectorizer.create_embedding(file_path, model)
    #     # Trích xuất metadata từ file_path (word, label, timestamps...)
    #     # Thêm tuple dữ liệu vào data_to_insert

    # 6. Chèn tất cả dữ liệu vào CSDL trong một lần
    # db_manager.insert_chunk_data(conn, data_to_insert)

    conn.close()
    logging.info("===== KẾT THÚC PIPELINE VECTOR HÓA =====")


if __name__ == "__main__":
    # TODO: Lấp đầy logic
    pass