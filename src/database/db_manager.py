# src/database/db_manager.py

import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import logging
import numpy as np
# Cần import kiểu dữ liệu vector từ pgvector.
from pgvector.psycopg2 import register_vector 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from sshtunnel import SSHTunnelForwarder # <-- IMPORT THƯ VIỆN MỚI
_server_tunnel = None
def _start_ssh_tunnel():
    """
    Kiểm tra cấu hình .env và khởi tạo đường hầm SSH nếu cần thiết.
    Sử dụng cache để chỉ mở tunnel một lần.
    """
    global _server_tunnel
    if _server_tunnel and _server_tunnel.is_active:
        logging.info("Đường hầm SSH đã hoạt động. Tái sử dụng.")
        return _server_tunnel.local_bind_port

    ssh_host = os.getenv("SSH_HOST")
    if not ssh_host:
        # Nếu không có SSH_HOST, hoạt động ở chế độ kết nối trực tiếp
        logging.info("Không có cấu hình SSH_HOST. Kết nối trực tiếp đến DB.")
        return None

    try:
        ssh_user = os.getenv("SSH_USER")
        ssh_password = os.getenv("SSH_PASSWORD")
        ssh_pkey = os.getenv("SSH_PRIVATE_KEY_PATH")

        # Cấu hình server tunnel
        tunnel = SSHTunnelForwarder(
            (ssh_host, 22), # Host và port của SSH server
            ssh_username=ssh_user,
            ssh_password=ssh_password if ssh_password else None,
            ssh_pkey=ssh_pkey if ssh_pkey else None,
            remote_bind_address=('127.0.0.1', int(os.getenv("DB_PORT", 5432))), # Đích đến bên trong server
            local_bind_address=('127.0.0.1', 0) # 0 = để hệ điều hành tự chọn một cổng trống
        )
        
        logging.info(f"Đang mở đường hầm SSH đến {ssh_host}...")
        tunnel.start()
        _server_tunnel = tunnel
        logging.info(f"✅ Đường hầm SSH đã được mở. DB giờ đây có thể truy cập tại: localhost:{tunnel.local_bind_port}")
        
        return tunnel.local_bind_port

    except Exception as e:
        logging.error(f"❌ LỖI: Không thể mở đường hầm SSH: {e}")
        return None

# def get_db_connection():
#     """Tạo và trả về một kết nối đến CSDL PostgreSQL."""
#     load_dotenv()
#     try:
#         conn = psycopg2.connect(
#             host=os.getenv("DB_HOST"),
#             port=os.getenv("DB_PORT"),
#             dbname=os.getenv("DB_NAME"),
#             user=os.getenv("DB_USER"),
#             password=os.getenv("DB_PASSWORD")
#         )
#         logging.info("Kết nối CSDL thành công.")
#         # Quan trọng: Đăng ký adapter cho kiểu dữ liệu vector
#         register_vector(conn)
#         return conn
#     except psycopg2.OperationalError as e:
#         logging.error(f"Lỗi kết nối CSDL: {e}")
#         return None
def get_db_connection():
    """
    Tự động mở đường hầm SSH (nếu được cấu hình) và kết nối đến CSDL.
    """
    local_port = _start_ssh_tunnel()
    
    db_host = "127.0.0.1" if local_port else os.getenv("DB_HOST")
    db_port = local_port if local_port else int(os.getenv("DB_PORT", 5432))
    
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        logging.info("Kết nối CSDL thành công.")
        from pgvector.psycopg2 import register_vector
        register_vector(conn)
        return conn
        
    except psycopg2.OperationalError as e:
        logging.error(f"Lỗi kết nối CSDL: {e}")
        return None
    
def close_ssh_tunnel():
    """Hàm tiện ích để đóng đường hầm khi pipeline kết thúc."""
    global _server_tunnel
    if _server_tunnel and _server_tunnel.is_active:
        logging.info("Đang đóng đường hầm SSH...")
        _server_tunnel.stop()
        _server_tunnel = None
        logging.info("Đã đóng đường hầm SSH.")
        
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

# def insert_words_data(conn, data_tuples: list):
#     """
#     Chèn một danh sách các chunk từ vào bảng `words`.
#     """
#     if not data_tuples:
#         return False
    
