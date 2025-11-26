# **IA MEDIA Project - Intelligent Automation for Media Processing**
## **Dự án IA MEDIA - Tự động hóa Thông minh cho Xử lý Truyền thông**
[![Status](https://img.shields.io/badge/Status-Phase%201%20Demo%20Ready-green)]()
[![Python](https://img.shields.io/badge/Python-3.10-blue)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey)]()
---

## **1. Overview / Tổng quan**

**IA MEDIA** is a strategic initiative to leverage **I**ntelligent **A**utomation to address challenges in the post-production workflow for the video dharma talks of Zen Master Thich Nhat Hanh. The core objective is to build an intelligent system capable of automating repetitive tasks, enhancing the editorial team's efficiency, standardizing product quality, and significantly shortening the project completion timeline.

-   **The Problem:** The manual editing process, especially the task of searching for micro-audio errors (pronunciation, phonemes, final sounds), consumes the majority of working hours (estimated >50%). This reduces productivity and extends the project timeline.
-   **The Solution:** To build an IA-powered pipeline that acts as an "intelligent editorial assistant," helping to identify, suggest, and ultimately, automatically correct audio errors.

***

**IA MEDIA** là một sáng kiến chiến lược nhằm ứng dụng **T**ự động hóa **T**hông minh (**I**ntelligent **A**utomation) để giải quyết các thách thức trong quy trình hậu kỳ video pháp thoại của Thiền sư Thích Nhat Hạnh. Mục tiêu cốt lõi là xây dựng một hệ thống thông minh có khả năng tự động hóa các tác vụ lặp đi lặp lại, nâng cao hiệu suất làm việc của đội ngũ biên tập, chuẩn hóa chất lượng sản phẩm và rút ngắn đáng kể thời gian hoàn thành dự án.

-   **Vấn đề:** Quy trình chỉnh sửa thủ công, đặc biệt là việc dò tìm các lỗi âm thanh vi mô (phát âm, âm vị, âm đuôi), tiêu tốn phần lớn thời gian làm việc (ước tính >50%), làm giảm năng suất và kéo dài tiến độ dự án.
-   **Giải pháp:** Xây dựng một pipeline được vận hành bởi IA, hoạt động như một "trợ lý biên tập thông minh", giúp xác định, gợi ý và tiến tới tự động khắc phục các lỗi âm thanh.

---

## **2. Development Roadmap / Lộ trình Phát triển**

The project will be implemented in 3 main phases, with each phase delivering a significant upgrade and immediate value.

### **Phase 1: Automated Error Detection System**
-   **Objective:** Build a system capable of "listening" to and analyzing entire videos, then automatically generating a list of potential errors with precise timestamps.
-   **Key Features:** Detect pronunciation/phonetic errors, technical issues (noise, clicks, clipping, volume), and pacing errors (long silences, filler words).
-   **Deliverable:** An FCPXML file with "To-Do Markers," allowing editors to import it directly into Final Cut Pro and jump to each error without manual searching.
-   **Impact:** Eliminates the manual search process, **boosting efficiency by an estimated 30-40%**.

### **Phase 2: Interactive Correction Suggestion System**
-   **Objective:** Upgrade the system from an "error spotter" to an "expert advisor" that can propose effective correction methods.
-   **Key Features:** Integrate a Large Language Model (LLM) with RAG techniques, build a knowledge base from past edits and editor expertise, and implement a feedback loop for continuous learning.
-   **Impact:** Reduces decision-making time, standardizes quality. **Total efficiency boost estimated at 50-60%**.

### **Phase 3: Automated Correction**
-   **Objective:** Achieve the highest level of automation, where the system can perform basic and complex correction tasks on its own.
-   **Key Features:** Rule-based automation (removing filler words) and AI-powered automation (replacing faulty audio with clean samples, applying dynamic EQ).
-   **Impact:** Shifts the editor's role from a "doer" to a "quality supervisor." **Total efficiency boost estimated at 70-80%**.

***

Dự án sẽ được triển khai theo 3 giai đoạn chính, với mỗi giai đoạn là một bản nâng cấp mang lại giá trị gia tăng rõ rệt.

### **Giai đoạn 1: Hệ thống Tự động Phát hiện Lỗi**
-   **Mục tiêu:** Xây dựng một hệ thống có khả năng "nghe" và phân tích toàn bộ video, sau đó tự động tạo ra một danh sách các lỗi tiềm ẩn kèm theo timestamp chính xác.
-   **Chức năng chính:** Phát hiện lỗi phát âm/âm vị, lỗi kỹ thuật (tiếng ồn, click, vỡ tiếng, âm lượng), và lỗi nhịp điệu (khoảng lặng dài, từ đệm).
-   **Kết quả đầu ra:** Một file định dạng FCPXML chứa các "To-Do Markers", cho phép biên tập viên nhập trực tiếp vào Final Cut Pro và nhảy đến chính xác từng vị trí lỗi.
-   **Tác động:** Loại bỏ hoàn toàn công đoạn dò tìm thủ công, **tăng hiệu suất ước tính 30-40%**.

### **Giai đoạn 2: Hệ thống Gợi ý Khắc phục Tương tác**
-   **Mục tiêu:** Nâng cấp hệ thống từ một "người chỉ điểm" thành một "cố vấn chuyên môn", có khả năng đề xuất các phương án sửa lỗi hiệu quả.
-   **Chức năng chính:** Tích hợp Mô hình Ngôn ngữ lớn (LLM) với kỹ thuật RAG, xây dựng "kho tri thức" từ dữ liệu cũ và kinh nghiệm của biên tập viên, xây dựng cơ chế thu thập phản hồi để hệ thống tự học.
-   **Tác động:** Giảm thời gian ra quyết định, chuẩn hóa chất lượng. **Tăng hiệu suất tổng cộng ước tính 50-60%**.

### **Giai đoạn 3: Tự động Khắc phục Lỗi**
-   **Mục tiêu:** Đưa hệ thống đến mức độ tự động hóa cao nhất, có khả năng tự thực hiện các thao tác sửa lỗi cơ bản và phức tạp.
-   **Chức năng chính:** Tự động hóa dựa trên luật (xóa từ đệm) và dựa trên AI (tự động thay thế âm thanh, áp dụng EQ).
-   **Tác động:** Chuyển vai trò của biên tập viên thành người giám sát chất lượng. **Tăng hiệu suất tổng cộng ước tính 70-80%**.

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

## 4. Project Structure / Cấu trúc Dự án

See [PROJECT_STRUCTURE.md](./documents/PROJECT_STRUCTURE.md) for a detailed file tree.
*Xem [PROJECT_STRUCTURE.md](./documents/PROJECT_STRUCTURE.md) để biết chi tiết cây thư mục.*

-   `src/`: Source code (`analysis`, `database`, `utils`, `ai`).
-   `notebooks/`: Jupyter Notebooks for Google Colab execution.
-   `server_configs/`: Postgres configuration files.
-   `tests/`: Unit tests.

---

### Next Immediate Step / Bước Tiếp theo:

The project is now in a **"Waiting for Data"** state. The next phase will focus on **implementing the core analysis pipeline** (`main.py`) to process the first batch of sample videos.
*Dự án hiện đang ở trạng thái **"Chờ Dữ liệu"**. Giai đoạn tiếp theo sẽ tập trung vào việc **hiện thực hóa pipeline phân tích lõi** (`main.py`) để xử lý lô video mẫu đầu tiên.*


### **Demo Objectives / Mục tiêu Demo:**
1.  **Prove Core Logic:** Successfully build a script that can analyze a pair of videos (raw and edited) and extract micro-audio chunks (word-level) for analysis.
2.  **Build Phonetic Dictionary:** Vectorize the extracted audio chunks and store them in a VectorDB (PostgreSQL + pgvector) to create a "signature" for "correct" and "incorrect" pronunciations.
3.  **Complete End-to-End Pipeline:** Integrate the logic into a Dockerized API service, deploy it to a cloud environment (RunPod), and orchestrate the workflow with n8n.
4.  **Generate Valuable Output:** Demonstrate that the system can produce a usable FCPXML file with To-Do Markers that editors can immediately use.

### **Technology Stack / Công nghệ Sử dụng:**
-   **Language / Ngôn ngữ:** Python 3.10
-   **AI/ML:** OpenAI Whisper, Sentence Transformers (Hugging Face), Pytorch
-   **Audio Processing / Xử lý Âm thanh:** FFmpeg, Librosa, Pydub
-   **Infrastructure / Hạ tầng:** GitHub Codespaces (Development), Docker, RunPod (GPU Deployment), PostgreSQL + pgvector
-   **Orchestration / Điều phối:** n8n
