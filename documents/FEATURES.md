# IA MEDIA - Feature Breakdown & Branching Guide
## IA MEDIA - Phân tích Tính năng & Hướng dẫn Phân nhánh

This document lists the main features planned for the project, broken down by phase. It also provides suggested branch names to be used during development, following our Git convention.

*Tài liệu này liệt kê các tính năng chính được lên kế hoạch cho dự án, được chia theo từng giai đoạn. Nó cũng cung cấp các tên nhánh được gợi ý để sử dụng trong quá trình phát triển, tuân thủ theo quy ước Git của chúng ta.*

---

## Phase 1: Core Analysis & Data Foundation / Giai đoạn 1: Phân tích Lõi & Nền tảng Dữ liệu

**Objective:** Build the foundational pipeline to process source videos into a queryable, multi-table vector database.
***Mục tiêu:** Xây dựng pipeline nền tảng để xử lý video nguồn thành một cơ sở dữ liệu vector đa bảng, có thể truy vấn được.*

| Feature / Tính năng | Description / Mô tả | Suggested Branch Name / Tên Nhánh Gợi ý | Status / Trạng thái |
| :--- | :--- | :--- | :--- |
| **1.1: FCPXML Parsing** | Implement logic to parse FCPXML files and create an accurate time map between edited and raw timelines. | `feature/fcpxml-parser` | **Done** |
| **1.2: Core Pipeline Orchestration** | Build the main `main.py` script that orchestrates the entire Video -> Chunks workflow. | `feature/core-analysis-pipeline` | **In Progress** |
| **1.3: Audio/Video Chunking** | Implement the core chunking logic in `chunker.py` to cut and save all media files based on Whisper and FCPXML data. | (Part of 1.2) | **To Do** |
| **1.4: Vectorization Pipeline** | Build the `vectorize.py` script to process generated audio chunks, create embeddings, and insert them into the database. | `feature/vectorization-pipeline` | **To Do** |
| **1.5: Colab Execution Notebook** | Create and refine the Google Colab notebook (`.ipynb`) that acts as the UI to run the pipelines. | `feature/colab-runner-notebook` | **In Progress** |
| **1.6: Detailed Error Labeling** | Implement signal analysis functions to automatically assign granular error labels (`clipping`, `noise_spike`, etc.) during chunking. | `feature/detailed-error-labeling` | **To Do** |

---

## Phase 2: Community & Enhancement / Giai đoạn 2: Cộng đồng & Cải tiến

**Objective:** Enhance the dataset with community contributions and build interactive tools for exploration and error analysis.
***Mục tiêu:** Cải thiện bộ dữ liệu với sự đóng góp của cộng đồng và xây dựng các công cụ tương tác để khám phá và phân tích lỗi.*

| Feature / Tính năng | Description / Mô tả | Suggested Branch Name / Tên Nhánh Gợi ý | Status / Trạng thái |
| :--- | :--- | :--- | :--- |
| **2.1: Hugging Face Dataset Publishing** | Create scripts to prepare and upload the processed data (metadata + IA links) to the Hugging Face Hub. | `feature/hf-dataset-publishing` | **Planned** |
| **2.2: Gradio/Streamlit Data Explorer** | Build an interactive web app on HF Spaces for the community to search, filter, and inspect the dataset (video, audio, text). | `feature/build-data-explorer` | **Planned** |
| **2.3: Community Labeling Tool** | (Advanced) Develop a simple UI where the community can help verify/correct transcripts or flag missed errors. | `feature/community-labeling-tool`| **Planned** |
| **2.4: LLM-Powered Suggestion (RAG)**| Implement the RAG pipeline to provide intelligent correction suggestions for detected errors. | `feature/rag-suggestion-engine` | **Planned** |

---

## Phase 3: Automation & Model Training / Giai đoạn 3: Tự động hóa & Huấn luyện Mô hình

**Objective:** Move towards automated correction and train custom AI models on our enriched dataset.
***Mục tiêu:** Hướng tới việc tự động sửa lỗi và huấn luyện các mô hình AI tùy chỉnh trên bộ dữ liệu đã được làm giàu của chúng ta.*

| Feature / Tính năng | Description / Mô tả | Suggested Branch Name / Tên Nhánh Gợi ý | Status / Trạng thái |
| :--- | :--- | :--- | :--- |
| **3.1: Rule-Based Auto-Correction**| Implement logic to automatically fix simple errors like long silences and filler words. | `feature/rule-based-autocorrect` | **Planned** |
| **3.2: Custom Error Detection Model** | Train a custom classification model (e.g., using spectrogram difference images) on our labeled data for more accurate error detection. | `feature/train-error-detector-v1`| **Planned** |
| **3.3: AI-Powered Auto-Correction (TTS)** | (Advanced) Develop proof-of-concept for automatically replacing faulty word chunks with clean, AI-generated versions (requires a TTS model). | `feature/ai-autocorrect-poc` | **Planned** |