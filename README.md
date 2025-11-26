# **IA MEDIA Project - Intelligent Automation for Media Processing**
## **Dự án IA MEDIA - Tự động hóa Thông minh cho Xử lý Truyền thông**
[![Status](https://img.shields.io/badge/Status-Phase%201%20Demo%20Ready-green)]()
[![Python](https://img.shields.io/badge/Python-3.10-blue)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey)]()
---

---

## 1. Overview / Tổng quan

**IA MEDIA** is a strategic, open-source initiative to leverage **I**ntelligent **A**utomation to address challenges in the post-production workflow for video dharma talks.

Our goal is to build a system that acts as an "Intelligent Editorial Assistant," capable of:
1.  **Automated Error Detection:** Finding pronunciation errors, noise, and bad cuts without manual listening.
2.  **Data Enrichment:** Creating a rich, multi-modal dataset (Audio-Text-Video) for AI research.
3.  **Future Expansion:** Serving as a foundation for Voice Cloning and TTS applications.

***IA MEDIA** là một sáng kiến chiến lược, mã nguồn mở nhằm ứng dụng **T**ự động hóa **T**hông minh (**I**ntelligent **A**utomation) để giải quyết các thách thức trong quy trình hậu kỳ video pháp thoại.*

-   **Vấn đề:** Quy trình chỉnh sửa thủ công, đặc biệt là việc dò tìm các lỗi âm thanh vi mô (phát âm, âm vị, âm đuôi), tiêu tốn phần lớn thời gian làm việc (ước tính >50%), làm giảm năng suất và kéo dài tiến độ dự án.
-   **Giải pháp:** Xây dựng một pipeline được vận hành bởi IA, hoạt động như một "trợ lý biên tập thông minh", giúp xác định, gợi ý và tiến tới tự động khắc phục các lỗi âm thanh. 
*   **[THEORETICAL_FRAMEWORK.md](./documents/THEORETICAL_FRAMEWORK.md):** Theoretical basic and Multi-layered Chunking(**Tài liệu cần đọc**).

---

## **2. Development Roadmap / Lộ trình Phát triển**
The project will be implemented in 3 main phases, with each phase delivering a significant upgrade and immediate value.

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

## 3. Current Status: Phase 1 Demo Ready / Trạng thái Hiện tại: Sẵn sàng Demo Giai đoạn 1

**We have successfully implemented the Core Analysis Pipeline.**
**Chúng ta đã thực hiện thành công Pipeline Phân tích Lõi.**

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

## 4. Documentation / Tài liệu
*   **[THEORETICAL_FRAMEWORK.md](./documents/THEORETICAL_FRAMEWORK.md):** Theoretical basic and Multi-layered Chunking.
*   **[GUIDE.md](./documents/GUIDE.md):** Operational commands (SSH Tunneling, DB management).
*   **[DATA_STRATEGY.md](./documents/DATA_STRATEGY.md):** Deep dive into data chunking and enrichment strategy.
*   **[COMPUTE_STRATEGY.md](./documents/COMPUTE_STRATEGY.md):** Analysis of compute platforms.
*   **[STORAGE_ANALYSIS.md](./documents/STORAGE_ANALYSIS.md):** Storage cost and architecture analysis.
*   **[FILE_NAMING_CONVENTION.md](./documents/FILE_NAMING_CONVENTION.md):** Rules for naming source files.
*   **[GIT_CONVENTION.md](./documents/GIT_CONVENTION.md):** Branching and commit standards.
---

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
### **Technology Stack / Công nghệ Sử dụng:**
-   **Language / Ngôn ngữ:** Python 3.10
-   **AI/ML:** OpenAI Whisper, Sentence Transformers (Hugging Face), Pytorch
-   **Audio Processing / Xử lý Âm thanh:** FFmpeg, Librosa, Pydub
-   **Infrastructure / Hạ tầng:** GitHub Codespaces (Development), Docker, RunPod (GPU Deployment), PostgreSQL + pgvector
-   **Orchestration / Điều phối:** n8n
