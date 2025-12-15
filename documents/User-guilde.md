# Hướng dẫn Sử dụng Module Phát hiện Lỗi (Detector)

Module Detector cho phép bạn quét một video thô (raw) và tự động tạo ra file FCPXML chứa các marker đánh dấu lỗi để import vào Final Cut Pro.

## 1. Chuẩn bị
*   Đảm bảo Database đã có dữ liệu "học" (đã chạy `vectorize.py` trước đó).
*   File video raw (định dạng `.mp4`, `.mov`).

## 2. Cách chạy (Local / Codespaces)

Bạn có thể chạy trực tiếp file script hoặc gọi qua hàm.

### Cách A: Viết script chạy nhanh (khuyên dùng)
Tạo file `run_detect.py`:

```python
from src.analysis.detector import detect_errors_in_video
import os

# Cấu hình
VIDEO_PATH = "./data/Batch_02/2025-05-20-phapthoai_raw.mp4"
OUTPUT_XML = "./workspace/detected_errors.fcpxml"
WORKSPACE = "./workspace"

# Chạy
detect_errors_in_video(VIDEO_PATH, OUTPUT_XML, WORKSPACE)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121