#     query = """
#         INSERT INTO "words" (
#             sentence_id, word_text, language, start_time_ms_edited, end_time_ms_edited,
#             embedding_clean, embedding_error, audio_path_clean, audio_path_error,
#             video_path_clean, video_path_error
#         ) VALUES %s
#     """
#     try:
#         with conn.cursor() as cur:
#             execute_values(cur, query, data_tuples)
#         conn.commit()
#         logging.info(f"Đã chèn thành công {len(data_tuples)} bản ghi vào bảng 'words'.")
#         return True
#     except Exception as e:
#         logging.error(f"Lỗi khi chèn dữ liệu vào bảng 'words': {e}")
#         conn.rollback()
#         return False
    
# src/database/db_manager.py (Thêm vào)
# Thêm vào src/database/db_manager.py

def insert_words_batch(conn, words_data: list):
    """
    Chèn một danh sách (batch) các bản ghi từ vào bảng 'words'.
    words_data là một list of tuples.
    """
    if not words_data:
        return False
    
    query = """
        INSERT INTO "words" (
            source_id, parent_event_id, word_text, start_ms, end_ms,
            language, embedding_clean, embedding_error
        ) VALUES %s
        ON CONFLICT DO NOTHING; -- Bỏ qua nếu có lỗi khóa (ví dụ, trùng lặp)
    """
    try:
        with conn.cursor() as cur:
            execute_values(cur, query, words_data, page_size=500)
        conn.commit()
        logging.info(f"Đã chèn thành công {len(words_data)} bản ghi vào bảng 'words'.")
        return True
    except Exception as e:
        logging.error(f"Lỗi khi chèn dữ liệu vào bảng 'words': {e}")
        conn.rollback()
        return False
    
def get_word_vectors(conn, word_text: str, limit=50):
    """
    Lấy các mẫu vector của một từ cụ thể từ DB.
    Trả về danh sách các dict: {'label': 'clean'/'error', 'embedding': [...]}
    """
    query = """
        SELECT label, embedding 
        FROM "words" -- (Hoặc bảng nơi bạn lưu vector)
        WHERE word_text = %s
        LIMIT %s
    """
    # Lưu ý: Nếu schema mới của bạn chia ra embedding_clean và embedding_error trong cùng 1 row (bảng words),
    # query sẽ cần sửa lại để union 2 cột đó hoặc select cả hai. 
    # Giả sử schema đơn giản hoặc đã union:
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT embedding_clean, 'clean' FROM words WHERE word_text = %s LIMIT %s", (word_text, limit))
            clean_rows = cur.fetchall()
            
            cur.execute("SELECT embedding_error, 'error' FROM words WHERE word_text = %s LIMIT %s", (word_text, limit))
            error_rows = cur.fetchall()
            
            results = []
            for r in clean_rows: results.append({'label': 'clean', 'embedding': np.array(r[0])})
            for r in error_rows: results.append({'label': 'error', 'embedding': np.array(r[0])})
            
            return results
    except Exception as e:
        logging.error(f"Lỗi query vector: {e}")
        return []
def insert_words_and_get_ids(conn, words_data: list) -> dict:
    """
    Chèn một danh sách các từ vào bảng `words` và trả về một map
    giữa start_ms_edited và word_id mới được tạo.
    """
    if not words_data:
        return {}
    
    id_map = {}
    query = """
        INSERT INTO "words" (
            sentence_id, word_text, language, start_time_ms_edited, end_time_ms_edited,
            embedding_clean, embedding_error, audio_path_clean, audio_path_error, 
            video_path_clean, video_path_error, label
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id, start_time_ms_edited
    """
    try:
        with conn.cursor() as cur:
            for d in words_data:
                # --- SỬA LỖI Ở ĐÂY ---
                # Chuyển đổi dictionary `d` thành một tuple `data_tuple`
                # theo đúng thứ tự các cột trong câu lệnh INSERT
                data_tuple = (
                    d["sentence_id"],
                    d["word_text"],
                    d["language"],
                    d["start_time_ms_edited"],
                    d["end_time_ms_edited"],
                    d["embedding_clean"],
                    d["embedding_error"],
                    d["audio_path_clean"],
                    d["audio_path_error"],
                    d.get("video_path_clean"), # Dùng .get() để an toàn nếu key không tồn tại
                    d.get("video_path_error"),
                    d.get("label") # Thêm label
                )
                
                # Truyền tuple vào lệnh execute
                cur.execute(query, data_tuple)
                
                # Lấy lại id và start_ms từ kết quả RETURNING
                word_id, start_ms = cur.fetchone()
                id_map[start_ms] = word_id
                
        conn.commit()
        logging.info(f"Đã chèn {len(id_map)} bản ghi vào 'words' và lấy ID.")
        return id_map
    except Exception as e:
        logging.error(f"Lỗi khi chèn vào 'words' và lấy ID: {e}")
        conn.rollback()
        return {}
