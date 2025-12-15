-- migrations/002_create_word_slices_table.sql
-- Kịch bản này tạo bảng `word_slices` và các index cần thiết.
-- An toàn để chạy lại nhiều lần.

\echo 'Bắt đầu kiểm tra và thiết lập bảng "word_slices"...'

-- -----------------------------------------------------------------------------
-- BẢNG `word_slices`
-- Lưu trữ các vector embedding của các "lát cắt" (sliding window)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "word_slices" (
    "id" SERIAL PRIMARY KEY,
    
    -- Khóa ngoại, liên kết đến từ cha trong bảng "words"
    -- ON DELETE CASCADE: Nếu từ cha bị xóa, tất cả các slice của nó cũng sẽ tự động bị xóa.
    "word_id" INTEGER NOT NULL REFERENCES "words"("id") ON DELETE CASCADE,
    
    -- Xác định slice này thuộc về phiên bản 'clean' hay 'error' của từ cha
    "source_type" VARCHAR(10) NOT NULL CHECK ("source_type" IN ('clean', 'error')),
    
    "slice_index" INTEGER NOT NULL, -- Thứ tự của lát cắt trong một từ (0, 1, 2...)
    "start_offset_ms" INTEGER,      -- (Tùy chọn) Thời điểm bắt đầu của lát cắt so với đầu của chunk từ (tính bằng ms)
    
    -- Vector embedding của lát cắt này (kích thước 192)
    "embedding" VECTOR(192),
    
    "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Đảm bảo mỗi slice trong một từ là duy nhất
    UNIQUE ("word_id", "source_type", "slice_index")
);

-- Thêm comment để NocoDB nhận diện
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_description JOIN pg_class ON pg_description.objoid = pg_class.oid
        WHERE pg_class.relname = 'word_slices'
    ) THEN
        COMMENT ON TABLE "word_slices" IS '{"uit":"Grid","v":"1.0"}';
    END IF;
END $$;

\echo '--> Bảng "word_slices" đã được kiểm tra/tạo thành công.'


-- -----------------------------------------------------------------------------
-- CÁC INDEX CẦN THIẾT
-- Để tăng tốc độ truy vấn
-- -----------------------------------------------------------------------------
\echo '--> Đang kiểm tra và tạo các index cho "word_slices"...'

-- Index trên cột vector embedding để tìm kiếm tương đồng
CREATE INDEX IF NOT EXISTS idx_word_slices_embedding ON "word_slices" USING ivfflat ("embedding" vector_cosine_ops) WITH (lists = 100);

-- Index trên khóa ngoại để tăng tốc các phép JOIN
CREATE INDEX IF NOT EXISTS idx_word_slices_word_id ON "word_slices" ("word_id");

\echo '--> Các index đã được kiểm tra/tạo thành công.'

-- =============================================================================
\echo 'Thiết lập bảng "word_slices" hoàn tất.'
-- =============================================================================