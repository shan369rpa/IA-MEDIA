**Mục đích:** File này giải thích **Mục tiêu, Cách hoạt động, và Hướng dẫn sử dụng** của chính module "IA PineLine Assistant". Nó dành cho bất kỳ ai (kể cả bạn trong tương lai) muốn hiểu module tự động hóa này làm gì.

# IA PineLine Assistant Module

## Overview / Tổng quan

This module is the central nervous system for integrating the AI Assistant (Gemini) deeply into the **IA MEDIA** project workflow. Its primary purpose is to automate the process of updating the AI's context, ensuring that it always has the most current information about the project's status and technical architecture.

Module này là hệ thần kinh trung ương cho việc tích hợp sâu Trợ lý AI (Gemini) vào luồng làm việc của dự án **IA MEDIA**. Mục đích chính là tự động hóa quy trình cập nhật bối cảnh cho AI, đảm bảo rằng AI luôn có thông tin mới nhất về trạng thái và kiến trúc kỹ thuật của dự án.

---

## Workflow / Luồng hoạt động

The assistant operates on a "pull" model, where its long-term memory is stored in a centralized Google Doc. This workflow automates the "push" of new information into that memory file by directly querying the project's databases and repositories.

Trợ lý hoạt động theo mô hình "pull" (kéo), nơi bộ nhớ dài hạn của nó được lưu trữ trong một file Google Doc tập trung. Luồng công việc này sẽ tự động hóa việc "push" (đẩy) thông tin mới vào file trí nhớ đó bằng cách truy vấn trực tiếp vào cơ sở dữ liệu và kho mã nguồn của dự án.

```
EVENT                                   n8n WORKFLOW                                         MEMORY                            USER ACTION
Sự kiện                                  Luồng làm việc n8n                                   Bộ nhớ                            Hành động của người dùng
-----------------                       ----------------------------                         -------------------------         ----------------------------
| Task Update   |                       | 1. Get Project Context |                       |                         |
| (NocoDB)      | -- Webhook Trigger -> |    (From GitHub)       | -- Update via API ->  | IA_MEDIA_AI_CONTEXT.gdoc| --> | 1. Attach Doc in AI Studio |
|---------------|                       |------------------------|                       | (Google Drive)          |     |----------------------------|
| Code Push     |                       | 2. Get Task Progress   |                       |                         |     | 2. Start Conversation      |
| (GitHub)      |                       |    (From PostgreSQL DB)|                       |                         |
-----------------                       ----------------------------                         -------------------------         ----------------------------
```

---

## Components / Các thành phần

1.  **`PROJECT_CONTEXT.md`:**
    -   **Purpose:** The AI's "long-term memory". Contains static, foundational information about the project (mission, tech stack, stakeholders).
    -   **Mục đích:** "Bộ nhớ dài hạn" của AI. Chứa các thông tin nền tảng, ít thay đổi của dự án (sứ mệnh, công nghệ, các bên liên quan).

2.  **`SYSTEM_MESSAGE.md`:**
    -   **Purpose:** A template file. The n8n workflow uses this structure to build the final content that gets written to the Google Doc.
    -   **Mục đích:** Một file mẫu. Luồng làm việc của n8n sử dụng cấu trúc này để xây dựng nội dung cuối cùng được ghi vào file Google Doc.

3.  **`IA_MEDIA_AI_CONTEXT.gdoc` (on Google Drive):**
    -   **Purpose:** The single source of truth for the AI's current context. This is the file that is automatically updated by n8n.
    -   **Mục đích:** Nguồn thông tin chính xác duy nhất về bối cảnh hiện tại cho AI. Đây là file được n8n tự động cập nhật.

4.  **PostgreSQL Database:**
    -   **Purpose:** The database used by NocoDB to store project tasks. The n8n workflow connects **directly** to this database to fetch the most up-to-date task statuses for higher efficiency and flexibility.
    -   **Mục đích:** Cơ sở dữ liệu được NocoDB sử dụng để lưu trữ các công việc của dự án. Luồng công việc của n8n sẽ kết nối **trực tiếp** tới CSDL này để lấy trạng thái công việc mới nhất, mang lại hiệu quả và sự linh hoạt cao hơn.

---

## How to Use / Hướng dẫn sử dụng

1.  **Work Normally:** Update your tasks on NocoDB or push code to GitHub as usual.
2.  **Automation Runs:** The n8n workflow triggers automatically in the background, queries the PostgreSQL database and GitHub repository, and updates the `IA_MEDIA_AI_CONTEXT.gdoc` file on Google Drive.
3.  **Start AI Session:**
    -   Open Google AI Studio.
    -   Start a new chat.
    -   Attach the `IA_MEDIA_AI_CONTEXT.gdoc` file from Google Drive.
    -   Use a simple prompt like: "Based on the attached context, let's continue working on..."
    
---
```