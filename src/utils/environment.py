# src/utils/environment.py
import os
import sys
import logging

def setup_environment():
    """
    Cấu hình các biến môi trường cần thiết cho ứng dụng,
    đặc biệt là PATH cho các thư viện CUDA/cuDNN trên Windows.
    Hàm này phải được gọi đầu tiên trong script chính.
    """
    if sys.platform == "win32":
        logging.info("Phát hiện môi trường Windows. Đang cấu hình CUDA PATH...")
        site_packages_path = next((p for p in sys.path if 'site-packages' in p), None)
        
        if not site_packages_path:
            logging.warning("Không tìm thấy thư mục site-packages. Bỏ qua cấu hình CUDA PATH.")
            return

        cuda_bin_dirs = [
            os.path.join(site_packages_path, "nvidia", "cuda_runtime", "bin"),
            os.path.join(site_packages_path, "nvidia", "cudnn", "bin"),
            os.path.join(site_packages_path, "nvidia", "cublas", "bin"),
        ]

        current_path = os.environ.get("PATH", "")
        paths_to_add = [d for d in cuda_bin_dirs if os.path.isdir(d) and d not in current_path]
            
        if paths_to_add:
            logging.info(f"Đang thêm các đường dẫn CUDA/cuDNN vào PATH: {paths_to_add}")
            os.environ["PATH"] = ";".join(paths_to_add) + ";" + current_path
        else:
            logging.info("Các đường dẫn CUDA/cuDNN cần thiết dường như đã có trong PATH.")