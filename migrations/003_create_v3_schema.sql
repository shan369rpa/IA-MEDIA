-- migrations/003_create_v3_schema.sql
-- Kịch bản Thiết lập CSDL v3.0 (Event-Driven) cho Dự án IA MEDIA
-- Xóa toàn bộ schema cũ và xây dựng lại từ đầu.

\echo '--- BẮT ĐẦU TÁI TẠO CẤU TRÚC CSDL v3.0 ---'

-- -----------------------------------------------------------------------------
-- BƯỚC 0: DỌN DẸP CÁC BẢNG CŨ (CỦA v1 và v2)
-- -----------------------------------------------------------------------------
\echo '--> Bước 0: Đang dọn dẹp các bảng cũ...'
DROP TABLE IF EXISTS "word_slices" CASCADE;
DROP TABLE IF EXISTS "anomalies" CASCADE;
DROP TABLE IF EXISTS "words" CASCADE;
DROP TABLE IF EXISTS "sentences" CASCADE;
DROP TABLE IF EXISTS "edit_clips" CASCADE;
DROP TABLE IF EXISTS "sources" CASCADE;
\echo '--> Các bảng cũ đã được dọn dẹp.'

-- -----------------------------------------------------------------------------
-- BƯỚC 1: KÍCH HOẠT EXTENSION `vector`
-- -----------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS vector;
\echo '--> Bước 1: Extension "vector" đã được kích hoạt.'

-- -----------------------------------------------------------------------------
-- BƯỚC 2: TẠO CÁC BẢNG MỚI THEO KIẾN TRÚC v3.0
-- -----------------------------------------------------------------------------
\echo '--> Bước 2: Đang tạo các bảng mới...'

-- Bảng `sources` (Bảng gốc)
CREATE TABLE "sources" (
    "id" SERIAL PRIMARY KEY,
    "video_name" TEXT UNIQUE NOT NULL,
    "duration_sec" FLOAT,
    "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "sources" IS 'Lưu trữ thông tin về các video nguồn.';
\echo '    - Bảng "sources" đã được tạo.'

-- Bảng `edit_events` (Bảng Trung tâm Mới)
CREATE TABLE "edit_events" (
    "id" SERIAL PRIMARY KEY,
    "source_id" INTEGER NOT NULL REFERENCES "sources"("id") ON DELETE CASCADE,
    
    "start_ms" BIGINT NOT NULL,
    "end_ms" BIGINT NOT NULL,
    
    "event_source" VARCHAR(20) NOT NULL, -- Nguồn phát hiện: 'FCPXML' hoặc 'AI_MODEL'
    "event_type" TEXT NOT NULL,          -- Loại sự kiện: 'noise_reduction', 'volume_mute', 'pronunciation'...
    
    "embedding_clean" VECTOR(192),
    "embedding_error" VECTOR(192),
    
    "details" JSONB,                     -- Chi tiết kỹ thuật: {"amount": "50"}, {"value": "-96dB"}
    
    "audio_path_clean" TEXT,
    "audio_path_error" TEXT
);
COMMENT ON TABLE "edit_events" IS 'Bảng trung tâm, lưu trữ tất cả các sự kiện chỉnh sửa hoặc khác biệt.';
\echo '    - Bảng "edit_events" đã được tạo.'

-- Bảng `words` (Bảng Vi mô)
CREATE TABLE "words" (
    "id" SERIAL PRIMARY KEY,
    "source_id" INTEGER NOT NULL REFERENCES "sources"("id") ON DELETE CASCADE, -- Liên kết trực tiếp đến source
    
    "word_text" TEXT NOT NULL,
    "start_ms" BIGINT NOT NULL,
    "end_ms" BIGINT NOT NULL,
    
    "language" VARCHAR(5),
    
    "embedding_clean" VECTOR(192),
    "embedding_error" VECTOR(192),

    -- (Tùy chọn) Liên kết đến sự kiện cha chứa nó
    "parent_event_id" INTEGER REFERENCES "edit_events"("id") ON DELETE SET NULL 
);
COMMENT ON TABLE "words" IS 'Lưu trữ các từ đã được phiên âm và vector hóa.';
\echo '    - Bảng "words" đã được tạo.'


-- -----------------------------------------------------------------------------
-- BƯỚC 3: TẠO CÁC INDEX ĐỂ TĂNG TỐC
-- -----------------------------------------------------------------------------
\echo '--> Bước 3: Đang tạo các index...'

-- Index cho `edit_events`
CREATE INDEX ON "edit_events" ("source_id");
CREATE INDEX ON "edit_events" ("event_type");
CREATE INDEX ON "edit_events" USING ivfflat ("embedding_clean" vector_cosine_ops);
CREATE INDEX ON "edit_events" USING ivfflat ("embedding_error" vector_cosine_ops);

-- Index cho `words`
CREATE INDEX ON "words" ("source_id");
CREATE INDEX ON "words" ("word_text");
CREATE INDEX ON "words" ("parent_event_id");
CREATE INDEX ON "words" USING ivfflat ("embedding_clean" vector_cosine_ops);
CREATE INDEX ON "words" USING ivfflat ("embedding_error" vector_cosine_ops);

\echo '--> Các index đã được tạo.'

-- =============================================================================
\echo '--- HOÀN TẤT! Cấu trúc CSDL v3.0 đã được tạo thành công. ---'
-- =============================================================================