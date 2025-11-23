# scripts/generate_repo_map.py

import os

# --- CẤU HÌNH ---
# Thay đổi nếu cần
REPO_URL = "https://github.com/shan369rpa/IA-MEDIA"
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUTPUT_FILE = "REPO_MAP.md"

# Các thư mục và file cần bỏ qua
EXCLUDE_DIRS = {'.git', '.github', '.devcontainer', '__pycache__', 'workspace', 'data', '.venv'}
EXCLUDE_FILES = {'REPO_MAP.md'}
# Chỉ lấy các file có đuôi này
INCLUDE_EXTENSIONS = {
    '.py', '.md', '.sql', '.toml', '.ini', '.json', 'Dockerfile', 
    '.env.example', '.gitignore',
}

def generate_repo_map():
    """
    Quét qua cây thư mục của repo, tạo cây cấu trúc và các URL raw,
    sau đó ghi ra file OUTPUT_FILE.
    """
    repo_map_content = "# IA MEDIA - Repository Map & Raw URLs\n\n"
    repo_map_content += "This file is auto-generated. It provides a map of the project structure with direct links to the raw content of each file on GitHub.\n\n"
    
    # Xác định nhánh hiện tại
    try:
        current_branch = os.popen('git rev-parse --abbrev-ref HEAD').read().strip()
    except Exception:
        current_branch = "main" # Mặc định nếu không tìm thấy
        
    repo_map_content += f"**Current Branch:** `{current_branch}`\n\n"

    tree_structure = "## Project Structure\n\n```\n"
    url_list = "## Raw File URLs\n\n"

    for root, dirs, files in os.walk(ROOT_DIR, topdown=True):
        # Bỏ qua các thư mục không cần thiết
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        # Tính toán độ sâu và tiền tố cho cây thư mục
        level = root.replace(ROOT_DIR, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree_structure += f"{indent}{os.path.basename(root)}/\n"
        sub_indent = ' ' * 4 * (level + 1)
        
        for file in sorted(files):
            if file in EXCLUDE_FILES:
                continue

            # Kiểm tra xem file có đuôi được cho phép không
            should_include = any(file.endswith(ext) for ext in INCLUDE_EXTENSIONS)
            if not should_include and os.path.splitext(file) == '':
                 # Xử lý các file không có đuôi như Dockerfile
                 if file in INCLUDE_EXTENSIONS:
                     should_include = True
            
            if should_include:
                tree_structure += f"{sub_indent}├── {file}\n"
                
                # Tạo URL raw
                relative_path = os.path.relpath(os.path.join(root, file), ROOT_DIR)
                raw_url = f"{REPO_URL.replace('github.com', 'raw.githubusercontent.com')}/{current_branch}/{relative_path}"
                url_list += f"- **{relative_path}**:\n  `{raw_url}`\n"

    tree_structure += "```\n"
    repo_map_content += tree_structure + "\n" + url_list

    # Ghi kết quả ra file
    output_path = os.path.join(ROOT_DIR, OUTPUT_FILE)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(repo_map_content)
        
    print(f"✅ Repository map has been generated: {output_path}")
    print("\nYou can now copy the content of this file to provide context to the AI.")

if __name__ == "__main__":
    generate_repo_map()