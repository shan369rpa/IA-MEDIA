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
    
    # The repository now uses the normalized schema (sources, sentences, words, anomalies).
    # Map legacy tuples (source, word, start_ms, end_ms, label, path, vector)
    # into the `words` table. We will:
    #  - ensure a `source` exists (get_or_create_source)
    #  - ensure a `sentence` exists for the time span (create a synthetic sentence if needed)
    #  - insert or upsert a `words` row that may contain embedding_clean and/or embedding_error

    # Group incoming tuples by (source, start_ms, end_ms, word_text)
    groups = {}
    for item in data_tuples:
        try:
            source, word, start_ms, end_ms, label, path, vector = item
        except Exception:
            logging.warning("Dữ liệu không có định dạng mong đợi, bỏ qua một bản ghi.")
            continue
        key = (source, int(start_ms), int(end_ms), word)
        entry = groups.get(key, {
            'source': source,
            'word': word,
            'start_ms': int(start_ms),
            'end_ms': int(end_ms),
            'audio_path_clean': None,
            'audio_path_error': None,
            'embedding_clean': None,
            'embedding_error': None
        })
        if label and label.lower() == 'clean':
            entry['audio_path_clean'] = path
            entry['embedding_clean'] = vector
        else:
            entry['audio_path_error'] = path
            entry['embedding_error'] = vector
        groups[key] = entry

    # Prepare rows to insert into words. We need sentence_id for each; create synthetic sentence if needed.
    rows_to_insert = []
    for key, e in groups.items():
        source_name = e['source']
        # Ensure source exists
        source_id = get_or_create_source(conn, source_name)
        if source_id is None:
            logging.error(f"Không thể xác định source_id cho {source_name}, bỏ qua nhóm {key}.")
            continue

        # Find or create a sentence covering this interval. For simplicity create a synthetic sentence.
        try:
            with conn.cursor() as cur:
                cur.execute(
                    'SELECT id FROM "sentences" WHERE source_id = %s AND start_time_ms = %s AND end_time_ms = %s',
                    (source_id, e['start_ms'], e['end_ms'])
                )
                res = cur.fetchone()
                if res:
                    sentence_id = res[0]
                else:
                    cur.execute(
                        'INSERT INTO "sentences" (source_id, transcript, start_time_ms, end_time_ms) VALUES (%s, %s, %s, %s) RETURNING id',
                        (source_id, None, e['start_ms'], e['end_ms'])
                    )
                    sentence_id = cur.fetchone()[0]
                    conn.commit()
        except Exception as ex:
            logging.error(f"Lỗi khi tìm/tạo sentence cho source {source_name}: {ex}")
            conn.rollback()
            continue

        rows_to_insert.append((
            sentence_id,
            e['word'],
            'und',
            e['start_ms'],
            e['end_ms'],
            e['embedding_clean'],
            e['embedding_error'],
            e['audio_path_clean'],
            e['audio_path_error'],
            None,
            None
        ))

    if not rows_to_insert:
        logging.error("Không có bản ghi hợp lệ để chèn vào 'words'.")
        return False

    try:
        with conn.cursor() as cur:
            execute_values(cur, """
                INSERT INTO "words" (
                    sentence_id, word_text, language, start_time_ms_edited, end_time_ms_edited,
                    embedding_clean, embedding_error, audio_path_clean, audio_path_error,
                    video_path_clean, video_path_error
                ) VALUES %s
            """, rows_to_insert)
        conn.commit()
        logging.info(f"Đã chèn thành công {len(rows_to_insert)} bản ghi vào bảng 'words'.")
        return True
    except Exception as e:
        logging.error(f"Lỗi khi chèn dữ liệu vào bảng 'words': {e}")
        conn.rollback()
        return False

def find_similar_chunks(conn, vector, limit=5):
    """Tìm các chunk có vector gần giống nhất với vector đầu vào."""
    # Prefer words.embedding_clean and embedding_error; return results ordered by distance
    results = []
    try:
        with conn.cursor() as cur:
            # Search by embedding_clean
            cur.execute("SELECT id, word_text, embedding_clean <=> %s AS distance FROM \"words\" ORDER BY distance LIMIT %s", (vector, limit))
            results = cur.fetchall()
    except Exception as e:
        logging.error(f"Lỗi khi tìm kiếm vector tương đồng: {e}")
    return results

def find_similar_words(conn, vector, limit=5):
    """Convenience wrapper to search `words.embedding_clean` by similarity."""
    return find_similar_chunks(conn, vector, limit)

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

# Thêm vào src/database/db_manager.py

def analyze_word_vector(conn, word_text: str, target_vector: list, limit=5):
    """
    So sánh vector mới với các vector đã lưu trong DB của cùng từ đó.
    Trả về khoảng cách trung bình đến nhóm Clean và nhóm Error.
    """
    # Chuyển list thành string định dạng vector cho SQL
    vector_str = str(target_vector)
    
    query = """
        SELECT 
            (embedding_clean <=> %s) as dist_clean,
            (embedding_error <=> %s) as dist_error
        FROM words 
        WHERE word_text = %s
        -- Chỉ lấy những bản ghi có cả 2 vector (để so sánh công bằng)
        AND embedding_error IS NOT NULL 
        ORDER BY dist_error ASC -- Tìm những lỗi giống nhất trước
        LIMIT %s;
    """
    
    try:
        with conn.cursor() as cur:
            cur.execute(query, (vector_str, vector_str, word_text, limit))
            rows = cur.fetchall()
            
            if not rows:
                return None # Từ này chưa từng xuất hiện trong DB
            
            # Tính trung bình khoảng cách
            avg_dist_clean = sum(r[0] for r in rows) / len(rows)
            avg_dist_error = sum(r[1] for r in rows) / len(rows)
            
            return {
                "avg_dist_clean": avg_dist_clean,
                "avg_dist_error": avg_dist_error,
                "sample_count": len(rows)
            }
            
    except Exception as e:
        logging.error(f"Lỗi khi phân tích vector: {e}")
        return None