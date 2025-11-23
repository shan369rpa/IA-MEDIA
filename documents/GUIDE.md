# IA MEDIA - Project Operations Guide
## Hướng dẫn Vận hành Dự án IA MEDIA

This guide contains essential commands and procedures for developing and managing the IA MEDIA project.
Tài liệu này chứa các lệnh và quy trình thiết yếu để phát triển và quản lý dự án IA MEDIA.

---

## 1. Development Environment (GitHub Codespaces)
### Môi trường Phát triển (GitHub Codespaces)

The entire development environment is containerized using GitHub Codespaces.
Toàn bộ môi trường phát triển được container hóa bằng GitHub Codespaces.

### Rebuilding the Environment / Xây dựng lại Môi trường

If you make changes to `Dockerfile`, `devcontainer.json`, or `requirements.txt`, you must rebuild the container.
Nếu bạn thay đổi các file `Dockerfile`, `devcontainer.json`, hoặc `requirements.txt`, bạn phải xây dựng lại container.

1.  Open the Command Palette: `Ctrl+Shift+P` (or `Cmd+Shift+P`).
2.  Type and select: `> Codespaces: Rebuild Container`.

---

## 2. Database Management (PostgreSQL)
### Quản lý Cơ sở dữ liệu (PostgreSQL)

The project uses a PostgreSQL database running in a Docker container on the main server. We connect to it securely using an SSH tunnel.
Dự án sử dụng CSDL PostgreSQL chạy trong một container Docker trên server chính. Chúng ta kết nối đến nó một cách an toàn bằng đường hầm SSH.

### 2.1. Connecting to the Database via SSH Tunnel / Kết nối đến CSDL qua Đường hầm SSH

**Prerequisites:** You need the server's IP, root password, and database credentials (user/password).
**Yêu cầu:** Bạn cần có IP của server, mật khẩu root, và thông tin đăng nhập CSDL (user/password).

**Step 1: Open the SSH Tunnel (in Terminal 1)**
**Bước 1: Mở Đường hầm SSH (trong Terminal 1)**

This command forwards local port `6000` to the database port `5432` on the server. **Keep this terminal running.**
Lệnh này chuyển tiếp cổng `6000` ở local đến cổng CSDL `5432` trên server. **Hãy giữ cho terminal này luôn chạy.**

```bash
# Replace <SERVER_IP> with the actual IP address
ssh -L 6000:localhost:5432 root@<SERVER_IP>
```

**Step 2: Connect with `psql` (in Terminal 2)**
**Bước 2: Kết nối bằng `psql` (trong Terminal 2)**

Use this command to access the database through the tunnel.
Sử dụng lệnh này để truy cập CSDL thông qua đường hầm.

```bash
# Replace <DB_USER> and <DB_NAME> with your actual credentials
psql -h localhost -p 6000 -U <DB_USER> -d <DB_NAME>
```

### 2.2. Initializing the Database Schema / Khởi tạo Cấu trúc CSDL

This command creates all necessary tables for NocoDB project management. Run this inside an active `psql` session.
Lệnh này tạo tất cả các bảng cần thiết cho việc quản lý dự án trên NocoDB. Chạy lệnh này bên trong một phiên `psql` đang hoạt động.

```sql
\i nocodb_setup.sql
```

After running the script, remember to go to the NocoDB UI and click **"Sync with DB"**.
Sau khi chạy script, hãy nhớ vào giao diện NocoDB và nhấn **"Sync with DB"**.

### 2.3. Useful `psql` Commands / Các lệnh `psql` Hữu ích

-   `\dt`: List all tables in the current database. (Liệt kê tất cả các bảng).
-   `\d <table_name>`: Describe a table (columns, types, etc.). (Mô tả một bảng).
-   `SELECT * FROM "<table_name>" LIMIT 10;`: View the first 10 rows of a table. (Xem 10 dòng đầu tiên của bảng).
-   `\q`: Quit `psql`. (Thoát `psql`).

---

## 3. Running Project Scripts
### Chạy các Kịch bản của Dự án

All scripts should be run from the root directory of the project.
Tất cả các kịch bản nên được chạy từ thư mục gốc của dự án.

### Running the Core Analysis Pipeline / Chạy Pipeline Phân tích Lõi

This script processes a pair of videos and extracts phonetic chunks.
Kịch bản này xử lý một cặp video và trích xuất các chunk âm vị.

```bash
# Ensure your .env file is correctly configured with file paths first
python main.py 
```

### Running the Vectorization Script / Chạy Kịch bản Vector hóa

This script vectorizes the generated chunks and saves them to the database.
Kịch bản này vector hóa các chunk đã được tạo ra và lưu chúng vào CSDL.

```bash
# (This script will be created in a later step)
# python vectorize_chunks.py
```
ssh -L 6000:localhost:5433 root@180.93.137.58