def insert_word_slices(conn, slices_data: list):
    """
    Chèn dữ liệu sliding window.
    slices_data: list of tuples (word_id, source_type, slice_index, embedding)
    """
    if not slices_data: return False
    
    query = """
        INSERT INTO "word_slices" (word_id, source_type, slice_index, embedding)
        VALUES %s
    """
    try:
        with conn.cursor() as cur:
            execute_values(cur, query, slices_data, page_size=500) # Dùng page_size cho list lớn
        conn.commit()
        logging.info(f"Đã chèn {len(slices_data)} lát cắt vào 'word_slices'.")
        return True
    except Exception as e:
        logging.error(f"Lỗi insert word_slices: {e}")
        conn.rollback()
        return False

# def insert_chunk_data(conn, data_tuples: list):
#     """
#     Chèn một danh sách các audio chunk vào CSDL một cách hiệu quả.
#     data_tuples là một list của các tuple, ví dụ:
#     [(source, word, start_ms, end_ms, label, path, vector), ...]
#     """
#     if not data_tuples:
#         return False
    
#     # The repository now uses the normalized schema (sources, sentences, words, anomalies).
#     # Map legacy tuples (source, word, start_ms, end_ms, label, path, vector)
#     # into the `words` table. We will:
#     #  - ensure a `source` exists (get_or_create_source)
#     #  - ensure a `sentence` exists for the time span (create a synthetic sentence if needed)
#     #  - insert or upsert a `words` row that may contain embedding_clean and/or embedding_error

#     # Group incoming tuples by (source, start_ms, end_ms, word_text)
#     groups = {}
#     for item in data_tuples:
#         try:
#             source, word, start_ms, end_ms, label, path, vector = item
#         except Exception:
#             logging.warning("Dữ liệu không có định dạng mong đợi, bỏ qua một bản ghi.")
#             continue
#         key = (source, int(start_ms), int(end_ms), word)
#         entry = groups.get(key, {
#             'source': source,
#             'word': word,
#             'start_ms': int(start_ms),
#             'end_ms': int(end_ms),
#             'audio_path_clean': None,
#             'audio_path_error': None,
#             'embedding_clean': None,
#             'embedding_error': None
#         })
#         if label and label.lower() == 'clean':
#             entry['audio_path_clean'] = path
#             entry['embedding_clean'] = vector
#         else:
#             entry['audio_path_error'] = path
#             entry['embedding_error'] = vector
#         groups[key] = entry

#     # Prepare rows to insert into words. We need sentence_id for each; create synthetic sentence if needed.
#     rows_to_insert = []
#     for key, e in groups.items():
#         source_name = e['source']
#         # Ensure source exists
#         source_id = get_or_create_source(conn, source_name)
#         if source_id is None:
#             logging.error(f"Không thể xác định source_id cho {source_name}, bỏ qua nhóm {key}.")
#             continue

#         # Find or create a sentence covering this interval. For simplicity create a synthetic sentence.
#         try:
#             with conn.cursor() as cur:
#                 cur.execute(
#                     'SELECT id FROM "sentences" WHERE source_id = %s AND start_time_ms = %s AND end_time_ms = %s',
#                     (source_id, e['start_ms'], e['end_ms'])
#                 )
#                 res = cur.fetchone()
#                 if res:
#                     sentence_id = res[0]
#                 else:
#                     cur.execute(
#                         'INSERT INTO "sentences" (source_id, transcript, start_time_ms, end_time_ms) VALUES (%s, %s, %s, %s) RETURNING id',
#                         (source_id, None, e['start_ms'], e['end_ms'])
#                     )
#                     sentence_id = cur.fetchone()[0]
#                     conn.commit()
#         except Exception as ex:
#             logging.error(f"Lỗi khi tìm/tạo sentence cho source {source_name}: {ex}")
#             conn.rollback()
#             continue

