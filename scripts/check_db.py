# scripts/check_db.py
import sys

from src.database.db_manager import get_db_connection

def main():
    conn = get_db_connection()
    if not conn:
        print("KẾT NỐI THẤT BẠI (get_db_connection trả về None). Kiểm tra biến môi trường và DB.", file=sys.stderr)
        sys.exit(2)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            val = cur.fetchone()
            print("SELECT 1 trả về:", val)
            print("KẾT NỐI OK.")
    except Exception as e:
        print("Kết nối nhưng query test thất bại:", e, file=sys.stderr)
        sys.exit(3)
    finally:
        conn.close()

if __name__ == '__main__':
    main()