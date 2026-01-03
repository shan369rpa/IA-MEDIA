-- migrations/004_refactor_to_clips.sql

-- 1. Xóa bảng cũ
DROP TABLE IF EXISTS "edit_events" CASCADE;

-- 2. Tạo bảng MỚI: edit_clips
CREATE TABLE "edit_clips" (
    "id" SERIAL PRIMARY KEY,
    "source_id" INTEGER NOT NULL REFERENCES "sources"("id") ON DELETE CASCADE,
    
    "start_ms" BIGINT NOT NULL, -- Thời điểm bắt đầu trên timeline edited
    "end_ms" BIGINT NOT NULL,   -- Thời điểm kết thúc
    
    "clip_type" VARCHAR(50),    -- asset-clip, gap, etc.
    
    "embedding_clean" VECTOR(192),
    "embedding_error" VECTOR(192),
    
    "applied_effects" JSONB,    -- Cột MỚI: Chứa danh sách các hiệu ứng ["volume", "transform"...]
    
    "audio_path_clean" TEXT,
    "audio_path_error" TEXT,
    
    "created_at" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ON "edit_clips" ("source_id");
CREATE INDEX ON "edit_clips" USING ivfflat ("embedding_clean" vector_cosine_ops);