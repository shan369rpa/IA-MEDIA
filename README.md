# IA MEDIA Project - Intelligent Automation for Media Processing
## Dự án IA MEDIA - Tự động hóa Thông minh cho Xử lý Truyền thông

[![Status](https://img.shields.io/badge/Status-Phase%201%20Demo%20Ready-green)]()
[![Python](https://img.shields.io/badge/Python-3.10-blue)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey)]()

---

## 1. Overview / Tổng quan

**IA MEDIA** is a strategic, open-source initiative to leverage **I**ntelligent **A**utomation to address challenges in the post-production workflow for video dharma talks.

Our goal is to build a system that acts as an "Intelligent Editorial Assistant," capable of:
1.  **Automated Error Detection:** Finding pronunciation errors, noise, and bad cuts without manual listening.
2.  **Data Enrichment:** Creating a rich, multi-modal dataset (Audio-Text-Video) for AI research.
3.  **Future Expansion:** Serving as a foundation for Voice Cloning and TTS applications.

***IA MEDIA** là một sáng kiến chiến lược, mã nguồn mở nhằm ứng dụng **T**ự động hóa **T**hông minh (**I**ntelligent **A**utomation) để giải quyết các thách thức trong quy trình hậu kỳ video pháp thoại.*

*Mục tiêu của chúng tôi là xây dựng một hệ thống hoạt động như "Trợ lý Biên tập Thông minh", có khả năng:*
1.  ***Tự động Phát hiện Lỗi:** Tìm lỗi phát âm, tiếng ồn, và các vết cắt lỗi mà không cần nghe thủ công.*
2.  ***Làm giàu Dữ liệu:** Tạo ra bộ dữ liệu đa phương thức (Âm thanh-Văn bản-Video) phong phú cho nghiên cứu AI.*
3.  ***Mở rộng Tương lai:** Làm nền tảng cho các ứng dụng Voice Cloning và TTS.*

---

## 2. System Architecture / Kiến trúc Hệ thống

We employ a **Hybrid Cloud Architecture** to maximize performance while minimizing costs:
*Chúng tôi áp dụng **Kiến trúc Đám mây Lai** để tối đa hóa hiệu suất trong khi giảm thiểu chi phí:*

*   **Compute Layer (Google Colab):** Utilizing free T4 GPUs for heavy lifting (Whisper transcription, Embedding generation).
*   **Storage Layer (Google Drive):** Staging area for raw videos and processed chunk archives.
*   **Database Layer (Self-hosted PostgreSQL):** Storing persistent vector embeddings and metadata with `pgvector`, accessed securely via **SSH Tunneling**.
*   **Development Layer (GitHub Codespaces):** Central environment for coding, testing, and CI/CD.

---

## 3. Current Status: Phase 1 Demo Ready / Trạng thái Hiện tại: Sẵn sàng Demo Giai đoạn 1

**We have successfully implemented the Core Analysis Pipeline.**
**Chúng tôi đã thực hiện thành công Pipeline Phân tích Lõi.**

### ✅ Accomplishments / Thành tựu:
-   **Infrastructure:** Database `ia-media-db-pgvector` is live and secure.
-   **Core Logic:** `main.py` (Analysis) and `vectorize.py` (Ingestion) utilize modular architecture.
-   **Parsing:** Advanced FCPXML parsing logic to map edited video timestamps back to raw source footage.
-   **AI Integration:** Integrated `OpenAI Whisper` for transcription and `SpeechBrain` for phonetic embedding.
-   **Execution:** A comprehensive Google Colab Notebook is ready for batch processing.

### 🚧 Next Steps / Bước Tiếp theo:
-   Run the end-to-end pipeline on the first batch of real data (3-5 videos).
-   Verify the quality of generated chunks and vector search results.

---

## 4. Project Structure / Cấu trúc Dự án

See [PROJECT_STRUCTURE.md](./documents/PROJECT_STRUCTURE.md) for a detailed file tree.
*Xem [PROJECT_STRUCTURE.md](./documents/PROJECT_STRUCTURE.md) để biết chi tiết cây thư mục.*

-   `src/`: Source code (`analysis`, `database`, `utils`, `ai`).
-   `notebooks/`: Jupyter Notebooks for Google Colab execution.
-   `server_configs/`: Postgres configuration files.
-   `tests/`: Unit tests.

---

## 5. Getting Started / Bắt đầu

### For Developers (Local Setup)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/shan369rpa/IA-MEDIA.git
    ```
2.  **Setup Environment:**
    -   Open in **GitHub Codespaces** (Recommended - Pre-configured Docker container).
    -   Or install dependencies: `pip install -r requirements.txt`.
    -   Install local package: `pip install -e .`
3.  **Configure Secrets:**
    -   Copy `.env.example` to `.env`.
    -   Fill in your Database credentials and paths.
4.  **Testing:**
    ```bash
    pytest
    ```

### For Processing (Running a Batch)

We use **Google Colab** as the production engine.
*Chúng tôi sử dụng **Google Colab** làm công cụ sản xuất.*

1.  Upload source videos and FCPXML to **Google Drive** (`/IA_MEDIA_PROJECT/source_data/`).
2.  Open `notebooks/demo_pipeline.ipynb` in Google Colab.
3.  Upload your SSH Key (`id_rsa_colab`) and `.env` file to Drive (`/IA_MEDIA_PROJECT/secrets/`).
4.  Run the Notebook cells to execute the pipeline.

---

## 6. Documentation / Tài liệu

*   **[GUIDE.md](./documents/GUIDE.md):** Operational commands (SSH Tunneling, DB management).
*   **[DATA_STRATEGY.md](./documents/DATA_STRATEGY.md):** Deep dive into data chunking and enrichment strategy.
*   **[COMPUTE_STRATEGY.md](./documents/COMPUTE_STRATEGY.md):** Analysis of compute platforms.
*   **[STORAGE_ANALYSIS.md](./documents/STORAGE_ANALYSIS.md):** Storage cost and architecture analysis.
*   **[FILE_NAMING_CONVENTION.md](./documents/FILE_NAMING_CONVENTION.md):** Rules for naming source files.
*   **[GIT_CONVENTION.md](./documents/GIT_CONVENTION.md):** Branching and commit standards.

---

## 7. Contact & Contribution

This is an open-source project. Contributions are welcome! Please read [GIT_CONVENTION.md](./documents/GIT_CONVENTION.md) before submitting a Pull Request.

*Đây là một dự án mã nguồn mở. Hoan nghênh mọi sự đóng góp! Vui lòng đọc [GIT_CONVENTION.md](./documents/GIT_CONVENTION.md) trước khi gửi Pull Request.*