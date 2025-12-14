-- migrations/002_refactor_label_column.sql
-- Kịch bản tái cấu trúc cột label trong bảng "words".
-- 1. Xóa các cột 'label_clean', 'label_error' nếu tồn tại.
-- 2. Thêm cột 'label' duy nhất nếu chưa tồn tại.

\echo 'Bắt đầu tái cấu trúc cột label cho bảng "words"...'

DO $$
BEGIN
    -- Xóa cột 'label_clean' nếu tồn tại
    IF EXISTS(SELECT 1 FROM information_schema.columns WHERE table_name = 'words' AND column_name = 'label_clean') THEN
        ALTER TABLE "words" DROP COLUMN "label_clean";
        RAISE NOTICE '--> Đã xóa cột "label_clean".';
    END IF;

    -- Xóa cột 'label_error' nếu tồn tại
    IF EXISTS(SELECT 1 FROM information_schema.columns WHERE table_name = 'words' AND column_name = 'label_error') THEN
        ALTER TABLE "words" DROP COLUMN "label_error";
        RAISE NOTICE '--> Đã xóa cột "label_error".';
    END IF;

    -- Thêm cột 'label' duy nhất nếu chưa tồn tại
    IF NOT EXISTS(SELECT 1 FROM information_schema.columns WHERE table_name = 'words' AND column_name = 'label') THEN
        ALTER TABLE "words" ADD COLUMN "label" VARCHAR(50);
        RAISE NOTICE '--> Đã thêm thành công cột "label" duy nhất.';
    ELSE
        RAISE NOTICE '--> Cột "label" đã tồn tại.';
    END IF;
END $$;

\echo 'Tái cấu trúc cột label hoàn tất.'