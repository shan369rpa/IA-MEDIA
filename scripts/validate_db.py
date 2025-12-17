# scripts/validate_db.py

import os
import sys
import logging
import pytest
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from scipy.spatial.distance import cosine

# Fix import path to allow importing from 'src'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.database import db_manager

# --- Cấu hình ---
# Số lượng mẫu ngẫu nhiên để kiểm tra cho mỗi test case
SAMPLE_SIZE = 100
# Thư mục chứa các file chunk (đọc từ .env hoặc mặc định)
load_dotenv()
WORKSPACE_DIR = os.getenv("WORKSPACE_DIR", "./workspace")
CHUNK_DIR = os.path.join(WORKSPACE_DIR, "datasets", "tnh_speech_v0.1")

# --- Fixture của Pytest: Thiết lập kết nối và tải dữ liệu một lần ---

@pytest.fixture(scope="module")
def db_data():
    """
    Fixture này kết nối đến CSDL, tải toàn bộ bảng 'words' vào một DataFrame
    của Pandas và cung cấp nó cho tất cả các bài test.
    Nó cũng đảm bảo kết nối được đóng lại sau khi test xong.
    """
    conn = db_manager.get_db_connection()
    if conn is None:
        pytest.fail("Không thể kết nối đến CSDL. Vui lòng kiểm tra SSH Tunnel và file .env.")
    
    print("\nĐang tải dữ liệu từ CSDL vào bộ nhớ để kiểm tra...")
    try:
        df = pd.read_sql_query('SELECT * FROM "words"', conn)
        print(f"Đã tải {len(df)} bản ghi.")
        yield df # Cung cấp DataFrame cho các hàm test
    finally:
        print("Đóng kết nối CSDL.")
        conn.close()

# --- Nhóm Test A: Kiểm tra Tính toàn vẹn Dữ liệu ---

def test_A1_file_paths_exist(db_data):
    """
    Test Case A1: Kiểm tra xem các đường dẫn file trong CSDL có thực sự tồn tại trên đĩa không.
    """
    if db_data.empty:
        pytest.skip("Bỏ qua test vì không có dữ liệu trong CSDL.")
    
    # Lấy một mẫu ngẫu nhiên
    sample_df = db_data.sample(n=min(SAMPLE_SIZE, len(db_data)), random_state=42)
    
    missing_files = []
    for index, row in sample_df.iterrows():
        clean_path = os.path.join(CHUNK_DIR, row['audio_path_clean'])
        error_path = os.path.join(CHUNK_DIR, row['audio_path_error'])
        if not os.path.exists(clean_path):
            missing_files.append(clean_path)
        if not os.path.exists(error_path):
            missing_files.append(error_path)
            
    assert not missing_files, f"Không tìm thấy các file sau: {missing_files[:5]}"

def test_A2_vector_dimensions_are_correct(db_data):
    """
    Test Case A2: Kiểm tra xem tất cả các embedding có đúng kích thước (192) không.
    """
    if db_data.empty:
        pytest.skip("Bỏ qua test vì không có dữ liệu trong CSDL.")
    
    # Lấy một mẫu ngẫu nhiên
    sample_df = db_data.sample(n=min(SAMPLE_SIZE, len(db_data)), random_state=42)
    
    incorrect_dims = []
    for index, row in sample_df.iterrows():
        if len(row['embedding_clean']) != 192:
            incorrect_dims.append(f"clean_id_{row['id']}")
        if len(row['embedding_error']) != 192:
            incorrect_dims.append(f"error_id_{row['id']}")
            
    assert not incorrect_dims, f"Các vector sau có kích thước sai: {incorrect_dims}"

# --- Nhóm Test B: Kiểm tra Logic Tương đồng ---

