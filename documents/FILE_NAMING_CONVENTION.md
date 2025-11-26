# IA MEDIA - File Naming Convention
## IA MEDIA - Quy ước Đặt tên File

---

## 1. Overview / Tổng quan

To ensure the automated processing pipeline runs smoothly and reliably, all source files must adhere to a strict and consistent naming convention. This document defines that convention. All files related to a single dharma talk (a "session") must share a common **Session ID**.

*Để đảm bảo pipeline xử lý tự động hoạt động một cách trơn tru và đáng tin cậy, tất cả các file nguồn phải tuân thủ một quy ước đặt tên nghiêm ngặt và nhất quán. Tài liệu này định nghĩa quy ước đó. Tất cả các file liên quan đến cùng một bài pháp thoại (một "buổi") phải chia sẻ chung một **Mã định danh Buổi (Session ID)**.*

---

## 2. Session ID Format / Định dạng của Session ID

The **Session ID** is the unique identifier for a dharma talk. It should be descriptive, contain no spaces or special characters (except hyphens `-`), and be in lowercase.
*Session ID là mã định danh duy nhất cho một bài pháp thoại. Nó nên có tính mô tả, không chứa khoảng trắng hoặc ký tự đặc biệt (trừ dấu gạch ngang `-`), và được viết bằng chữ thường.*

-   **Format / Định dạng:** `YYYY-MM-DD-<topic-or-location>`
-   **Example / Ví dụ:**
    -   `2010-06-15-blue-cliff-monastery`
    -   `2012-08-01-upper-hamlet-vietnamese`

---

## 3. File Naming Rules / Quy tắc Đặt tên File

For each session, there must be a set of three corresponding files. All files must be placed within the same batch directory (e.g., `source_data/Batch_01/`).
*Với mỗi buổi, phải có một bộ ba file tương ứng. Tất cả các file phải được đặt trong cùng một thư mục lô (ví dụ: `source_data/Batch_01/`).*

### 3.1. Raw Video File / File Video Thô

-   **Suffix / Hậu tố:** `_raw`
-   **Format / Định dạng:** `{Session-ID}_raw.{extension}`
-   **Example / Ví dụ:** `2010-06-15-blue-cliff-monastery_raw.mp4`

### 3.2. Edited Video File / File Video Đã Chỉnh sửa

-   **Suffix / Hậu tố:** `_edited`
-   **Format / Định dạng:** `{Session-ID}_edited.{extension}`
-   **Example / Ví dụ:** `2010-06-15-blue-cliff-monastery_edited.mp4`

### 3.3. Final Cut Pro XML File / File XML của Final Cut Pro

-   **Suffix / Hậu tố:** (none / không có)
-   **Format / Định dạng:** `{Session-ID}.fcpxml`
-   **Example / Ví dụ:** `2010-06-15-blue-cliff-monastery.fcpxml`

---

## 4. Example File Set / Ví dụ về một Bộ File Hoàn chỉnh

All of these files must exist in the same source directory for the pipeline to process them successfully.
*Tất cả các file này phải tồn tại trong cùng một thư mục nguồn để pipeline có thể xử lý chúng thành công.*

```
source_data/Batch_01/
│
├── 2010-06-15-blue-cliff-monastery_raw.mp4
├── 2010-06-15-blue-cliff-monastery_edited.mp4
└── 2010-06-15-blue-cliff-monastery.fcpxml
```

---

## 5. How the Pipeline Uses This Convention / Cách Pipeline Sử dụng Quy ước này

The pipeline is designed to be "FCPXML-driven".
*Pipeline được thiết kế để "vận hành dựa trên file FCPXML".*

1.  It scans the source directory for all `*.fcpxml` files.
2.  For each FCPXML file found (e.g., `2010-06-15-blue-cliff-monastery.fcpxml`), it extracts the **Session ID** (`2010-06-15-blue-cliff-monastery`).
3.  It then constructs the expected filenames for the raw and edited videos using this Session ID and looks for them in the same directory.
4.  If all three files are found, the session is processed. If not, it is skipped, and a warning is logged.

*1. Nó quét thư mục nguồn để tìm tất cả các file `*.fcpxml`.*
*2. Với mỗi file FCPXML tìm thấy, nó sẽ trích xuất ra **Session ID**.*
*3. Sau đó, nó xây dựng tên file dự kiến cho video thô và đã sửa bằng Session ID này và tìm kiếm chúng trong cùng thư mục.*
*4. Nếu tìm thấy cả ba file, buổi đó sẽ được xử lý. Nếu không, nó sẽ bị bỏ qua và một cảnh báo sẽ được ghi lại.*