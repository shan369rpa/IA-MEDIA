Việc tạo tài liệu **ADR (Architecture Decision Records)** là một bước đi cực kỳ chuyên nghiệp. Nó giúp ghi lại **lý do tại sao** chúng ta lại đưa ra các quyết định kỹ thuật cụ thể tại thời điểm đó, giúp team trong tương lai (hoặc chính bạn) hiểu được bối cảnh và tránh tranh luận lại những vấn đề đã chốt.

Dựa trên toàn bộ quá trình phát triển dự án **IA MEDIA** của chúng ta, dưới đây là bộ tài liệu ADRs chuẩn, được đánh số và tổ chức trong thư mục `docs/adr/`.

---

### **Cấu trúc thư mục đề xuất**

```
docs/
└── adr/
    ├── 0001-record-architecture-decisions.md
    ├── 0002-use-postgresql-and-pgvector-for-vector-db.md
    ├── 0003-hybrid-compute-strategy-colab-and-codespaces.md
    ├── 0004-multi-tier-storage-strategy-gdrive-and-internet-archive.md
    ├── 0005-fcpxml-based-audio-video-alignment.md
    └── 0006-secure-db-access-via-ssh-tunneling.md
```

---

### **Nội dung chi tiết các file ADR**

Bạn có thể copy các nội dung dưới đây để tạo file tương ứng.

#### **1. `docs/adr/0001-record-architecture-decisions.md`**

```markdown
# 1. Record Architecture Decisions

*   Status: Accepted
*   Date: 2025-11-26

## Context
Chúng ta cần một phương pháp để ghi lại các quyết định kiến trúc quan trọng, bao gồm bối cảnh, các lựa chọn đã cân nhắc và hệ quả của quyết định đó. Nếu không có điều này, kiến thức về hệ thống sẽ bị mai một hoặc chỉ nằm trong đầu một vài cá nhân.

## Decision
Chúng ta sẽ sử dụng **Architecture Decision Records (ADRs)** để ghi lại mọi quyết định quan trọng ảnh hưởng đến kiến trúc, công nghệ, và quy trình của dự án IA MEDIA.

Các file ADR sẽ:
*   Được đánh số thứ tự (0001, 0002...).
*   Định dạng Markdown.
*   Lưu trữ trong thư mục `docs/adr/` cùng với mã nguồn.
*   Không thể thay đổi (immutable) sau khi đã được chốt (trừ khi có ADR mới thay thế).

## Consequences
*   Cần kỷ luật để viết tài liệu mỗi khi có quyết định lớn.
*   Lịch sử dự án trở nên minh bạch và dễ tiếp cận cho người mới.
```

---

#### **2. `docs/adr/0002-use-postgresql-and-pgvector-for-vector-db.md`**

```markdown
# 2. Use PostgreSQL with pgvector for Vector Database

*   Status: Accepted
*   Date: 2025-11-26

## Context
Dự án cần lưu trữ hàng triệu vector embeddings đại diện cho các đoạn âm thanh (chunk) để phục vụ việc tìm kiếm tương đồng và phát hiện lỗi.
Các lựa chọn:
1.  **Vector DB chuyên dụng (Milvus, Qdrant, Pinecone):** Hiệu năng cao nhưng tốn chi phí hoặc phức tạp để vận hành thêm một hệ thống riêng.
2.  **PostgreSQL + pgvector:** Tận dụng CSDL quan hệ có sẵn.

## Decision
Chúng ta chọn **Self-hosted PostgreSQL (containerized) kết hợp với extension `pgvector`**.

## Consequences
**Điểm tích cực:**
*   **Đơn giản hóa hạ tầng:** Không cần bảo trì 2 loại CSDL khác nhau. Dữ liệu quản lý dự án (NocoDB) và Vector Embeddings nằm chung một chỗ.
*   **Truy vấn mạnh mẽ:** Cho phép thực hiện các truy vấn kết hợp (Hybrid Search) giữa Vector và Metadata (SQL) trong cùng một câu lệnh, điều mà các Vector DB chuyên dụng thường yếu.
*   **Chi phí thấp:** Tận dụng VPS hiện có, không tốn phí cloud services.

**Điểm tiêu cực:**
*   Hiệu năng có thể thấp hơn Vector DB chuyên dụng ở quy mô cực lớn (tỷ vector), nhưng với quy mô dự án này (< 50 triệu vector), `ivfflat` index của pgvector là đủ tốt.
```

