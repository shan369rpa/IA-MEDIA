# src/utils/fcpxml_parser.py

import xml.etree.ElementTree as ET
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fcpxml_time_to_seconds(time_str: str) -> float:
    """
    Chuyển đổi định dạng thời gian của FCPXML (ví dụ: "36036/600s" hoặc "10s") thành giây.
    """
    if not time_str:
        return 0.0
    
    time_str = time_str.replace('s', '')
    if '/' in time_str:
        try:
            num, den = map(int, time_str.split('/'))
            return num / den
        except (ValueError, ZeroDivisionError):
            return 0.0
    else:
        try:
            return float(time_str)
        except ValueError:
            return 0.0

def parse_fcpxml_to_time_map(fcpxml_path: str) -> list:
    """
    Đọc file FCPXML và tạo ra một bản đồ chuyển đổi thời gian.
    Trả về một danh sách các tuple: (edited_start_sec, edited_end_sec, raw_start_sec).
    """
    time_map = []
    logging.info(f"Đang phân tích file FCPXML: {fcpxml_path}")
    try:
        tree = ET.parse(fcpxml_path)
        root = tree.getroot()

        # Tìm tất cả các thẻ asset-clip trong timeline chính (spine)
        for clip in root.findall(".//spine/asset-clip"):
            offset_str = clip.get('offset', '0s') # Mặc định là 0s nếu không có
            duration_str = clip.get('duration')
            start_str = clip.get('start')

            # Chỉ xử lý các clip có đủ thông tin cần thiết
            if not all([duration_str, start_str]):
                logging.warning(f"Bỏ qua clip không đủ thông tin: {clip.get('name')}")
                continue

            edited_start = fcpxml_time_to_seconds(offset_str)
            duration = fcpxml_time_to_seconds(duration_str)
            raw_start = fcpxml_time_to_seconds(start_str)
            
            edited_end = edited_start + duration
            
            time_map.append((edited_start, edited_end, raw_start))
            
        # Sắp xếp bản đồ theo thời gian bắt đầu của video đã chỉnh sửa để tìm kiếm hiệu quả
        time_map.sort()
        logging.info(f"Phân tích thành công, đã tạo time map với {len(time_map)} clip.")
        return time_map
    
    except ET.ParseError as e:
        logging.error(f"Lỗi phân tích XML: {e}")
        return []
    except FileNotFoundError:
        logging.error(f"Không tìm thấy file FCPXML tại: {fcpxml_path}")
        return []

def convert_edited_to_raw_time(edited_time_sec: float, time_map: list) -> float | None:
    """
    Tìm thời gian tương ứng trên file RAW từ một thời điểm trên file EDITED.
    Sử dụng tìm kiếm nhị phân (binary search) sẽ hiệu quả hơn cho list lớn, 
    nhưng tìm kiếm tuần tự đủ tốt cho số lượng clip < vài nghìn.
    """
    for edited_start, edited_end, raw_start in time_map:
        if edited_start <= edited_time_sec < edited_end:
            offset_in_clip = edited_time_sec - edited_start
            return raw_start + offset_in_clip
    # Trả về None nếu không tìm thấy (ví dụ: đoạn đó là khoảng trống/transition trên timeline)
    return None