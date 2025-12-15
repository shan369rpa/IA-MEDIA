# scripts/train_classifier.py
import os
import sys
import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
from dotenv import load_dotenv


# Fix import path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.database import db_manager

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s', force=True)

def train_model():
    """
    Tải dữ liệu, huấn luyện mô hình phân loại lỗi và lưu lại.
    """
    load_dotenv()
    conn = db_manager.get_db_connection()
    if not conn:
        return

    try:
        logging.info("Đang tải dữ liệu huấn luyện từ CSDL (bảng 'words')...")
        
        # --- [QUERY ĐÃ ĐƯỢC SỬA LẠI - SIÊU ĐƠN GIẢN] ---
        # Chỉ cần SELECT trực tiếp các cột cần thiết từ bảng 'words'.
        # Không cần JOIN nữa.
        query = """
            SELECT
                embedding_clean,
                embedding_error,
                label
            FROM "words"
            WHERE 
                label LIKE 'error_%%' 
                AND embedding_clean IS NOT NULL 
                AND embedding_error IS NOT NULL;
        """
        
        train_df = pd.read_sql_query(query, conn)
        logging.info(f"Đã tải thành công {len(train_df)} bản ghi lỗi từ CSDL.")

        if train_df.empty:
            logging.error("Không có dữ liệu trong bảng 'words' để huấn luyện. Vui lòng kiểm tra lại kết quả của vectorize.py.")
            return

        # --- PHẦN CÒN LẠI CỦA SCRIPT HOÀN TOÀN GIỮ NGUYÊN ---
        
        logging.info("Đang chuẩn bị dữ liệu (Input: X, Output: y)...")
        
        embeds_clean = np.array(train_df['embedding_clean'].tolist())
        embeds_error = np.array(train_df['embedding_error'].tolist())

        # Input (X) là vector khác biệt
        X = embeds_error - embeds_clean
        # Output (y) là nhãn lỗi
        y = train_df['label']

        logging.info(f"Tập dữ liệu có {X.shape[0]} mẫu, {X.shape[1]} chiều.")
        logging.info(f"Phân bố các nhãn lỗi:\n{y.value_counts()}")

        # Chia dữ liệu...
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
        
        # Huấn luyện...
        model = KNeighborsClassifier(n_neighbors=5, metric='cosine')
        model.fit(X_train, y_train)
        
        # Đánh giá...
        y_pred = model.predict(X_test)
        print("\n--- BÁO CÁO PHÂN LOẠI ---")
        print(classification_report(y_test, y_pred))
        
        # Lưu model...
        model_path = "error_classifier.pkl"
        joblib.dump(model, model_path)
        logging.info(f"Đã lưu mô hình đã huấn luyện vào file: {model_path}")

    except Exception as e:
        logging.error(f"Lỗi trong quá trình huấn luyện: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    train_model()