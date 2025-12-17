# scripts/explore_fcpxml_tags.py

import os
import argparse
import xml.etree.ElementTree as ET
import logging
from collections import Counter

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s', force=True)

def find_all_fcpxml_files(root_dir: str) -> list:
    """
    Duyệt đệ quy một thư mục để tìm tất cả các file .fcpxml.
    """
    fcpxml_files = []
    logging.info(f"Đang quét thư mục '{root_dir}' để tìm các file .fcpxml...")
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith('.fcpxml'):
                fcpxml_files.append(os.path.join(dirpath, filename))
    logging.info(f"Đã tìm thấy {len(fcpxml_files)} file.")
    return fcpxml_files

def extract_tags_from_file(file_path: str) -> set:
    """
    Phân tích một file XML và trả về một tập hợp (set) chứa tất cả các tên thẻ duy nhất.
    Sử dụng iterparse để không tải toàn bộ file lớn vào bộ nhớ cùng lúc.
    """
    tags = set()
    try:
        # iterparse là cách hiệu quả nhất để xử lý các file XML lớn
        # Nó duyệt qua file và tạo ra các sự kiện (start, end) cho mỗi thẻ
        for event, elem in ET.iterparse(file_path, events=('start',)):
            tags.add(elem.tag)
        logging.info(f"Đã trích xuất {len(tags)} thẻ duy nhất từ file: {os.path.basename(file_path)}")
    except ET.ParseError as e:
        logging.error(f"Lỗi phân tích cú pháp file XML '{file_path}': {e}")
    except Exception as e:
        logging.error(f"Lỗi không xác định khi xử lý file '{file_path}': {e}")
    return tags

def main(source_dir: str, output_file: str):
    """
    Hàm chính điều phối việc quét, trích xuất và tạo báo cáo.
    """
    fcpxml_files = find_all_fcpxml_files(source_dir)
    if not fcpxml_files:
        logging.warning("Không tìm thấy file FCPXML nào để phân tích.")
        return

    all_tags = set()
    tag_counter = Counter()

    for file_path in fcpxml_files:
        tags_in_file = extract_tags_from_file(file_path)
        all_tags.update(tags_in_file) # Gộp các thẻ mới vào tập hợp tổng
        tag_counter.update(list(tags_in_file)) # Đếm số file chứa thẻ này

    sorted_tags = sorted(list(all_tags))

    logging.info(f"\nTổng hợp hoàn tất. Tìm thấy tổng cộng {len(sorted_tags)} thẻ duy nhất.")

    # Tạo báo cáo Markdown
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# FCPXML Tag Inventory Report\n")
        f.write("## Báo cáo Thống kê các Thẻ FCPXML\n\n")
        f.write(f"This report lists all unique XML tags found across **{len(fcpxml_files)}** `.fcpxml` files in the directory: `{source_dir}`.\n")
        f.write(f"*Báo cáo này liệt kê tất cả các thẻ XML duy nhất được tìm thấy trong **{len(fcpxml_files)}** file `.fcpxml` tại thư mục: `{source_dir}`.*\n\n")
        f.write("--- \n\n")
        f.write("| Tag Name / Tên Thẻ | Found in Files / Tìm thấy trong (số file) |\n")
        f.write("| :--- | :--- |\n")
        
        for tag in sorted_tags:
            f.write(f"| `{tag}` | {tag_counter[tag]} |\n")

    logging.info(f"Đã lưu báo cáo vào file: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quét các file FCPXML và thống kê tất cả các thẻ XML duy nhất.")
    parser.add_argument("source_directory", type=str, help="Thư mục gốc chứa các file FCPXML cần quét (sẽ quét cả thư mục con).")
    parser.add_argument("-o", "--output", type=str, default="FCPXML_TAG_INVENTORY.md", help="Tên file báo cáo đầu ra (mặc định: FCPXML_TAG_INVENTORY.md).")
    
    args = parser.parse_args()
    
    main(os.path.abspath(args.source_directory), args.output)