#         rows_to_insert.append((
#             sentence_id,
#             e['word'],
#             'und',
#             e['start_ms'],
#             e['end_ms'],
#             e['embedding_clean'],
#             e['embedding_error'],
#             e['audio_path_clean'],
#             e['audio_path_error'],
#             None,
#             None
#         ))

#     if not rows_to_insert:
#         logging.error("Không có bản ghi hợp lệ để chèn vào 'words'.")
#         return False

#     try:
#         with conn.cursor() as cur:
#             execute_values(cur, """
#                 INSERT INTO "words" (
#                     sentence_id, word_text, language, start_time_ms_edited, end_time_ms_edited,
#                     embedding_clean, embedding_error, audio_path_clean, audio_path_error,
#                     video_path_clean, video_path_error
#                 ) VALUES %s
#             """, rows_to_insert)
#         conn.commit()
#         logging.info(f"Đã chèn thành công {len(rows_to_insert)} bản ghi vào bảng 'words'.")
#         return True
#     except Exception as e:
#         logging.error(f"Lỗi khi chèn dữ liệu vào bảng 'words': {e}")
#         conn.rollback()
#         return False

def get_or_create_sentence(conn, source_id: int, transcript: str, start_ms: int, end_ms: int) -> int | None:
    """
    Tìm một 'sentence' theo source_id và transcript, nếu không có thì tạo mới.
    Trong giai đoạn demo, nó dùng để tạo một 'câu cha' giả cho cả video.
    
    Args:
        conn: Đối tượng kết nối CSDL.
        source_id (int): ID của video nguồn từ bảng 'sources'.
        transcript (str): Nội dung văn bản của câu (trong demo là một chuỗi định danh).
        start_ms (int): Thời gian bắt đầu giả.
        end_ms (int): Thời gian kết thúc giả.

    Returns:
        int | None: ID của bản ghi 'sentence', hoặc None nếu có lỗi.
    """
    try:
        with conn.cursor() as cur:
            # 1. Thử tìm xem 'câu cha' giả này đã tồn tại cho video này chưa.
            #    Chúng ta dùng transcript làm khóa định danh duy nhất cho sự tồn tại.
            cur.execute('SELECT id FROM "sentences" WHERE source_id = %s AND transcript = %s', (source_id, transcript))
            result = cur.fetchone()
            
            # 2. Nếu đã tồn tại, trả về ID của nó
            if result:
                sentence_id = result[0]
                logging.debug(f"Sentence placeholder đã tồn tại cho source {source_id} với id: {sentence_id}")
                return sentence_id
            # 3. Nếu chưa tồn tại, tạo mới
            else:
                logging.info(f"Đang tạo sentence placeholder cho source_id {source_id}...")
                cur.execute(
                    'INSERT INTO "sentences" (source_id, transcript, start_time_ms, end_time_ms) VALUES (%s, %s, %s, %s) RETURNING id',
                    (source_id, transcript, start_ms, end_ms)
                )
                sentence_id = cur.fetchone()[0]
                conn.commit() # Commit transaction để lưu bản ghi mới
                logging.info(f"Đã tạo sentence placeholder với id: {sentence_id}")
                return sentence_id
    except Exception as e:
        logging.error(f"Lỗi khi get/create sentence: {e}")
        conn.rollback() # Rollback nếu có lỗi
        return None
    
def insert_edit_events(conn, events_data: list):
    """
    Chèn hàng loạt các sự kiện chỉnh sửa vào bảng 'edit_events'.
    """
    if not events_data:
        return False
    
    query = """
        INSERT INTO "edit_events" (
            source_id, start_ms, end_ms, event_source, event_type,
            embedding_clean, embedding_error, details, 
            audio_path_clean, audio_path_error
        ) VALUES %s
    """
    try:
        with conn.cursor() as cur:
            execute_values(cur, query, events_data, page_size=200)
        conn.commit()
        logging.info(f"Đã chèn thành công {len(events_data)} bản ghi vào 'edit_events'.")
        return True
    except Exception as e:
        logging.error(f"Lỗi khi chèn dữ liệu vào 'edit_events': {e}")
        conn.rollback()
        return False