---

#### **3. `docs/adr/0003-hybrid-compute-strategy-colab-and-codespaces.md`**

```markdown
# 3. Hybrid Compute Strategy: Google Colab & GitHub Codespaces

*   Status: Accepted
*   Date: 2025-11-26

## Context
Dự án cần tài nguyên tính toán cho hai mục đích khác nhau:
1.  **Phát triển (Dev):** Cần môi trường ổn định, tích hợp Git tốt, dễ gỡ lỗi code.
2.  **Xử lý Hàng loạt (Batch Processing):** Cần GPU mạnh để chạy model AI (Whisper, Embedding) nhưng ngân sách hạn hẹp (gần như bằng 0).

Hugging Face Spaces đã thay đổi chính sách GPU miễn phí (chuyển sang ZeroGPU queue), không còn phù hợp để chạy pipeline dài.

## Decision
Chúng ta áp dụng chiến lược **Compute Lai (Hybrid Compute Strategy)**:
*   **GitHub Codespaces:** Dùng làm môi trường phát triển chính (Dev Environment). Nơi viết code, unit test, quản lý Git. (Chỉ CPU).
*   **Google Colab (Free Tier):** Dùng làm môi trường thực thi (Execution Environment). Code từ GitHub được clone về đây để tận dụng GPU T4 miễn phí xử lý các lô video.

## Consequences
**Điểm tích cực:**
*   Tận dụng được GPU miễn phí của Google.
*   Môi trường phát triển chuyên nghiệp, tách biệt với môi trường chạy.
*   Linh hoạt, dễ dàng thay thế Colab bằng Kaggle hoặc server riêng nếu cần.

**Điểm tiêu cực:**
*   Quy trình làm việc hơi phức tạp: Code ở Codespaces -> Push Github -> Pull về Colab -> Chạy.
*   Colab có giới hạn phiên (~12h), cần tương tác thủ công để chạy từng lô (batch).
```

---

#### **4. `docs/adr/0004-multi-tier-storage-strategy-gdrive-and-internet-archive.md`**

```markdown
# 4. Multi-tier Storage Strategy: Google Drive & Internet Archive

*   Status: Accepted
*   Date: 2025-11-26

## Context
Dự án dự kiến xử lý 2000 video (~2000 giờ), tạo ra khoảng 7-8 TB dữ liệu chunk.
*   Google Drive (100GB): Không đủ lưu trữ lâu dài, chỉ đủ làm bộ đệm.
*   AWS S3 / Cloud Storage: Chi phí quá cao cho dự án phi lợi nhuận.

## Decision
Chúng ta áp dụng chiến lược **Lưu trữ Đa tầng (Multi-tier Storage)**:
1.  **Staging (Dàn dựng):** Sử dụng **Google Drive** để chứa dữ liệu đầu vào (Raw/Edited Video) và nhận kết quả tạm thời từ Colab.
2.  **Long-term Archival (Lưu trữ vĩnh viễn):** Sử dụng **Internet Archive (archive.org)** để lưu trữ các file audio/video chunk vật lý. Upload ngay trong quá trình xử lý và xóa file tạm để tiết kiệm chỗ.
3.  **Metadata & Distribution:** Sử dụng **Hugging Face Datasets** để lưu trữ file `metadata.csv` chứa các đường dẫn trỏ đến Internet Archive.

## Consequences
**Điểm tích cực:**
*   **Chi phí bằng 0:** Internet Archive miễn phí không giới hạn cho dữ liệu văn hóa/cộng đồng.
*   **Bền vững:** Dữ liệu được bảo tồn lâu dài.
*   **Khả năng mở rộng:** Không lo bị tràn ổ cứng trong quá trình xử lý.

**Điểm tiêu cực:**
*   Tốc độ upload/download từ Internet Archive chậm hơn S3.
*   Quy trình upload phức tạp hơn (cần quản lý key, metadata).
```

