# scripts/analyze_events_db.py

import os
import sys
import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import json

# Fix import path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.database import db_manager

# Cấu hình
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s', force=True)
load_dotenv()
OUTPUT_DIR = "analysis_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def analyze_events_database():
    """
    Phân tích và trực quan hóa dữ liệu từ bảng 'edit_events'
    để chứng minh hiệu quả của model embedding.
    """
    conn = db_manager.get_db_connection()
    if not conn:
        return

    try:
        # 1. Tải dữ liệu từ CSDL
        logging.info("Đang tải dữ liệu từ bảng 'edit_events'...")
        query = 'SELECT event_type, details, embedding_clean, embedding_error FROM "edit_events"'
        df = pd.read_sql_query(query, conn)
        logging.info(f"Đã tải thành công {len(df)} bản ghi sự kiện.")

        if df.empty:
            logging.warning("Không có dữ liệu trong bảng 'edit_events' để phân tích.")
            return

        # 2. Tiền xử lý và Kỹ thuật Đặc trưng
        logging.info("Đang tiền xử lý dữ liệu và tính toán các vector đặc trưng...")

        # Loại bỏ các dòng không có embedding
        df.dropna(subset=['embedding_clean', 'embedding_error'], inplace=True)
        
        # Tạo cột event_group để nhóm các filter phụ
        df['event_group'] = df['event_type'].apply(lambda x: 'audio_filter' if x.startswith('filter-') else x)
        
        # Chuyển đổi embedding
        embeds_clean = np.array(df['embedding_clean'].tolist())
        embeds_error = np.array(df['embedding_error'].tolist())

        # --- ĐÂY LÀ CÁC ĐẶC TRƯNG CHÚNG TA SẼ PHÂN TÍCH ---
        # a) Vector Khác biệt (Dấu hiệu của "hành động sửa chữa")
        df['diff_vector'] = list(embeds_error - embeds_clean)
        
        # b) Khoảng cách Cosine (Mức độ khác biệt)
        dot_product = np.sum(embeds_clean * embeds_error, axis=1)
        norm_clean = np.linalg.norm(embeds_clean, axis=1)
        norm_error = np.linalg.norm(embeds_error, axis=1)
        cosine_similarity = dot_product / (norm_clean * norm_error + 1e-9)
        df['distance'] = 1 - cosine_similarity

        # 3. Phân tích Thống kê
        print("\n" + "="*50)
        print("  PHÂN TÍCH KHOẢNG CÁCH COSINE THEO LOẠI SỰ KIỆN")
        print("="*50)
        # In ra khoảng cách trung bình cho mỗi loại lỗi
        # Điều này cho thấy loại lỗi nào gây ra "khác biệt" lớn nhất
        distance_stats = df.groupby('event_group')['distance'].describe()
        print(distance_stats)
        print("="*50)


        # 4. Trực quan hóa
        logging.info("Đang tạo các biểu đồ trực quan hóa...")

        # --- BIỂU ĐỒ 1: Mức độ khác biệt của từng loại lỗi ---
        plt.figure(figsize=(15, 8))
        sns.boxplot(x='distance', y='event_group', data=df, orient='h')
        plt.title('Phân bố Khoảng cách Cosine theo Từng loại Sự kiện Chỉnh sửa', fontsize=16)
        plt.xlabel('Cosine Distance (0 = Giống, 1 = Khác)', fontsize=12)
        plt.ylabel('Loại Sự kiện', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'event_distance_by_type.png'))
        logging.info(f"Đã lưu biểu đồ phân bố khoảng cách tại: {OUTPUT_DIR}/event_distance_by_type.png")

        # --- BIỂU ĐỒ 2: Bản đồ "Dấu hiệu Lỗi" (PCA) ---
        # Sử dụng PCA để xem các "diff_vector" có tụ lại thành cụm không
        logging.info("Đang thực hiện PCA trên các vector khác biệt...")
        
        # Chỉ lấy các nhóm có nhiều hơn 1 mẫu để tránh lỗi
        valid_groups = df['event_group'].value_counts()
        valid_groups = valid_groups[valid_groups > 1].index
        df_for_pca = df[df['event_group'].isin(valid_groups)]

        if not df_for_pca.empty:
            diff_vectors = np.array(df_for_pca['diff_vector'].tolist())
            pca = PCA(n_components=2)
            principal_components = pca.fit_transform(diff_vectors)
            
            df_pca = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
            df_pca['Error Type'] = df_for_pca['event_group'].values
            
            plt.figure(figsize=(16, 12))
            sns.scatterplot(
                x='PC1', y='PC2',
                hue='Error Type',
                data=df_pca,
                alpha=0.7,
                s=50, # Kích thước điểm
                palette='viridis' # Bảng màu
            )
            plt.title('Bản đồ "Dấu hiệu Lỗi" (PCA 2D của các Vector Khác biệt)', fontsize=18)
            plt.xlabel('Thành phần Chính 1 (Principal Component 1)', fontsize=14)
            plt.ylabel('Thành phần Chính 2 (Principal Component 2)', fontsize=14)
            plt.legend(title='Loại Sự kiện')
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            plt.savefig(os.path.join(OUTPUT_DIR, 'event_diff_vector_pca.png'))
            logging.info(f"Đã lưu biểu đồ PCA tại: {OUTPUT_DIR}/event_diff_vector_pca.png")
            
            # (Tùy chọn) Hiển thị biểu đồ
            plt.show()

    except Exception as e:
        logging.error(f"Lỗi khi phân tích CSDL: {e}", exc_info=True)
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    analyze_events_database()