-- =============================================================================
-- KỊCH BẢN KHỞI TẠO CSDL NÂNG CAO - DỰ ÁN IA MEDIA
-- Version 2.0
-- Tự động dọn dẹp và tạo lại toàn bộ cấu trúc CSDL.
-- =============================================================================

\set QUIET on
\echo 'Bắt đầu khởi tạo/tái tạo cấu trúc CSDL nâng cao...'
\set QUIET off

-- -----------------------------------------------------------------------------
-- BƯỚC 0: DỌN DẸP CẤU TRÚC CŨ (Sử dụng CASCADE để xóa các phụ thuộc)
-- -----------------------------------------------------------------------------
\echo '--> BƯỚC 0: Đang dọn dẹp các bảng cũ...'
DROP TABLE IF EXISTS "anomalies" CASCADE;
DROP TABLE IF EXISTS "words" CASCADE;
DROP TABLE IF EXISTS "sentences" CASCADE;
DROP TABLE IF EXISTS "sources" CASCADE;
\echo '--> Các bảng cũ đã được dọn dẹp.'

-- -----------------------------------------------------------------------------
-- BƯỚC 1: KÍCH HOẠT EXTENSION `vector`
-- -----------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS vector;
\echo '--> BƯỚC 1: Extension "vector" đã được kích hoạt.'

-- -----------------------------------------------------------------------------
-- BƯỚC 2: TẠO CÁC BẢNG MỚI
-- -----------------------------------------------------------------------------
\echo '--> BƯỚC 2: Đang tạo các bảng mới...'

-- Bảng `sources`
CREATE TABLE "sources" (
    "id" SERIAL PRIMARY KEY,
    "video_name" TEXT UNIQUE NOT NULL,
    "duration_sec" FLOAT,
    "path_to_raw" TEXT,
    "path_to_edited" TEXT,
    "fcpxml_path" TEXT,
    "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "sources" IS '{"uit":"Grid","v":"1.0"}';
\echo '    - Bảng "sources" đã được tạo.'

-- Bảng `sentences`
CREATE TABLE "sentences" (
    "id" SERIAL PRIMARY KEY,
    "source_id" INTEGER NOT NULL REFERENCES "sources"("id") ON DELETE CASCADE,
    "transcript" TEXT,
    "start_time_ms" BIGINT NOT NULL,
    "end_time_ms" BIGINT NOT NULL,
    "embedding" VECTOR(192), -- Đã cập nhật kích thước
    "acoustic_features" JSONB,
    "emotion_label" VARCHAR(50),
    "audio_path_clean" TEXT UNIQUE,
    "video_path_clean" TEXT UNIQUE
);
\echo '    - Bảng "sentences" đã được tạo.'

-- Bảng `words`
CREATE TABLE "words" (
    "id" SERIAL PRIMARY KEY,
    "sentence_id" INTEGER NOT NULL REFERENCES "sentences"("id") ON DELETE CASCADE,
    "word_text" TEXT NOT NULL,
    "language" VARCHAR(5) NOT NULL,
    "start_time_ms_edited" BIGINT NOT NULL,
    "end_time_ms_edited" BIGINT NOT NULL,
    "embedding_clean" VECTOR(192), -- Đã cập nhật kích thước
    "embedding_error" VECTOR(192), -- Đã cập nhật kích thước
    "acoustic_features_diff" JSONB,
    "audio_path_clean" TEXT UNIQUE,
    "audio_path_error" TEXT UNIQUE,
    "video_path_clean" TEXT UNIQUE,
    "video_path_error" TEXT UNIQUE,
    "spectrogram_diff_path" TEXT
);
\echo '    - Bảng "words" đã được tạo.'

-- Bảng `anomalies`
CREATE TABLE "anomalies" (
    "id" SERIAL PRIMARY KEY,
    "source_id" INTEGER NOT NULL REFERENCES "sources"("id") ON DELETE CASCADE,
    "start_time_ms" BIGINT NOT NULL,
    "end_time_ms" BIGINT NOT NULL,
    "anomaly_type" TEXT NOT NULL,
    "confidence_score" FLOAT,
    "details" JSONB,
    "related_word_id" INTEGER REFERENCES "words"("id") ON DELETE SET NULL,
    "related_sentence_id" INTEGER REFERENCES "sentences"("id") ON DELETE SET NULL
);
\echo '    - Bảng "anomalies" đã được tạo.'


-- -----------------------------------------------------------------------------
-- BƯỚC 3: TẠO CÁC INDEX ĐỂ TĂNG TỐC
-- -----------------------------------------------------------------------------
\echo '--> BƯỚC 3: Đang tạo các index...'

-- Index cho tìm kiếm vector
CREATE INDEX ON "sentences" USING ivfflat ("embedding" vector_cosine_ops) WITH (lists = 100);
CREATE INDEX ON "words" USING ivfflat ("embedding_clean" vector_cosine_ops) WITH (lists = 100);
CREATE INDEX ON "words" USING ivfflat ("embedding_error" vector_cosine_ops) WITH (lists = 100);

-- Index cho các khóa ngoại để tăng tốc JOIN
CREATE INDEX ON "sentences" ("source_id");
CREATE INDEX ON "words" ("sentence_id");
CREATE INDEX ON "anomalies" ("source_id");
CREATE INDEX ON "anomalies" ("related_word_id");
CREATE INDEX ON "anomalies" ("related_sentence_id");

\echo '--> Các index đã được tạo.'

-- =============================================================================
\set QUIET on
\echo '>>>>>> HOÀN TẤT! Toàn bộ cấu trúc CSDL đã được tái tạo thành công.'
\set QUIET off
-- =============================================================================