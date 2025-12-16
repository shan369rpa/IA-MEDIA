# IA MEDIA - Technical Overview
## IA MEDIA - Tổng quan Kỹ thuật

**Last Updated / Cập nhật lần cuối:** 2025-12-15
**Version / Phiên bản:** 1.0

---

## 1. Abstract & Problem Statement / Tóm tắt & Bối cảnh Vấn đề

This document provides a technical overview of the IA MEDIA project, an open-source pipeline designed to automatically detect and classify audio defects in a large corpus of dharma talk videos (~2000 hours). The primary input for the training phase is a pair of videos for each session: a `raw` version and a human-`edited` version, along with a Final Cut Pro XML file (`.fcpxml`).

The core challenge is to leverage the implicit corrections made by human editors to create a labeled dataset of audio defects. This dataset is then used to train a model that can predict errors in new, unedited `raw` videos. The final output is an FCPXML "To-Do List" with color-coded markers pointing to potential errors, designed to accelerate the workflow of the media editing team.

*Tài liệu này cung cấp một cái nhìn tổng quan về kỹ thuật của dự án IA MEDIA, một pipeline mã nguồn mở được thiết kế để tự động phát hiện và phân loại các lỗi âm thanh trong một kho video pháp thoại lớn (~2000 giờ). Dữ liệu đầu vào chính cho giai đoạn huấn luyện là một cặp video cho mỗi buổi: một phiên bản `raw` (thô) và một phiên bản `edited` (đã được con người chỉnh sửa), cùng với một file XML của Final Cut Pro (`.fcpxml`).*

*Thách thức cốt lõi là tận dụng những chỉnh sửa ngầm định của biên tập viên để tạo ra một bộ dữ liệu lỗi âm thanh đã được gán nhãn. Bộ dữ liệu này sau đó được sử dụng để huấn luyện một mô hình có khả năng dự đoán lỗi trong các video `raw` mới, chưa được chỉnh sửa. Đầu ra cuối cùng là một file FCPXML "To-Do List" với các dấu đánh dấu được tô màu, chỉ đến các lỗi tiềm ẩn, nhằm mục đích tăng tốc quy trình làm việc của đội ngũ biên tập media.*

---

## 2. Project Status / Tình trạng Dự án

### 2.1. What Has Been Done / Những gì Đã Hoàn thành

-   **✅ Infrastructure Setup:** A stable local development environment (Windows + NVIDIA GPU) has been configured. A dedicated PostgreSQL + pgvector database is deployed and accessible.
-   **✅ Data Ingestion Pipeline (End-to-End):** The complete data processing pipeline (`main.py` -> `vectorize.py`) has been successfully executed.
    -   It correctly parses FCPXML files for time alignment.
    -   It uses WhisperX with a `large-v2` model for accurate transcription and forced alignment.
    -   It generates paired `clean`/`error` audio chunks.
    -   It automatically labels technical defects (`clipping`, `noise_spike`, etc.) using signal analysis.
    -   It generates embeddings for all chunks using a `SpeechBrain` model.
    -   It successfully ingests all data into the multi-table relational database.
-   **✅ Initial Model Training:** An initial error classification model (`KNeighborsClassifier`) has been trained on the first batch of data and saved as `error_classifier.pkl`.

***✅ Đã Hoàn thành:*** *Thiết lập hạ tầng; Thực thi thành công pipeline nhập liệu từ đầu đến cuối (phân tích FCPXML, phiên âm WhisperX, chunking, gán nhãn, vector hóa, và lưu vào CSDL); Huấn luyện thành công mô hình phân loại lỗi ban đầu.*

### 2.2. What Needs to Be Done Next / Những gì Cần Làm Tiếp theo

1.  **Implement the Inference Pipeline (`analyze_new_video.py`):** Build the script that uses the trained classifier to analyze new raw videos.
2.  **Implement the FCPXML Report Generator (`fcpxml_generator.py`):** Build the module to create the final To-Do List output file.
3.  **Establish the Human-in-the-Loop Feedback Process:** Implement the workflow for collecting, parsing, and utilizing feedback from the Media Team to retrain and improve the model.

***➡️ Cần Làm Tiếp:*** *Hiện thực hóa Pipeline Suy luận để phân tích video mới; Hiện thực hóa Module tạo Báo cáo FCPXML; Thiết lập Quy trình Phản hồi để thu thập feedback và cải tiến mô hình.*

---

## 3. End-to-End Pipeline Architecture / Kiến trúc Pipeline Toàn diện

### 3.1. Data Ingestion & Training Pipeline / Pipeline Nhập liệu & Huấn luyện

This pipeline processes existing edited sessions to build our VectorDB and classifier model.
*Pipeline này xử lý các buổi đã được chỉnh sửa để xây dựng VectorDB và mô hình phân loại.*