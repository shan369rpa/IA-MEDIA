# IA MEDIA - Git Workflow & Naming Convention
## IA MEDIA - Quy trình và Quy ước Git

---

This document defines the Git workflow, branch naming conventions, and commit message standards for the IA MEDIA project. Adhering to these conventions is crucial for maintaining a clean, readable, and manageable project history.

*Tài liệu này định nghĩa quy trình làm việc với Git, quy ước đặt tên nhánh, và tiêu chuẩn cho thông điệp commit của dự án IA MEDIA. Việc tuân thủ các quy ước này là cực kỳ quan-trọng để duy trì một lịch sử dự án sạch sẽ, dễ đọc, và dễ quản lý.*

---

## 1. Branching Strategy / Chiến lược Phân nhánh

We use a simplified Git Flow model with three main long-lived branches and short-lived feature branches.
*Chúng ta sử dụng mô hình Git Flow đơn giản hóa với ba nhánh chính tồn tại lâu dài và các nhánh tính năng tồn tại ngắn hạn.*

-   **`prod`:** The production branch. Contains the most stable, released code. Deploys to the Hugging Face Space are triggered from this branch.
    - ***`prod` (Sản phẩm):*** *Nhánh sản phẩm. Chứa mã nguồn ổn định nhất, đã được phát hành. Việc triển khai lên Hugging Face Space được kích hoạt từ nhánh này.*

-   **`dev`:** The main development and integration branch. All feature branches are merged into `dev` for testing. This branch should always be in a runnable state.
    - ***`dev` (Phát triển):*** *Nhánh phát triển và tích hợp chính. Tất cả các nhánh tính năng sẽ được hợp nhất vào `dev` để kiểm thử. Nhánh này phải luôn ở trạng thái có thể chạy được.*

-   **`test`:** (Optional) A staging branch for deploying to a test environment before merging into `dev`.
    - ***`test` (Kiểm thử):*** *(Tùy chọn) Một nhánh dàn dựng để triển khai lên môi trường kiểm thử trước khi hợp nhất vào `dev`.*

---

## 2. Branch Naming Convention / Quy ước Đặt tên Nhánh

All new work must be done on a feature branch created from `dev`. Branch names should be descriptive, in English, lowercase, and use hyphens `-` to separate words.
*Tất cả công việc mới phải được thực hiện trên một nhánh tính năng được tạo ra từ `dev`. Tên nhánh phải có tính mô tả, bằng tiếng Anh, viết thường, và sử dụng dấu gạch ngang `-` để phân cách các từ.*

### Format / Định dạng:
`<type>/<short-description>`

### Branch Types / Các loại Nhánh:

-   **`feature/`:** For developing a new feature or functionality.
    - ***`feature/` (Tính năng):*** *Dùng để phát triển một tính năng hoặc chức năng mới.*
    - **Example:** `feature/core-analysis-pipeline`, `feature/add-gradio-interface`

-   **`fix/`:** For fixing a bug.
    - ***`fix/` (Sửa lỗi):*** *Dùng để sửa một lỗi.*
    - **Example:** `fix/database-connection-timeout`, `fix/incorrect-xml-parsing`

-   **`docs/`:** For adding or improving documentation.
    - ***`docs/` (Tài liệu):*** *Dùng để thêm hoặc cải thiện tài liệu.*
    - **Example:** `docs/update-readme-with-new-schema`

-   **`refactor/`:** For refactoring code without changing its external behavior.
    - ***`refactor/` (Tái cấu trúc):*** *Dùng để tái cấu trúc code mà không làm thay đổi hành vi bên ngoài của nó.*
    - **Example:** `refactor/move-db-logic-to-separate-module`

-   **`chore/`:** For routine tasks, configuration, or maintenance that don't fit other categories.
    - ***`chore/` (Việc vặt):*** *Dùng cho các công việc thường lệ, cấu hình, hoặc bảo trì không thuộc các loại khác.*
    - **Example:** `chore/update-python-dependencies`, `chore/configure-ci-workflow`

---

## 3. Commit Message Convention / Quy ước Thông điệp Commit

We follow the **Conventional Commits** standard. This makes the history easy to read and allows for automated changelog generation in the future.
*Chúng ta tuân theo tiêu chuẩn **Conventional Commits**. Điều này giúp lịch sử commit dễ đọc và cho phép tự động tạo ra nhật ký thay đổi (changelog) trong tương lai.*

### Format / Định dạng:
`<type>(<scope>): <subject>`
` `
`<body>`
` `
`<footer>`

### Commit Types / Các loại Commit:

-   **`feat`:** A new feature.
-   **`fix`:** A bug fix.
-   **`docs`:** Documentation only changes.
-   **`style`:** Changes that do not affect the meaning of the code (white-space, formatting, etc.).
-   **`refactor`:** A code change that neither fixes a bug nor adds a feature.
-   **`perf`:** A code change that improves performance.
-   **`test`:** Adding missing tests or correcting existing tests.
-   **`chore`:** Changes to the build process or auxiliary tools.

### Examples / Ví dụ:

**Good Commit (Simple):**
```
feat: Add Gradio interface for pipeline control
```

**Excellent Commit (Detailed):**
```
feat(database): Implement multi-table relational schema

- Replaces the single `audio_chunks` table with a normalized schema including `sources`, `sentences`, `words`, and `anomalies`.
- Updates `vector_db_setup.sql` to automatically drop old tables and create the new structure.
- This new schema provides better data integrity and query flexibility.

Resolves: #12
```

---

## 4. Pull Request (PR) Workflow / Quy trình Pull Request (PR)

1.  **Create Branch:** Always create a new feature branch from the latest version of `dev`.
    - `git checkout dev && git pull && git checkout -b <type>/<branch-name>`
2.  **Develop & Commit:** Work on your feature and commit your changes frequently with clear messages.
3.  **Push:** Push your feature branch to the remote repository.
    - `git push -u origin <type>/<branch-name>`
4.  **Create Pull Request:** On GitHub, create a new Pull Request from your feature branch into the `dev` branch.
5.  **Describe PR:** Write a clear title and description for your PR. Explain *what* the PR does and *why*. If it resolves a GitHub Issue, link to it (e.g., "Resolves #12").
6.  **Review:** The PR will be reviewed. Discuss any feedback and make necessary changes.
7.  **Merge:** Once approved, the PR will be merged into `dev`.
8.  **Clean up:** Delete your feature branch after it has been merged.

---
```