# scripts/train_classifier.py
import os
import sys
import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib # Dùng để lưu model
from dotenv import load_dotenv

# Fix import
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.database import db_manager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

def train_model():
    """
    Tải dữ liệu, huấn luyện mô hình phân loại lỗi và lưu lại.
    """
    conn = db_manager.get_db_connection()
    if not conn:
        return

    try:
        # 1. Tải dữ liệu đã được gán nhãn từ CSDL
        logging.info("Đang tải dữ liệu từ CSDL...")
        # Lấy các cặp embedding và nhãn lỗi chi tiết
        query = """
            SELECT w.embedding_clean, w.embedding_error, a.anomaly_type
            FROM words w
            JOIN anomalies a ON w.id = a.related_word_id
            WHERE a.anomaly_type IS NOT NULL;
        """
        # Lưu ý: Cần có logic để gán nhãn "error_pronunciation" cho các từ không có trong bảng anomalies
        # Để đơn giản cho demo, ta tạm thời chỉ dùng các lỗi kỹ thuật đã được gán nhãn.
        # Hoặc một cách khác là đọc từ metadata.csv
        
        # --- CÁCH ĐƠN GIẢN HƠN: ĐỌC TỪ CSV ---
        workspace_dir = os.getenv("WORKSPACE_DIR", "./workspace")
        metadata_path = os.path.join(workspace_dir, "datasets/tnh_speech_v0.1/metadata.csv")
        if not os.path.exists(metadata_path):
            logging.error(f"Không tìm thấy metadata.csv tại {metadata_path}")
            return
            
        df = pd.read_csv(metadata_path)
        error_df = df[df['label'].str.startswith('error')].copy()
        logging.info(f"Đã tìm thấy {len(error_df)} bản ghi lỗi để huấn luyện.")

        # 2. Chuẩn bị dữ liệu huấn luyện (X, y)
        logging.info("Đang chuẩn bị dữ liệu huấn luyện...")
        # Tải lại các vector từ DB hoặc tính toán lại nếu cần
        # Để demo, chúng ta sẽ cần chạy vectorize.py trước để có dữ liệu trong DB
        
        # --- GIẢ ĐỊNH DỮ LIỆU ĐÃ CÓ TRONG DB ---
        query = 'SELECT embedding_clean, embedding_error, label FROM "words" WHERE label LIKE \'error_%%\' '
        train_df = pd.read_sql_query(query, conn)
        
        if train_df.empty:
            logging.error("Không có dữ liệu lỗi trong CSDL để huấn luyện. Vui lòng chạy vectorize.py trước.")
            return

        embeds_clean = np.array(train_df['embedding_clean'].tolist())
        embeds_error = np.array(train_df['embedding_error'].tolist())

        # Input (X) là vector khác biệt
        X = embeds_error - embeds_clean
        # Output (y) là nhãn lỗi
        y = train_df['label']

        logging.info(f"Tập dữ liệu có {X.shape[0]} mẫu, {X.shape[1]} chiều.")
        logging.info(f"Phân bố các nhãn:\n{y.value_counts()}")

        # 3. Chia dữ liệu thành tập train và test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
        logging.info(f"Train set: {len(X_train)} mẫu, Test set: {len(X_test)} mẫu.")

        # 4. Huấn luyện mô hình
        logging.info("Đang huấn luyện mô hình KNeighborsClassifier...")
        # KNN là một lựa chọn tốt, đơn giản và hiệu quả cho bài toán phân loại vector
        model = KNeighborsClassifier(n_neighbors=5, metric='cosine')
        model.fit(X_train, y_train)
        logging.info("Huấn luyện hoàn tất.")

        # 5. Đánh giá mô hình
        logging.info("Đang đánh giá mô hình trên tập test...")
        y_pred = model.predict(X_test)
        
        print("\n--- BÁO CÁO PHÂN LOẠI ---")
        print(classification_report(y_test, y_pred))
        print("\n--- MA TRẬN NHẦM LẪN ---")
        print(confusion_matrix(y_test, y_pred))

        # 6. Lưu mô hình
        model_path = "error_classifier.pkl"
        joblib.dump(model, model_path)
        logging.info(f"Đã lưu mô hình đã huấn luyện vào file: {model_path}")

    except Exception as e:
        logging.error(f"Lỗi trong quá trình huấn luyện: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    load_dotenv()
    train_model()