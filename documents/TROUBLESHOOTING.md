# Troubleshooting Guide - IA MEDIA Project
## Hướng dẫn Gỡ lỗi - Dự án IA MEDIA

This document logs common issues, errors, and their resolutions encountered during the setup and development of the IA MEDIA project, particularly on a Windows + NVIDIA GPU environment.

*Tài liệu này ghi lại các vấn đề, lỗi thường gặp và giải pháp của chúng trong quá trình cài đặt và phát triển dự án IA MEDIA, đặc biệt trên môi trường Windows có GPU NVIDIA.*

---

## 1. Issue: Dependency Hell with `WhisperX` on Windows
### Vấn đề: "Địa ngục Phụ thuộc" với `WhisperX` trên Windows

**Date Encountered / Ngày Gặp phải:** 2025-12-13

### Symptoms / Triệu chứng

Running the main pipeline (`main.py`) resulted in a series of `ModuleNotFoundError` and `ImportError` crashes, even after multiple attempts to reinstall libraries. Key errors included:
*   `ModuleNotFoundError: No module named 'pyannote'`
*   `ModuleNotFoundError: No module named 'opentelemetry'`
*   `ImportError: TorchCodec is required...`
*   `AttributeError: 'np.NaN' was removed...` (NumPy 2.x incompatibility)
*   `TypeError: unexpected keyword argument 'initial_prompt'`
*   `ValueError: ... The chosen align_model could not be found...`
*   `Could not locate cudnn_ops64_9.dll`

### Root Cause Analysis / Phân tích Nguyên nhân Gốc rễ

The core issue is a complex web of version conflicts between several core AI libraries (`WhisperX`, `PyTorch`, `transformers`, `pyannote.audio`, `numpy`) when installed via `pip` on a Windows system. `pip`'s dependency resolver struggles to find a stable combination that satisfies every package's requirements, especially when dealing with GPU-specific builds of PyTorch. The `cudnn_ops64_9.dll` error specifically points to Python not being able to find the necessary NVIDIA library files in the system's PATH, even if they were installed by `pip`.

*Nguyên nhân cốt lõi là một mạng lưới phức tạp các xung đột phiên bản giữa các thư viện AI chính. Bộ giải quyết phụ thuộc của `pip` gặp khó khăn trong việc tìm ra một tổ hợp ổn định, đặc biệt với các bản build PyTorch dành riêng cho GPU. Lỗi `.dll` chỉ ra rằng Python không tìm thấy thư viện NVIDIA trong biến môi trường PATH của hệ thống.*

### Resolution / Giải pháp

Instead of a single `requirements.txt` file, a **"Surgical Installation"** process was required, installing libraries in specific layers to enforce version compatibility. The final, stable working environment was achieved with the following key steps:
*Thay vì một file `requirements.txt` duy nhất, một quy trình **"Cài đặt Phẫu thuật"** đã được yêu cầu, cài đặt các thư viện theo từng lớp để ép buộc sự tương thích về phiên bản.*

1.  **Clean Virtual Environment:** Started with a fresh Python virtual environment (`venv`).
2.  **PyTorch First:** Installed a specific, stable GPU version of PyTorch first to establish the foundation.
    - `pip install torch==2.3.1+cu121 torchvision==0.18.1+cu121 torchaudio==2.3.1+cu121 --index-url https://download.pytorch.org/whl/cu121`
3.  **Dependency Pinning:** Manually installed specific older versions of `numpy` and `pandas` before installing other packages that depend on them.
    - `pip install "numpy<2.0"`
4.  **Targeted Dependency Installation:** Installed key dependencies of `WhisperX` (like `pyannote.audio==3.1.1` and `transformers==4.36.2`) manually to ensure compatible versions were used.
5.  **`--no-deps` Installation:** Installed `WhisperX` itself with the `--no-deps` flag to prevent it from overwriting our carefully selected dependencies.
6.  **PATH Configuration for CUDA DLLs:** Added a code block at the beginning of `src/analysis/transcriber.py` to programmatically find the paths to the `cudnn` and `cublas` `.dll` files (installed via `pip`) and prepend them to the system's `PATH` environment variable at runtime. This was the final step that resolved the `cudnn_ops64_9.dll` error.

**Key takeaway:** Setting up complex AI pipelines on Windows often requires manual intervention and precise version pinning, and dynamically updating the PATH variable in code can be necessary to resolve DLL loading issues.
***Bài học chính:** Việc thiết lập các pipeline AI phức tạp trên Windows thường đòi hỏi sự can thiệp thủ công, ghim phiên bản chính xác, và việc cập nhật động biến PATH trong code có thể là cần thiết để giải quyết các vấn đề tải file DLL.*

---