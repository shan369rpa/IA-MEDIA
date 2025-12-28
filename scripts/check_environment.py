# scripts/check_environment.py

import sys
import os
import subprocess
import importlib.util
import logging

# --- Cấu hình ---
# Thêm các thư viện quan trọng và phiên bản mong muốn vào đây
REQUIRED_PACKAGES = {
    "torch": "2.3.1",
    "torchaudio": "2.3.1",
    "transformers": "4.36.2",
    "whisperx": None, # Kiểm tra sự tồn tại, không cần phiên bản cụ thể
    "pyannote.audio": "3.1.1",
    "speechbrain": "1.0.0",
    "numpy": "1.26.4", # Hoặc phiên bản < 2.0.0
    "pandas": "2.2.2",
    "librosa": "0.10.1",
    "psycopg2": None,
    "pgvector": None,
}

# --- Thiết lập Logging ---
# Sử dụng một logger riêng để không xung đột với các module khác
logger = logging.getLogger("EnvironmentCheck")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

def check_python_version():
    """Kiểm tra phiên bản Python."""
    logger.info("--- 1. Kiểm tra Phiên bản Python ---")
    major, minor = sys.version_info.major, sys.version_info.minor
    if major == 3 and minor == 10:
        logger.info(f"✅ OK: Phiên bản Python là {major}.{minor}, đạt yêu cầu.")
    else:
        logger.warning(f"⚠️ Cảnh báo: Phiên bản Python là {major}.{minor}. Dự án được phát triển với 3.10.")

def check_system_tool(tool_name):
    """Kiểm tra sự tồn tại của một công cụ dòng lệnh hệ thống."""
    logger.info(f"--- 2. Kiểm tra Công cụ Hệ thống: {tool_name} ---")
    try:
        # Dùng `subprocess.run` để chạy lệnh `tool --version`
        # `capture_output=True` để ẩn output, `check=True` để báo lỗi nếu không tìm thấy
        subprocess.run([tool_name, "-version"], check=True, capture_output=True, text=True)
        logger.info(f"✅ OK: Đã tìm thấy '{tool_name}' trong PATH hệ thống.")
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        logger.error(f"❌ LỖI: Không tìm thấy '{tool_name}'. Vui lòng cài đặt và/hoặc thêm nó vào biến môi trường PATH.")
        return False

def check_python_packages():
    """Kiểm tra các thư viện Python đã được cài đặt."""
    logger.info("--- 3. Kiểm tra các Gói thư viện Python ---")
    all_ok = True
    installed_packages = {pkg.key: pkg.version for pkg in __import__("pkg_resources").working_set}
    
    for package, required_version in REQUIRED_PACKAGES.items():
        # Xử lý các gói cài từ git
        if package == 'whisperx':
            spec = importlib.util.find_spec(package)
            if spec:
                logger.info(f"✅ OK: Đã tìm thấy '{package}'.")
            else:
                logger.error(f"❌ LỖI: Gói '{package}' chưa được cài đặt.")
                all_ok = False
            continue

        if package not in installed_packages:
            logger.error(f"❌ LỖI: Gói '{package}' chưa được cài đặt.")
            all_ok = False
        elif required_version and installed_packages[package] != required_version:
            logger.warning(f"⚠️ Cảnh báo: Gói '{package}' có phiên bản {installed_packages[package]}, khác với phiên bản đề xuất {required_version}.")
        else:
            logger.info(f"✅ OK: Đã tìm thấy '{package}' (version: {installed_packages[package]}).")
            
    if all_ok:
        logger.info("=> Tất cả các gói Python chính đều đã được cài đặt.")

def check_pytorch_gpu_support():
    """Kiểm tra PyTorch và hỗ trợ CUDA."""
    logger.info("--- 4. Kiểm tra PyTorch và Hỗ trợ GPU ---")
    try:
        import torch
        logger.info(f"✅ OK: PyTorch đã được cài đặt, phiên bản: {torch.__version__}")
        
        is_cuda_available = torch.cuda.is_available()
        if is_cuda_available:
            logger.info("✅ OK: PyTorch nhận diện được GPU (CUDA is available).")
            device_count = torch.cuda.device_count()
            logger.info(f"   - Tìm thấy {device_count} thiết bị GPU.")
            for i in range(device_count):
                logger.info(f"   - GPU {i}: {torch.cuda.get_device_name(i)}")
        else:
            logger.warning("⚠️ Cảnh báo: PyTorch đang chạy ở chế độ CPU-only (CUDA is not available).")
            logger.warning("   - Các tác vụ AI sẽ chạy rất chậm. Đây là điều bình thường nếu máy bạn không có GPU NVIDIA.")
            
    except ImportError:
        logger.error("❌ LỖI: Không tìm thấy PyTorch. Đây là một thư viện bắt buộc.")
    except Exception as e:
        logger.error(f"❌ LỖI khi kiểm tra PyTorch: {e}")

def main():
    """Chạy tất cả các bước kiểm tra."""
    print("\n" + "="*50)
    print("      BẮT ĐẦU KIỂM TRA MÔI TRƯỜNG DỰ ÁN IA MEDIA")
    print("="*50 + "\n")
    
    check_python_version()
    print("-" * 50)
    
    check_system_tool("ffmpeg")
    print("-" * 50)
    
    check_python_packages()
    print("-" * 50)
    
    check_pytorch_gpu_support()
    
    print("\n" + "="*50)
    print("      KIỂM TRA MÔI TRƯỜNG HOÀN TẤT")
    print("="*50 + "\n")


if __name__ == "__main__":
    # Cần cài đặt pkg_resources nếu chưa có
    try:
        import pkg_resources
    except ImportError:
        print("Đang cài đặt 'pkg_resources'...")
        subprocess.run([sys.executable, "-m", "pip", "install", "setuptools"])
    
    main()
