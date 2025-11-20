-- =============================================================================
-- KỊCH BẢN KHỞI TẠO CƠ SỞ DỮ LIỆU VECTOR CHO DỰ ÁN IA MEDIA
--
-- Mục đích: Tạo bảng `audio_chunks` để lưu trữ các vector embedding và metadata
--           liên quan đến các đoạn âm thanh vi mô.
--
-- Cách chạy: \i vector_db_setup.sql
-- =============================================================================

\set QUIET on
\echo 'Bắt đầu khởi tạo cấu trúc bảng vector cho dự án IA MEDIA...'
\set QUIET off

-- -----------------------------------------------------------------------------
-- BƯỚC 1: KÍCH HOẠT EXTENSION `vector`
-- Cần quyền superuser để chạy lần đầu tiên trên một database.
-- -----------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS vector;

\echo '--> Extension "vector" đã được kích hoạt.'

-- -----------------------------------------------------------------------------
-- BẢNG CHÍNH: `audio_chunks`
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "audio_chunks" (
    "id" SERIAL PRIMARY KEY,
    
    -- --- Metadata về Nguồn ---
    "source_video_name" TEXT NOT NULL,
    "word_text" TEXT NOT NULL,
    
    -- --- Thông tin Thời gian ---
    "start_time_ms" BIGINT NOT NULL,
    "end_time_ms" BIGINT NOT NULL,
    
    -- --- Nhãn và Dữ liệu ---
    "label" VARCHAR(10) NOT NULL CHECK ("label" IN ('clean', 'error')),
    "chunk_file_path" TEXT NOT NULL UNIQUE,
    
    -- --- Dữ liệu Vector ---
    -- LƯU Ý: Con số 1024 có thể cần thay đổi cho phù hợp với model embedding
    "embedding" VECTOR(1024), 
    
    -- --- Dấu thời gian ---
    "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE "audio_chunks" IS '{"uit":"Grid","v":"1.0"}';
\echo '--> Bảng "audio_chunks" đã được tạo.'


-- -----------------------------------------------------------------------------
-- BƯỚC 2: TẠO INDEX ĐỂ TĂNG TỐC TÌM KIẾM
-- Đây là bước tối quan trọng cho hiệu năng.
-- -----------------------------------------------------------------------------
-- Xóa index cũ nếu tồn tại để tránh lỗi khi chạy lại
DROP INDEX IF EXISTS idx_audio_chunks_embedding;

-- Tạo index IVFFlat với phép đo cosine distance.
-- `lists = 100` là một giá trị khởi đầu tốt cho vài triệu vector.
CREATE INDEX idx_audio_chunks_embedding ON "audio_chunks" USING ivfflat ("embedding" vector_cosine_ops) WITH (lists = 100);

\echo '--> Index IVFFlat trên cột "embedding" đã được tạo.'

-- =============================================================================
\set QUIET on
\echo '>>>>>> HOÀN TẤT! Cấu trúc CSDL Vector đã sẵn sàng.'
\set QUIET off
-- =============================================================================