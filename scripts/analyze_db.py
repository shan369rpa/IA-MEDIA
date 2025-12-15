# scripts/analyze_db.py

import os
import sys
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from sklearn.decomposition import PCA # Dùng để giảm chiều dữ liệu và trực quan hóa

# Fix lỗi import
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.database import db_manager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

def analyze_database():
    """
    Phân tích dữ liệu trong CSDL:
    1. Lấy tất cả các cặp embedding clean/error.
    2. Tính toán vector khác biệt và khoảng cách.
    3. Trực quan hóa sự phân bố của dữ liệu.
    """
    load_dotenv()
    conn = db_manager.get_db_connection()
    if not conn:
        return

    try:
        # 1. Tải dữ liệu từ CSDL vào DataFrame của Pandas
        logging.info("Đang tải dữ liệu embedding từ bảng 'words'...")
        # Chúng ta cũng cần lấy các nhãn lỗi chi tiết sau này, tạm thời chỉ lấy vector
        query = 'SELECT word_text, embedding_clean, embedding_error FROM "words"'
        df = pd.read_sql_query(query, conn)
        logging.info(f"Đã tải thành công {len(df)} bản ghi.")

        if df.empty:
            logging.warning("Không có dữ liệu trong bảng 'words' để phân tích.")
            return

        # 2. Tính toán vector khác biệt và khoảng cách
        logging.info("Đang tính toán vector khác biệt và cosine distance...")
        
        # Chuyển đổi các chuỗi vector từ CSDL thành numpy array
        embeds_clean = np.array(df['embedding_clean'].tolist())
        embeds_error = np.array(df['embedding_error'].tolist())

        # Tính vector hiệu
        diff_vectors = embeds_error - embeds_clean
        df['diff_vector'] = list(diff_vectors)

        # Tính cosine distance
        # distance = 1 - (A . B) / (||A|| * ||B||)
        dot_product = np.sum(embeds_clean * embeds_error, axis=1)
        norm_clean = np.linalg.norm(embeds_clean, axis=1)
        norm_error = np.linalg.norm(embeds_error, axis=1)
        
        # Tránh chia cho 0
        cosine_similarity = dot_product / (norm_clean * norm_error + 1e-9)
        df['distance'] = 1 - cosine_similarity

        # 3. Phân tích thống kê cơ bản
        print("\n--- PHÂN TÍCH THỐNG KÊ KHOẢNG CÁCH (COSINE DISTANCE) ---")
        print(df['distance'].describe())
        print("------------------------------------------------------\n")

        # 4. Trực quan hóa
        logging.info("Đang tạo biểu đồ trực quan hóa...")
        
        # Biểu đồ 1: Phân bố của Khoảng cách (Histogram)
        plt.figure(figsize=(12, 6))
        sns.histplot(df['distance'], bins=50, kde=True)
        plt.title('Phân bố Khoảng cách Cosine giữa Embedding Clean và Error')
        plt.xlabel('Cosine Distance (0=Giống, 1=Khác)')
        plt.ylabel('Số lượng')
        plt.grid(True)
        plt.savefig('distance_distribution.png')
        logging.info("Đã lưu biểu đồ phân bố khoảng cách vào 'distance_distribution.png'")

        # Biểu đồ 2: Trực quan hóa các Vector Khác biệt (dùng PCA)
        # PCA giúp giảm 192 chiều xuống còn 2 chiều để vẽ lên biểu đồ 2D
        logging.info("Đang thực hiện PCA để trực quan hóa các vector khác biệt...")
        pca = PCA(n_components=2)
        principal_components = pca.fit_transform(diff_vectors)
        
        df_pca = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
        df_pca['word_text'] = df['word_text'] # Thêm lại tên từ để tham khảo
        
        plt.figure(figsize=(12, 10))
        sns.scatterplot(x='PC1', y='PC2', data=df_pca, alpha=0.5)
        plt.title('Trực quan hóa các Vector Khác biệt (PCA 2D)')
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.grid(True)
        plt.savefig('diff_vector_pca.png')
        logging.info("Đã lưu biểu đồ PCA của các vector khác biệt vào 'diff_vector_pca.png'")
        
        plt.show() # Hiển thị biểu đồ nếu chạy trong môi trường có giao diện đồ họa

    except Exception as e:
        logging.error(f"Lỗi khi phân tích CSDL: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    analyze_database()