def test_B1_self_similarity_is_zero(db_data):
    """
    Test Case B1: Khoảng cách từ một vector đến chính nó phải bằng 0.
    """
    if db_data.empty:
        pytest.skip("Bỏ qua test vì không có dữ liệu trong CSDL.")
        
    sample_row = db_data.sample(n=1, random_state=42).iloc[0]
    vec = np.array(sample_row['embedding_clean'])
    
    distance = cosine(vec, vec)
    
    assert distance < 1e-6, f"Khoảng cách tự so sánh phải gần 0, nhưng lại là {distance}"

def test_B2_intra_word_similarity_is_low(db_data):
    """
    Test Case B2: Khoảng cách giữa hai lần xuất hiện 'clean' của cùng một từ phải nhỏ.
    """
    # Tìm các từ xuất hiện nhiều hơn 1 lần
    word_counts = db_data['word_text'].value_counts()
    repeated_words = word_counts[word_counts > 1].index
    
    if len(repeated_words) == 0:
        pytest.skip("Bỏ qua test vì không có từ nào được lặp lại trong tập dữ liệu.")
        
    # Chọn từ đầu tiên trong danh sách lặp lại
    target_word = repeated_words[0]
    
    two_samples = db_data[db_data['word_text'] == target_word].head(2)
    vec_a = np.array(two_samples.iloc[0]['embedding_clean'])
    vec_b = np.array(two_samples.iloc[1]['embedding_clean'])
    
    distance = cosine(vec_a, vec_b)
    
    print(f"Kiểm tra khoảng cách giữa 2 lần nói từ '{target_word}': {distance:.4f}")
    assert distance < 0.3, f"Khoảng cách giữa 2 lần nói cùng một từ '{target_word}' quá lớn ({distance:.4f}), kỳ vọng < 0.3"

def test_B3_inter_word_dissimilarity_is_high(db_data):
    """
    Test Case B3: Khoảng cách giữa hai từ 'clean' khác nhau phải lớn.
    """
    if len(db_data) < 2:
        pytest.skip("Không đủ dữ liệu để so sánh 2 từ khác nhau.")
        
    # Lấy 2 từ khác nhau một cách ngẫu nhiên
    two_samples = db_data.sample(n=2, random_state=42)
    word_a = two_samples.iloc[0]['word_text']
    word_b = two_samples.iloc[1]['word_text']
    
    # Đảm bảo chúng thực sự là 2 từ khác nhau
    if word_a == word_b:
        pytest.skip("Ngẫu nhiên chọn trúng 2 từ giống nhau, bỏ qua test.")
        
    vec_a = np.array(two_samples.iloc[0]['embedding_clean'])
    vec_b = np.array(two_samples.iloc[1]['embedding_clean'])
    
    distance = cosine(vec_a, vec_b)
    
    print(f"Kiểm tra khoảng cách giữa từ '{word_a}' và '{word_b}': {distance:.4f}")
    assert distance > 0.3, f"Khoảng cách giữa 2 từ khác nhau '{word_a}' và '{word_b}' quá nhỏ ({distance:.4f}), kỳ vọng > 0.3"

def test_B4_error_clean_divergence_exists(db_data):
    """
    Test Case B4: Khoảng cách giữa cặp clean/error của cùng một từ phải lớn hơn 0.
    """
    if db_data.empty:
        pytest.skip("Bỏ qua test vì không có dữ liệu trong CSDL.")

    sample_df = db_data.sample(n=min(SAMPLE_SIZE, len(db_data)), random_state=42)
    
    distances = []
    for index, row in sample_df.iterrows():
        vec_clean = np.array(row['embedding_clean'])
        vec_error = np.array(row['embedding_error'])
        distances.append(cosine(vec_clean, vec_error))
        
    avg_distance = np.mean(distances)
    
    print(f"Khoảng cách trung bình giữa các cặp clean/error: {avg_distance:.4f}")
    assert avg_distance > 0.1, f"Khoảng cách trung bình giữa clean/error quá nhỏ ({avg_distance:.4f}), kỳ vọng > 0.1"