---

#### **5. `docs/adr/0005-fcpxml-based-audio-video-alignment.md`**

```markdown
# 5. FCPXML-based Audio/Video Alignment

*   Status: Accepted
*   Date: 2025-11-26

## Context
Để tạo ra cặp dữ liệu `clean` (đã sửa) và `error` (lỗi) tương ứng nhau, chúng ta cần đồng bộ hóa (align) thời gian giữa video Raw và video Edited.
Các phương pháp xử lý tín hiệu âm thanh (như cross-correlation, DTW) thường gặp khó khăn khi video edited bị cắt xén, đảo lộn, hoặc xử lý nhiễu nền mạnh.

## Decision
Chúng ta sử dụng phương pháp **"Deterministic Alignment" dựa trên file dự án FCPXML (Final Cut Pro XML)**.
Pipeline sẽ phân tích file `.fcpxml` để trích xuất chính xác các thông số `start`, `duration`, `offset` của từng clip raw được sử dụng trong timeline edited.

## Consequences
**Điểm tích cực:**
*   **Độ chính xác tuyệt đối:** Dựa trên quyết định biên tập của con người, không phải phỏng đoán của máy.
*   **Hiệu suất cao:** Phân tích file XML (text) nhanh hơn hàng nghìn lần so với xử lý tín hiệu audio/video.

**Điểm tiêu cực:**
*   **Phụ thuộc vào quy trình:** Bắt buộc đội ngũ Media phải xuất file XML đúng quy chuẩn từ Final Cut Pro.
*   Chỉ hoạt động với workflow dùng Final Cut Pro (cần viết parser khác nếu đổi sang Premiere/DaVinci).
```

---

#### **6. `docs/adr/0006-secure-db-access-via-ssh-tunneling.md`**

```markdown
# 6. Secure Database Access via SSH Tunneling

*   Status: Accepted
*   Date: 2025-11-26

## Context
Cơ sở dữ liệu PostgreSQL nằm trên một VPS riêng (`tuduc.cloud`).
Môi trường Google Colab (Public Internet) cần kết nối vào CSDL này để ghi dữ liệu.
Việc mở cổng CSDL (5432/5433) trực tiếp ra Internet là một rủi ro bảo mật lớn.

## Decision
Chúng ta sử dụng **SSH Tunneling (Port Forwarding)** để kết nối.
*   Colab sử dụng khóa SSH (private key) để tạo một đường hầm mã hóa đến server.
*   Cổng CSDL nội bộ của server được ánh xạ về `localhost` của Colab.
*   Ứng dụng Python kết nối đến `localhost:6000` như thể DB đang chạy tại chỗ.

## Consequences
**Điểm tích cực:**
*   **Bảo mật cao:** Không cần mở cổng trên Firewall. Mọi dữ liệu truyền đi đều được mã hóa.
*   **Xác thực mạnh:** Sử dụng SSH Key thay vì chỉ mật khẩu DB.

**Điểm tiêu cực:**
*   Cần bước thiết lập SSH Key trên cả Server và Google Drive (để Colab truy cập).
*   Cần thêm code khởi tạo tunnel trong notebook.
```

---

Bạn hãy tạo các file này. Đây sẽ là tài sản vô giá để bất kỳ ai (bao gồm AI Copilot) tham gia dự án đều hiểu ngay "Tại sao chúng ta làm thế này?".