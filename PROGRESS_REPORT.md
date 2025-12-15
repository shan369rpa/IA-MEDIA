# IA MEDIA - Project Progress Report
## Báo cáo Tiến độ Dự án IA MEDIA

**Date / Ngày:** 2025-12-13
**Report Version / Phiên bản Báo cáo:** 1.0
**Author / Người lập:** shan369rpa

---

## 1. Executive Summary / Tóm tắt Báo cáo

The initial development phase (Demo Phase 1) of the IA MEDIA project has made significant progress. We have successfully built and tested the foundational data processing pipeline, capable of transforming raw video/audio data into a structured format ready for AI analysis. During this process, a critical strategic pivot was made regarding the error detection mechanism, moving from a simple threshold-based model to a more sophisticated machine learning classification approach. The project is now poised to enter the "model building" stage before proceeding to the final inference and report generation tasks.

*Giai đoạn phát triển ban đầu (Demo Giai đoạn 1) của dự án IA MEDIA đã đạt được những tiến bộ đáng kể. Chúng ta đã xây dựng và kiểm thử thành công pipeline xử lý dữ liệu nền tảng, có khả năng chuyển đổi dữ liệu video/audio thô thành một định dạng có cấu trúc, sẵn sàng cho việc phân tích AI. Trong quá trình này, một sự thay đổi chiến lược quan trọng đã được thực hiện đối với cơ chế phát hiện lỗi, chuyển từ mô hình dựa trên ngưỡng đơn giản sang một phương pháp phân loại học máy tinh vi hơn. Dự án hiện đã sẵn sàng để bước vào giai đoạn "xây dựng mô hình" trước khi tiến hành các nhiệm vụ suy luận và tạo báo cáo cuối cùng.*

---

## 2. Completed Tasks / Các Công việc Đã Hoàn thành

### 2.1. Infrastructure & Environment Setup / Thiết lập Hạ tầng & Môi trường
-   **[COMPLETED]** Established a fully containerized development environment on **GitHub Codespaces**.
-   **[COMPLETED]** Deployed a dedicated, parallel **PostgreSQL 16 + pgvector** database container (`ia-media-db-pgvector`) on the production server, ensuring no disruption to existing services.
-   **[COMPLETED]** Successfully resolved complex **dependency conflicts** on the local Windows + NVIDIA environment, resulting in a stable and documented installation procedure.
-   **[COMPLETED]** Established and verified a secure **SSH Tunneling** workflow for connecting development environments (Codespaces, Colab, Local) to the private database.

### 2.2. Data Schema & Project Management / Cấu trúc Dữ liệu & Quản lý Dự án
-   **[COMPLETED]** Designed and implemented a detailed, **multi-table relational database schema** (`sources`, `sentences`, `words`, `anomalies`) to support advanced data analysis.
-   **[COMPLETED]** Integrated the new database with **NocoDB**, providing a functional UI for project task management.

### 2.3. Core Pipeline Execution / Thực thi Pipeline Cốt lõi
-   **[COMPLETED]** Successfully executed the **end-to-end analysis pipeline (`main.py`)** on the first real data sample.
-   **[COMPLETED]** The pipeline correctly performed: FCPXML parsing, audio extraction, `WhisperX` (large-v2) transcription with forced alignment, and generation of **2,290 pairs** of `clean`/`error` audio chunks into the `workspace`.
-   **[COMPLETED]** Successfully executed the **vectorization pipeline (`vectorize.py`)**, which processed all generated chunks, created `SpeechBrain` embeddings for both `clean` and `error` versions, and ingested the data into the PostgreSQL `words` and `sources` tables.

---

## 3. Strategic Pivot / Thay đổi Chiến lược Quan trọng

**Initial Approach (Obsolete):** The original plan for "Phase 1 - Stage 2" was to analyze the distance distribution between `clean` and `error` embeddings to find a single **"Error Threshold"**.

**New, Improved Approach:** Based on a deeper analysis, we recognized that every `clean`/`error` pair in our database is, by definition, an example of a corrected error. Therefore, the task is not to *find* errors, but to *learn to classify* them.

**The new "Stage 2" is now:** **Build an "Error Signature Library" and a Classifier Model.**

-   **Objective:** To train a simple machine learning model (e.g., SVM, KNN) that can predict the *type* of error (`clipping`, `noise`, `pronunciation`, etc.) based on the vector difference between a `new_raw_chunk` and its closest `clean` counterpart in the database.
-   **Benefit:** This approach is far more powerful. Instead of a simple "error/no-error" flag, the final To-Do List can provide specific, actionable feedback to editors (e.g., "Potential clipping issue at 01:15:32").

***Thay đổi Chiến lược Quan trọng:** Hướng đi ban đầu là tìm một "Ngưỡng Lỗi" duy nhất. Hướng đi mới, cải tiến hơn, là xây dựng một "Thư viện Dấu hiệu Lỗi" và huấn luyện một mô hình phân loại. Mục tiêu là dự đoán *loại* lỗi (vỡ tiếng, nhiễu, phát âm...) dựa trên sự khác biệt vector, giúp cung cấp thông tin chi tiết hơn cho biên tập viên.*

---

## 4. Remaining Tasks for Demo Completion / Các Công việc Còn lại để Hoàn thành Demo

The final output of the demo is a To-Do List FCPXML file. To achieve this, the following major stages remain:
*Đầu ra cuối cùng của bản demo là một file FCPXML To-Do List. Để đạt được điều này, các công đoạn lớn sau đây vẫn còn lại:*

### **Stage 2: Model Building / Giai đoạn 2: Xây dựng Mô hình**
-   **Task 2.1: Data Analysis Script (`scripts/analyze_db.py`):**
    -   Write a script to query all `clean`/`error` embedding pairs and their corresponding labels (`error_clipping`, etc. from the `anomalies` table - *Note: this requires running the signal analyzer first*).
    -   Calculate difference vectors (`embedding_error` - `embedding_clean`).
    -   Visualize the data to understand the separation between error types.
-   **Task 2.2: Train Classifier:**
    -   Write a script (`scripts/train_classifier.py`) using `scikit-learn`.
    -   Train a classifier (e.g., `KNeighborsClassifier`) on the difference vectors and labels.
    -   Save the trained model to a file (e.g., `error_classifier.pkl`).

### **Stage 3: Inference Pipeline / Giai đoạn 3: Pipeline Suy luận**
-   **Task 3.1: New Video Processor Script (`analyze_new_video.py`):**
    -   Create a new script that takes a single **new raw video** as input.
    -   Perform transcription and word chunking.
    -   For each new word chunk embedding, find the nearest `clean` embedding in the DB.
    -   Calculate the difference vector.
-   **Task 3.2: Error Classification:**
    -   Load the `error_classifier.pkl` model.
    -   Use the model to predict the error type for each word chunk.
    -   Collect all words flagged as potential errors, along with their timestamps and predicted error types.

### **Stage 4: Report Generation / Giai đoạn 4: Tạo Báo cáo**
-   **Task 4.1: FCPXML Generator Module (`src/utils/report_generator.py`):**
    -   Write a function that takes a list of error timestamps and messages.
    -   Programmatically generate an FCPXML string containing To-Do Markers at the specified timestamps.
-   **Task 4.2: Final Integration:**
    -   Integrate the FCPXML generator into `analyze_new_video.py` to produce the final output file.

---