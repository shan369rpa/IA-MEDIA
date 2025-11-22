# src/database/db_manager.py

import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import logging
# Cần import kiểu dữ liệu vector từ pgvector.
from pgvector.psycopg2 import register_vector 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    """Tạo và trả về một kết nối đến CSDL PostgreSQL."""
    load_dotenv()
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        logging.info("Kết nối CSDL thành công.")
        # Quan trọng: Đăng ký adapter cho kiểu dữ liệu vector
        register_vector(conn)
        return conn
    except psycopg2.OperationalError as e:
        logging.error(f"Lỗi kết nối CSDL: {e}")
        return None

def insert_chunk_data(conn, data_tuples: list):
    """
    Chèn một danh sách các audio chunk vào CSDL một cách hiệu quả.
    data_tuples là một list của các tuple, ví dụ:
    [(source, word, start_ms, end_ms, label, path, vector), ...]
    """
    if not data_tuples:
        return False
    
    query = """
        INSERT INTO "audio_chunks" 
        (source_video_name, word_text, start_time_ms, end_time_ms, label, chunk_file_path, embedding)
        VALUES %s
    """
    try:
        with conn.cursor() as cur:
            # execute_values là cách hiệu quả nhất để chèn nhiều dòng
            execute_values(cur, query, data_tuples)
        conn.commit()
        logging.info(f"Đã chèn thành công {len(data_tuples)} bản ghi.")
        return True
    except Exception as e:
        logging.error(f"Lỗi khi chèn dữ liệu: {e}")
        conn.rollback()
        return False

def find_similar_chunks(conn, vector, limit=5):
    """Tìm các chunk có vector gần giống nhất với vector đầu vào."""
    query = """
        SELECT id, word_text, label, chunk_file_path, embedding <=> %s AS distance
        FROM "audio_chunks"
        ORDER BY distance
        LIMIT %s
    """
    results = []
    try:
        with conn.cursor() as cur:
            cur.execute(query, (vector, limit))
            results = cur.fetchall()
    except Exception as e:
        logging.error(f"Lỗi khi tìm kiếm vector tương đồng: {e}")
    return results

def clear_table(conn, table_name: str):
    """Xóa tất cả dữ liệu từ một bảng. Rất hữu ích cho việc dọn dẹp sau khi test."""
    # Thêm dấu ngoặc kép để xử lý tên bảng có chữ viết hoa
    query = f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY CASCADE;'
    try:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()
        logging.info(f"Đã xóa toàn bộ dữ liệu từ bảng: {table_name}")
        return True
    except Exception as e:
        logging.error(f"Lỗi khi xóa dữ liệu bảng {table_name}: {e}")
        conn.rollback()
        return False
def get_or_create_source(conn, video_name: str) -> int | None:
    """
    Tìm một source theo tên, nếu không có thì tạo mới.
    Trả về id của source.
    """
    try:
        with conn.cursor() as cur:
            # Thử tìm trước
            cur.execute('SELECT id FROM "sources" WHERE video_name = %s', (video_name,))
            result = cur.fetchone()
            
            if result:
                source_id = result[0]
                logging.info(f"Source '{video_name}' đã tồn tại với id: {source_id}")
                return source_id
            else:
                # Nếu không có, tạo mới
                logging.info(f"Source '{video_name}' chưa tồn tại, đang tạo mới...")
                cur.execute('INSERT INTO "sources" (video_name) VALUES (%s) RETURNING id', (video_name,))
                source_id = cur.fetchone()[0]
                conn.commit()
                logging.info(f"Đã tạo source '{video_name}' với id: {source_id}")
                return source_id
    except Exception as e:
        logging.error(f"Lỗi khi get/create source: {e}")
        conn.rollback()
        return None

def insert_words_data(conn, data_tuples: list):
    """
    Chèn một danh sách các chunk từ vào bảng `words`.
    """
    if not data_tuples:
        return False
    
    query = """
        INSERT INTO "words" (
            sentence_id, word_text, language, start_time_ms_edited, end_time_ms_edited,
            embedding_clean, embedding_error, audio_path_clean, audio_path_error,
            video_path_clean, video_path_error
        ) VALUES %s
    """
    try:
        with conn.cursor() as cur:
            execute_values(cur, query, data_tuples)
        conn.commit()
        logging.info(f"Đã chèn thành công {len(data_tuples)} bản ghi vào bảng 'words'.")
        return True
    except Exception as e:
        logging.error(f"Lỗi khi chèn dữ liệu vào bảng 'words': {e}")
        conn.rollback()
        return False