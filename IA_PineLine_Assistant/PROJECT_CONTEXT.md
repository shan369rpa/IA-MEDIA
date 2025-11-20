**Mục đích:** Đây là "bộ não" chứa thông tin nền tảng của dự án. `n8n` sẽ đọc nội dung file này trong mỗi lần chạy.

# Project Context: IA MEDIA / Bối cảnh Dự án: IA MEDIA

## 1. Mission Statement / Tuyên bố Sứ mệnh
- **Objective / Mục tiêu:** To build an Intelligent Automation system to optimize the audio editing workflow for the remaining 300 dharma talk videos.
- **Vision / Tầm nhìn:** To create a reusable, self-improving technological asset that standardizes the quality of media products.
- **End-Users / Người dùng cuối:** A team of 10 editors working 4 hours/day using Final Cut Pro.

## 2. Stakeholders & Roles / Các bên liên quan & Vai trò
- **Project Manager:** [Tên của bạn] - Decision-maker, progress manager.
- **Developer(s):** [Tên developer/PM with AI support] - Implements the technical solution.
- **AI Assistant:** Gemini - A multi-disciplinary team member providing technical consulting, debugging, project management support, and data analysis.

## 3. Technology Stack / Kho Công nghệ
- **Development / Phát triển:** GitHub Codespaces (VS Code Web).
- **Language & Runtime / Ngôn ngữ & Runtime:** Python 3.10 on Debian Bullseye.
- **Infrastructure / Hạ tầng:**
  - **Orchestration / Điều phối:** n8n (self-hosted).
  - **Database / CSDL:** PostgreSQL + pgvector (self-hosted). **This DB is also used by NocoDB for task management.**
  - **Task Management Interface / Giao diện Quản lý Task:** NocoDB (self-hosted).
  - **AI Service Deployment / Triển khai AI Service:** Docker on RunPod (GPU).
- **Core AI Models / Các Model AI chính:**
  - **STT:** Whisper (`base` -> `small`).
  - **Embedding:** `speechbrain/spkrec-ecapa-voxceleb`.
  - **LLM (Phase 2):** OpenAI API -> Llama 3 8B.

## 4. Data & Artifacts / Dữ liệu & Sản phẩm
- **Inputs / Đầu vào:** `raw` video, `edited` video, `FCPXML` file.
- **Phase 1 Output / Đầu ra Giai đoạn 1:** `FCPXML` file with To-Do Markers.
- **Generated Data / Dữ liệu được tạo ra:** `workspace/phonetic_chunks` directory containing `clean`/`error` audio pairs.

## 5. Working Principles / Nguyên tắc Làm việc
- **Code Management / Quản lý code:** All code must be committed to the `IA-MEDIA` GitHub repo.
- **Configuration Management / Quản lý cấu hình:** Use `.env` files for configuration; never commit them to Git.
- **Progress Tracking / Quản lý tiến độ:** All tasks are tracked on NocoDB, with the underlying data stored in PostgreSQL.
- **AI Interaction / Tương tác với AI:** Work sessions are initiated by providing the AI with the context from the `IA_MEDIA_AI_CONTEXT.gdoc` file.