# scripts/check_db.py

import os
import sys
import logging
import random
import numpy as np
from dotenv import load_dotenv

# Fix import path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.database import db_manager

# --- Cấu hình ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s', force=True)
# Số lượng mẫu ngẫu nhiên để kiểm tra
SAMPLE_SIZE = 5 

def print_header(title):
    """Hàm tiện ích để in tiêu đề cho đẹp."""
    print("\n" + "="*70)
    print(f"      {title.upper()}")
    print("="*70)

def check_db_v3():
    """
    Thực hiện một chuỗi các kiểm tra toàn diện trên CSDL v3.0.
    """
    load_dotenv()
    conn = db_manager.get_db_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            # --- KIỂM TRA 1: TỔNG QUAN ---
            print_header("Kiểm tra Tổng quan (Overview)")
            
            cur.execute('SELECT COUNT(*) FROM "sources";')
            source_count = cur.fetchone()[0]
            logging.info(f"✅ Bảng 'sources': Tìm thấy {source_count} bản ghi.")

            cur.execute('SELECT COUNT(*) FROM "edit_events";')
            event_count = cur.fetchone()[0]
            logging.info(f"✅ Bảng 'edit_events': Tìm thấy {event_count} bản ghi.")

            cur.execute('SELECT COUNT(*) FROM "words";')
            word_count = cur.fetchone()[0]
            logging.info(f"✅ Bảng 'words': Tìm thấy {word_count} bản ghi.")

            if source_count == 0 or event_count == 0:
                logging.warning("CSDL có vẻ trống. Các kiểm tra chi tiết có thể bị bỏ qua.")
                return

            # --- KIỂM TRA 2: TÍNH TOÀN VẸN CỦA 'edit_events' ---
            print_header(f"Kiểm tra chi tiết {SAMPLE_SIZE} sự kiện ngẫu nhiên trong 'edit_events'")
            
            cur.execute(f'SELECT id, event_type, details FROM "edit_events" ORDER BY RANDOM() LIMIT {SAMPLE_SIZE};')
            sample_events = cur.fetchall()
            
            for event in sample_events:
                event_id, event_type, details = event
                # Kiểm tra xem embedding có rỗng không
                cur.execute('SELECT embedding_clean IS NOT NULL, embedding_error IS NOT NULL FROM "edit_events" WHERE id = %s;', (event_id,))
                has_clean, has_error = cur.fetchone()
                
                status = "✅ OK"
                if not (has_clean and has_error):
                    status = "❌ LỖI: Thiếu embedding"
                    
                logging.info(f" - Event ID {event_id}: Type='{event_type}', Details='{details}', Embeddings Status: {status}")

            # Thống kê các loại sự kiện
            print_header("Thống kê các loại sự kiện (event_type)")
            cur.execute('SELECT event_type, COUNT(*) as count FROM "edit_events" GROUP BY event_type ORDER BY count DESC;')
            event_distribution = cur.fetchall()
            for event_type, count in event_distribution:
                logging.info(f" - {event_type}: {count} lần")


            # --- KIỂM TRA 3: TÍNH TOÀN VẸN CỦA 'words' ---
            print_header(f"Kiểm tra chi tiết {SAMPLE_SIZE} từ ngẫu nhiên trong 'words'")
            
            cur.execute(f'SELECT id, word_text, parent_event_id FROM "words" ORDER BY RANDOM() LIMIT {SAMPLE_SIZE};')
            sample_words = cur.fetchall()

            for word in sample_words:
                word_id, word_text, parent_event_id = word
                
                # Kiểm tra liên kết khóa ngoại
                cur.execute('SELECT COUNT(*) FROM "edit_events" WHERE id = %s;', (parent_event_id,))
                parent_exists = cur.fetchone()[0] > 0
                
                status = "✅ OK"
                if not parent_exists:
                    status = f"❌ LỖI: parent_event_id {parent_event_id} không hợp lệ!"
                    
                logging.info(f" - Word ID {word_id}: Text='{word_text}', Parent Event Link Status: {status}")


            # --- KIỂM TRA 4: KIỂM TRA LOGIC VECTOR ---
            print_header("Kiểm tra logic Vector")

            # Lấy một embedding 'clean' và một embedding 'error' từ cùng một event
            cur.execute("""
                SELECT embedding_clean, embedding_error 
                FROM "edit_events" 
                WHERE embedding_clean IS NOT NULL AND embedding_error IS NOT NULL 
                ORDER BY RANDOM() LIMIT 1;
            """)
            sample_vectors = cur.fetchone()
            
            if sample_vectors:
                vec_clean, vec_error = np.array(sample_vectors[0]), np.array(sample_vectors[1])
                
                # Test 1: Khoảng cách tự so sánh phải gần 0
                self_distance = 1 - np.dot(vec_clean, vec_clean) / (np.linalg.norm(vec_clean) * np.linalg.norm(vec_clean))
                logging.info(f"  - Khoảng cách Tự so sánh (Self-distance): {self_distance:.6f} (Kỳ vọng: ~0)")
                if self_distance > 1e-5:
                     logging.error("   -> Lỗi logic vector: Tự so sánh không bằng 0.")

                # Test 2: Khoảng cách clean/error phải lớn hơn 0
                ce_distance = 1 - np.dot(vec_clean, vec_error) / (np.linalg.norm(vec_clean) * np.linalg.norm(vec_error))
                logging.info(f"  - Khoảng cách Clean/Error (C/E distance): {ce_distance:.4f} (Kỳ vọng: > 0)")
                if ce_distance <= 0:
                    logging.warning("   -> Cảnh báo: Khoảng cách Clean/Error quá nhỏ hoặc âm.")
            else:
                logging.warning("Không tìm thấy cặp vector nào để kiểm tra logic.")


    except Exception as e:
        logging.error(f"Lỗi khi truy vấn CSDL: {e}")
    finally:
        if conn:
            conn.close()
            logging.info("Đã đóng kết nối CSDL.")

if __name__ == "__main__":
    check_db_v3()