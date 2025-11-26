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
    
    # Dọn dẹp trước khi bắt đầu (bảng words theo schema hiện tại)
    db_manager.clear_table(conn, "words")
    
    yield conn # Cung cấp kết nối cho các hàm test
    
    # Dọn dẹp sau khi tất cả các test đã chạy xong
    db_manager.clear_table(conn, "audio_chunks")
    conn.close()

def test_insert_and_clear_data(db_connection):
    """Kiểm tra chức năng chèn và xóa dữ liệu."""
    # Prepare 192-dim mock vectors to match VECTOR(192) in schema
    mock_vector = np.random.rand(192).tolist()

    # Prepare data tuples compatible with insert_words_data
    data_to_insert = [
        (
            1, # sentence_id
            "word1",
            "vie",
            100,
            200,
            mock_vector,
            None,
            "/path/clean1.wav",
            None,
            "/path/video_clean1.mp4",
            None
        ),
        (
            1,
            "word2",
            "vie",
            300,
            400,
            mock_vector,
            None,
            "/path/clean2.wav",
            None,
            "/path/video_clean2.mp4",
            None
        )
    ]

    # Test chèn
    success = db_manager.insert_words_data(db_connection, data_to_insert)
    assert success == True

    # Kiểm tra xem dữ liệu có thực sự được chèn vào không
    with db_connection.cursor() as cur:
        cur.execute('SELECT COUNT(*) FROM "words"')
        assert cur.fetchone()[0] == 2

    # Test xóa
    success_clear = db_manager.clear_table(db_connection, "words")
    assert success_clear == True

    with db_connection.cursor() as cur:
        cur.execute('SELECT COUNT(*) FROM "words"')
        assert cur.fetchone()[0] == 0

def test_find_similar_chunks(db_connection):
    """Kiểm tra chức năng tìm kiếm tương đồng vector."""
    # Create 3 sample vectors of dimension 192
    vec1 = np.zeros(192)
    vec2 = np.concatenate(([0.9, 0.1], np.zeros(190)))
    vec3 = np.concatenate(([0.0, 1.0], np.zeros(190)))

    # Insert two records into `words` using insert_words_data
    data_to_insert = [
        (
            1, 'w_far', 'vie', 1, 2, vec3.tolist(), None, '/far.wav', None, '/far.mp4', None
        ),
        (
            1, 'w_close', 'vie', 3, 4, vec2.tolist(), None, '/close.wav', None, '/close.mp4', None
        ),
    ]
    db_manager.insert_words_data(db_connection, data_to_insert)

    # Find vectors similar to vec1
    results = db_manager.find_similar_words(db_connection, vec1.tolist(), limit=2)

    # Results must have 2 rows
    assert len(results) == 2

    # First row (closest) should be 'w_close'
    assert results[0][1] == 'w_close'

    # Second row should be 'w_far'
    assert results[1][1] == 'w_far'