# scripts/check_db.py
import os
import sys
from dotenv import load_dotenv

# Fix path import
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.database.db_manager import get_db_connection

def main():
    load_dotenv()
    print("--- ĐANG KIỂM TRA DỮ LIỆU TRONG DB ---")
    conn = get_db_connection()
    if not conn:
        print("❌ Kết nối thất bại.")
        return

    try:
        with conn.cursor() as cur:
            # 1. Check Sources
            cur.execute('SELECT COUNT(*) FROM "sources"')
            source_count = cur.fetchone()[0]
            print(f"✅ Bảng 'sources': {source_count} bản ghi.")

            # 2. Check Words
            cur.execute('SELECT COUNT(*) FROM "words"')
            word_count = cur.fetchone()[0]
            print(f"✅ Bảng 'words'  : {word_count} bản ghi.")

            if word_count > 0:
                # 3. Check Vector Integrity
                cur.execute('SELECT word_text, embedding_clean IS NOT NULL FROM "words" LIMIT 1')
                sample = cur.fetchone()
                print(f"🔍 Mẫu dữ liệu: Từ '{sample[0]}' - Có vector clean? {'CÓ' if sample[1] else 'KHÔNG'}")
            else:
                print("⚠️ CẢNH BÁO: Bảng words trống trơn!")

    except Exception as e:
        print(f"❌ Lỗi truy vấn: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    main()