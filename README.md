# **IA MEDIA Project - Intelligent Automation for Media Processing**
## **Dự án IA MEDIA - Tự động hóa Thông minh cho Xử lý Truyền thông**
[![Status](https://img.shields.io/badge/Status-Phase%201%20Demo%20Completed-green)]()
[![Python](https://img.shields.io/badge/Python-3.10-blue)]()
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey)]()
---

## **1. Overview / Tổng quan**

**IA MEDIA** is a strategic initiative to leverage **I**ntelligent **A**utomation to address challenges in the post-production workflow for the video dharma talks of Zen Master Thich Nhat Hanh. The core objective is to build an intelligent system capable of automating repetitive tasks, enhancing the editorial team's efficiency, standardizing product quality, and significantly shortening the project completion timeline.

-   **The Problem:** The manual editing process, especially the task of searching for micro-audio errors (pronunciation, phonemes, final sounds), consumes the majority of working hours (estimated >50%). This reduces productivity and extends the project timeline.
-   **The Solution:** To build an IA-powered pipeline that acts as an "intelligent editorial assistant," helping to identify, suggest, and ultimately, automatically correct audio errors.
-   **Cơ sở lý thuyết (Reading materials):** **[THEORETICAL_FRAMEWORK.md](./documents/THEORETICAL_FRAMEWORK.md):** Theoretical basic and Multi-layered Chunking.
***

**IA MEDIA** là một sáng kiến chiến lược nhằm ứng dụng **T**ự động hóa **T**hông minh (**I**ntelligent **A**utomation) để giải quyết các thách thức trong quy trình hậu kỳ video pháp thoại của Thiền sư Thích Nhất Hạnh. Mục tiêu cốt lõi là xây dựng một hệ thống thông minh có khả năng tự động hóa các tác vụ lặp đi lặp lại, nâng cao hiệu suất làm việc của đội ngũ biên tập, chuẩn hóa chất lượng sản phẩm và rút ngắn đáng kể thời gian hoàn thành dự án.

-   **Vấn đề:** Quy trình chỉnh sửa thủ công, đặc biệt là việc dò tìm các lỗi âm thanh vi mô (phát âm, âm vị, âm đuôi), tiêu tốn phần lớn thời gian làm việc (ước tính >50%), làm giảm năng suất và kéo dài tiến độ dự án.
-   **Giải pháp:** Xây dựng một pipeline được vận hành bởi IA, hoạt động như một "trợ lý biên tập thông minh", giúp xác định, gợi ý và tiến tới tự động khắc phục các lỗi âm thanh. 
-   **Cơ sở lý thuyết (Tài liệu cần đọc):** **[THEORETICAL_FRAMEWORK.md](./documents/THEORETICAL_FRAMEWORK.md):** Cơ sở lý thuyết và các kỹ thuật cắt lớp.

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

## 3. Current Status: Phase 1 Foundation Complete & Pivoting to v3 Architecture / Trạng thái Hiện tại: Hoàn thành Nền tảng & Chuyển hướng sang Kiến trúc v3

**We have successfully built and validated all core components of the initial data pipeline. A successful end-to-end run on sample data has generated thousands of labeled audio chunks and a preliminary classifier model.**
***Chúng ta đã xây dựng và xác thực thành công tất cả các thành phần cốt lõi của pipeline dữ liệu ban đầu. Một lần chạy thử từ đầu đến cuối trên dữ liệu mẫu đã tạo ra hàng ngàn audio chunk được gán nhãn và một mô hình phân loại sơ bộ.***

### Key Accomplishments to Date / Thành tựu Chính Đã đạt được:
-   ✅ **Infrastructure Ready:** A stable local development environment (Windows + GPU) and a dedicated PostgreSQL + pgvector database are fully operational.
    - ***Hạ tầng Sẵn sàng:*** *Môi trường phát triển local ổn định và CSDL chuyên dụng đã hoạt động hoàn chỉnh.*
-   ✅ **Initial Data Ingestion:** Successfully processed a full video, performing FCPXML parsing, WhisperX transcription, chunking, and vectorization, ingesting over 2,290 records into the database.
    - ***Nhập liệu Ban đầu:*** *Đã xử lý thành công một video hoàn chỉnh, thực hiện phân tích FCPXML, phiên âm WhisperX, chunking, và vector hóa, nhập liệu hơn 2,290 bản ghi vào CSDL.*
-   ✅ **Proof-of-Concept Model:** Successfully trained a baseline `KNeighborsClassifier` model (`error_classifier.pkl`) and generated a proof-of-concept FCPXML To-Do List.
    - ***Mô hình Proof-of-Concept:*** *Đã huấn luyện thành công một mô hình `KNeighborsClassifier` cơ bản và tạo ra được một file FCPXML To-Do List mẫu.*

### Strategic Pivot to v3.0 (Event-Driven Architecture) / Chuyển hướng Chiến lược sang v3.0 (Kiến trúc Hướng sự kiện)

Through deep analysis of FCPXML files, we discovered a wealth of explicit editing information (noise reduction, EQ, volume automation, etc.). To leverage this, we are upgrading the project to a more robust **"Event-Driven" architecture**.
*Thông qua phân tích sâu các file FCPXML, chúng tôi đã khám phá ra một kho thông tin chỉnh sửa tường minh. Để tận dụng điều này, chúng tôi đang nâng cấp dự án lên một kiến trúc **"Hướng sự kiện"** vững chắc hơn.*

**Instead of treating every word as an isolated chunk, the new pipeline will be centered around "Edit Events" extracted directly from FCPXML.** This will provide higher-quality labels and richer context for our AI models.
***Thay vì coi mỗi từ là một chunk riêng lẻ, pipeline mới sẽ tập trung vào các "Sự kiện Chỉnh sửa" được trích xuất trực tiếp từ FCPXML.** Điều này sẽ cung cấp các nhãn chất lượng cao hơn và ngữ cảnh phong phú hơn cho các mô hình AI của chúng ta.*

### Next Immediate Step / Bước Tiếp theo:

We are now implementing the **v3.0 Data Ingestion Pipeline**. This involves:
*Chúng ta hiện đang hiện thực hóa **Pipeline Nhập liệu v3.0**. Việc này bao gồm:*

1.  **Refactoring the FCPXML Parser** to extract all detailed "Edit Events".
    - *Tái cấu trúc Bộ phân tích FCPXML để trích xuất tất cả các "Sự kiện Chỉnh sửa" chi tiết.*
2.  **Implementing the new Database Schema** (v3.0) to store these events.
    - *Hiện thực hóa Lược đồ CSDL mới (v3.0) để lưu trữ các sự kiện này.*
3.  **Refactoring the Ingestion Pipeline** (`ingest.py`) to process data based on these events and populate the new database structure.
    - *Tái cấu trúc Pipeline Nhập liệu (`ingest.py`) để xử lý dữ liệu dựa trên các sự kiện này và điền vào cấu trúc CSDL mới.*

---

## 4. Technical Documentation / Tài liệu kỹ thuật
*   **[THEORETICAL_FRAMEWORK.md](./documents/THEORETICAL_FRAMEWORK.md):** Theoretical basic and Multi-layered Chunking.
*   **[GUIDE.md](./documents/GUIDE.md):** Operational commands (SSH Tunneling, DB management).
*   **[DATA_STRATEGY.md](./documents/DATA_STRATEGY.md):** Deep dive into data chunking and enrichment strategy.
*   **[COMPUTE_STRATEGY.md](./documents/COMPUTE_STRATEGY.md):** Analysis of compute platforms.
*   **[STORAGE_ANALYSIS.md](./documents/STORAGE_ANALYSIS.md):** Storage cost and architecture analysis.
*   **[FILE_NAMING_CONVENTION.md](./documents/FILE_NAMING_CONVENTION.md):** Rules for naming source files.
*   **[GIT_CONVENTION.md](./documents/GIT_CONVENTION.md):** Branching and commit standards.
---

### **Technology Stack / Công nghệ Sử dụng:**
-   **Language / Ngôn ngữ:** Python 3.10
-   **AI/ML:** OpenAI Whisper, Sentence Transformers (Hugging Face), Pytorch
-   **Audio Processing / Xử lý Âm thanh:** FFmpeg, Librosa, Pydub
-   **Infrastructure / Hạ tầng:** GitHub Codespaces (Development), Docker, RunPod (GPU Deployment), PostgreSQL + pgvector
-   **Orchestration / Điều phối:** n8n
