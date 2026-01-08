import os
from pathlib import Path

def print_tree(startpath):
    startpath = Path(startpath)
    
    # Duyệt qua các thư mục và tệp tin
    for root, dirs, files in os.walk(startpath):
        # Chuyển root (PosixPath) thành chuỗi (str)
        root = str(root)
        
        # Tính chiều sâu của thư mục
        level = root.replace(str(startpath), '').count(os.sep)
        
        # In khoảng cách thụt đầu dòng tùy thuộc vào mức độ của thư mục
        indent = ' ' * 4 * level
        print(f"{indent}[DIR] {os.path.basename(root)}")
        
        # In tên các tệp trong thư mục
        for file in files:
            print(f"{indent}    {file}")

# Ví dụ sử dụng hàm

path = Path("/Applications/BorisFX/CrumplePop/SoundApp/bfx-license-tool")

start_directory = "/path/Applications/BorisFX"  # Thay đổi đường dẫn này
print_tree(path)