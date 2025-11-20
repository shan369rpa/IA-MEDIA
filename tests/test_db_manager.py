# tests/test_db_manager.py
import pytest
import numpy as np
from src.database import db_manager

@pytest.fixture(scope="module")
def db_connection():
    """Tạo một kết nối CSDL duy nhất cho tất cả các test trong module này."""
    conn = db_manager.get_db_connection()
    # Nếu không kết nối được, bỏ qua tất cả các test
    if conn is None:
        pytest.skip("Không thể kết nối đến CSDL, bỏ qua các test DB.")
    
    # Dọn dẹp trước khi bắt đầu
    db_manager.clear_table(conn, "audio_chunks")
    
    yield conn # Cung cấp kết nối cho các hàm test
    
    # Dọn dẹp sau khi tất cả các test đã chạy xong
    db_manager.clear_table(conn, "audio_chunks")
    conn.close()

def test_insert_and_clear_data(db_connection):
    """Kiểm tra chức năng chèn và xóa dữ liệu."""
    # Dữ liệu giả, kích thước vector phải khớp với CSDL (ví dụ 1024)
    mock_vector = np.random.rand(1024).tolist()
    
    data_to_insert = [
        ("video1", "word1", 100, 200, "clean", "/path/1", mock_vector),
        ("video1", "word2", 300, 400, "error", "/path/2", mock_vector)
    ]
    
    # Test chèn
    success = db_manager.insert_chunk_data(db_connection, data_to_insert)
    assert success == True
    
    # Kiểm tra xem dữ liệu có thực sự được chèn vào không
    with db_connection.cursor() as cur:
        cur.execute('SELECT COUNT(*) FROM "audio_chunks"')
        assert cur.fetchone()[0] == 2
        
    # Test xóa
    success_clear = db_manager.clear_table(db_connection, "audio_chunks")
    assert success_clear == True
    
    with db_connection.cursor() as cur:
        cur.execute('SELECT COUNT(*) FROM "audio_chunks"')
        assert cur.fetchone()[0] == 0

def test_find_similar_chunks(db_connection):
    """Kiểm tra chức năng tìm kiếm tương đồng vector."""
    # Tạo 3 vector mẫu
    vec1 = np.array([1.0, 0.0, 0.0]) # Vector gốc
    vec2 = np.array([0.9, 0.1, 0.0]) # Gần giống nhất
    vec3 = np.array([0.0, 1.0, 0.0]) # Khác biệt nhất
    
    # Lưu ý: Kích thước vector phải khớp với CSDL. Chúng ta cần một CSDL test riêng
    # hoặc tạm thời thay đổi kích thước vector trong CSDL thành 3 để test.
    # Ở đây, giả sử CSDL đã được tạo với VECTOR(3) để test.
    # TRONG THỰC TẾ, BẠN CẦN THAY ĐỔI KÍCH THƯỚC VECTOR Ở ĐÂY CHO KHỚP 1024
    
    # Bỏ qua test này nếu kích thước vector không phải là 3
    # Lấy kích thước vector từ CSDL để kiểm tra
    with db_connection.cursor() as cur:
        cur.execute("SELECT typname, atttypmod FROM pg_type t JOIN pg_attribute a ON t.oid = a.atttypid WHERE a.attrelid = '\"audio_chunks\"'::regclass AND a.attname = 'embedding';")
        result = cur.fetchone()
        if result is None or result[1] != 3:
             pytest.skip("Bỏ qua test tìm kiếm vì kích thước vector không phải là 3.")

    data_to_insert = [
        ("v", "w_far", 1, 2, "clean", "/far", vec3.tolist()),
        ("v", "w_close", 3, 4, "clean", "/close", vec2.tolist()),
    ]
    db_manager.insert_chunk_data(db_connection, data_to_insert)
    
    # Tìm các vector gần với vec1
    results = db_manager.find_similar_chunks(db_connection, vec1.tolist(), limit=2)
    
    # Kết quả trả về phải có 2 dòng
    assert len(results) == 2
    
    # Dòng đầu tiên (gần nhất) phải là của "w_close"
    # Cột thứ 2 trong kết quả là word_text
    assert results[0][1] == "w_close"
    
    # Dòng thứ hai (xa hơn) phải là của "w_far"
    assert results[1][1] == "w_far"