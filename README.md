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

## 3. Current Status: Phase 1 Demo COMPLETED / Trạng thái Hiện tại: Demo Giai đoạn 1 HOÀN THÀNH

**We have successfully completed a full end-to-end demonstration of the entire Phase 1 pipeline, from raw video input to a final FCPXML "To-Do List" output.**
**Chúng ta đã thực thi thành công một bản demo hoàn chỉnh từ đầu đến cuối cho toàn bộ Giai đoạn 1, từ video thô đầu vào cho đến file FCPXML "To-Do List" đầu ra.**

### Key Accomplishments / Thành tựu Chính Đã đạt được:

-   ✅ **End-to-End Pipeline Execution:** Successfully processed a sample video, performing FCPXML parsing, WhisperX transcription with forced alignment, audio chunking, and vectorization. **2,290 records** were successfully ingested into the PostgreSQL database.
    - ***Thực thi Pipeline Từ-đầu-đến-cuối:*** *Đã xử lý thành công một video mẫu, thực hiện phân tích FCPXML, phiên âm và căn chỉnh bằng WhisperX, cắt chunk audio, và vector hóa. **2,290 bản ghi** đã được nhập thành công vào CSDL PostgreSQL.*

-   ✅ **Machine Learning Model Trained:** Successfully trained a `KNeighborsClassifier` model on the generated data to classify different types of audio defects. The trained model (`error_classifier.pkl`) is now ready for inference.
    - ***Mô hình Học máy được Huấn luyện:*** *Đã huấn luyện thành công một mô hình `KNeighborsClassifier` trên dữ liệu được tạo ra để phân loại các loại lỗi âm thanh khác nhau. Mô hình đã huấn luyện (`error_classifier.pkl`) hiện đã sẵn sàng để suy luận.*

-   ✅ **Final Product Generated:** Successfully executed the inference pipeline (`analyze_new_video.py`) which uses the trained model to detect errors in a new video and generates a final, usable **FCPXML To-Do List** with colored markers.
    - ***Sản phẩm Cuối cùng được Tạo ra:*** *Đã thực thi thành công pipeline suy luận (`analyze_new_video.py`), sử dụng mô hình đã huấn luyện để phát hiện lỗi trong video mới và tạo ra một file **FCPXML To-Do List** cuối cùng, có thể sử dụng được, với các marker được tô màu.*

### Next Immediate Step / Bước Tiếp theo:

The project will now focus on **improving the accuracy of the classifier model** by implementing a human-in-the-loop feedback system and experimenting with advanced machine learning techniques.
*Dự án bây giờ sẽ tập trung vào việc **cải thiện độ chính xác của mô hình phân loại** bằng cách triển khai một hệ thống phản hồi có con người tham gia và thử nghiệm các kỹ thuật học máy nâng cao.*

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
