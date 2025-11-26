# tests/test_fcpxml_parser.py

from src.utils.fcpxml_parser import parse_fcpxml_to_time_map, convert_edited_to_raw_time

FCPXML_FIXTURE_PATH = "tests/fixtures/sample_project.fcpxml"

def test_parse_fcpxml():
    """Kiểm tra xem hàm parser có đọc đúng file XML giả lập không."""
    time_map = parse_fcpxml_to_time_map(FCPXML_FIXTURE_PATH)
    
    # Phải có 2 clip được tìm thấy
    assert len(time_map) == 2
    
    # Kiểm tra clip đầu tiên
    assert time_map[0] == (0.0, 10.0, 50.0) # (edited_start, edited_end, raw_start)
    
    # Kiểm tra clip thứ hai
    assert time_map[1] == (10.0, 25.0, 120.0)

def test_time_conversion():
    """Kiểm tra xem hàm chuyển đổi thời gian có hoạt động chính xác không."""
    time_map = parse_fcpxml_to_time_map(FCPXML_FIXTURE_PATH)
    
    # Trường hợp 1: Tại giây thứ 5 của video EDITED
    # (Nằm trong clip đầu tiên, offset 5s)
    # -> Phải tương ứng với 50s (raw_start) + 5s = 55s của video RAW
    assert convert_edited_to_raw_time(5.0, time_map) == 55.0

    # Trường hợp 2: Tại giây thứ 12 của video EDITED
    # (Nằm trong clip thứ hai, offset 2s so với đầu clip)
    # -> Phải tương ứng với 120s (raw_start) + 2s = 122s của video RAW
    assert convert_edited_to_raw_time(12.0, time_map) == 122.0
    
    # Trường hợp 3: Một thời điểm không thuộc clip nào (khoảng trống)
    assert convert_edited_to_raw_time(28.0, time_map) is None