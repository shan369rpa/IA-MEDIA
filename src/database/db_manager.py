# src/database/db_manager.py
import psycopg2
import os

def get_db_connection():
    # Code kết nối CSDL dùng các biến env
    pass

def create_chunks_table(conn):
    # Code SQL để tạo bảng `audio_chunks` với các cột:
    # id, word, label (clean/error), file_path, embedding (kiểu vector)
    pass

# src/database/db_manager.py

def insert_chunk_data(conn, source_video, word, start_ms, end_ms, label, file_path, vector):
    """Chèn dữ liệu của một audio chunk vào CSDL."""
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO audio_chunks 
                (source_video_name, word_text, start_time_ms, end_time_ms, label, chunk_file_path, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (source_video, word, start_ms, end_ms, label, file_path, vector)
            )
        conn.commit()
        return True
    except Exception as e:
        print(f"Lỗi khi chèn dữ liệu: {e}")
        conn.rollback()
        return False