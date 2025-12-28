-- =============================================================================
-- KỊCH BẢN KHỞI TẠO CƠ SỞ DỮ LIỆU CHO DỰ ÁN IA MEDIA
--
-- Mục đích: Tự động tạo các bảng quản lý dự án (`Epics`, `User_Stories`, 
--           `Project_Tasks`) và thiết lập các mối quan hệ giữa chúng.
--
-- Cách chạy:
-- 1. Kết nối đến CSDL bằng psql: 
--    psql -h <host> -p <port> -U <user> -d <database>
-- 2. Chạy lệnh: \i nocodb_setup.sql
-- =============================================================================

-- Tắt các thông báo không cần thiết để output gọn gàng hơn
\set QUIET on
\echo 'Bắt đầu khởi tạo cấu trúc bảng cho dự án IA MEDIA...'
\set QUIET off

-- -----------------------------------------------------------------------------
-- Bảng 1: Epics (Các hạng mục chức năng lớn)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "Epics" (
    "id" SERIAL PRIMARY KEY,
    "EpicName" TEXT,
    "Description" TEXT,
    "Status" VARCHAR(20) DEFAULT 'To Do' CHECK ("Status" IN ('To Do', 'In Progress', 'Done')),
    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "UpdatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Thêm comment để NocoDB nhận diện và hiển thị đúng giao diện
COMMENT ON TABLE "Epics" IS '{"uit":"Grid","v":"1.0"}';

\echo '--> Bảng "Epics" đã được tạo.'


-- -----------------------------------------------------------------------------
-- Bảng 2: User_Stories (Các câu chuyện người dùng)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "User_Stories" (
    "id" SERIAL PRIMARY KEY,
    "UserStoryID" TEXT UNIQUE, -- Đảm bảo ID là duy nhất
    "Title" TEXT NOT NULL,
    "FullStory" TEXT,
    "Status" VARCHAR(20) DEFAULT 'To Do' CHECK ("Status" IN ('To Do', 'In Progress', 'Done')),
    "Priority" VARCHAR(20) DEFAULT 'Medium' CHECK ("Priority" IN ('High', 'Medium', 'Low')),
    
    -- Mối quan hệ: Một User Story thuộc về một Epic.
    -- ON DELETE SET NULL: Nếu Epic cha bị xóa, trường này sẽ thành NULL thay vì xóa User Story.
    "Epic" INTEGER REFERENCES "Epics"("id") ON DELETE SET NULL,

    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "UpdatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE "User_Stories" IS '{"uit":"Grid","v":"1.0"}';

\echo '--> Bảng "User_Stories" đã được tạo.'


-- -----------------------------------------------------------------------------
-- Bảng 3: Project_Tasks (Các công việc kỹ thuật cụ thể)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS "Project_Tasks" (
    "id" SERIAL PRIMARY KEY,
    "TaskName" TEXT NOT NULL,
    "Description" TEXT,
    "Status" VARCHAR(20) DEFAULT 'To Do' CHECK ("Status" IN ('To Do', 'In Progress', 'Done', 'Blocked')),
    
    -- Mối quan hệ: Một Task thuộc về một User Story.
    "UserStory" INTEGER REFERENCES "User_Stories"("id") ON DELETE SET NULL,

    "Assignee" TEXT,
    "DueDate" DATE,
    "EstimatedHours" DECIMAL(5, 2),
    "ActualHours" DECIMAL(5, 2),
    "CreatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    "UpdatedAt" TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE "Project_Tasks" IS '{"uit":"Grid","v":"1.0"}';

\echo '--> Bảng "Project_Tasks" đã được tạo.'


-- -----------------------------------------------------------------------------
-- TẠO CÁC TRIGGER ĐỂ TỰ ĐỘNG CẬP NHẬT TRƯỜNG "UpdatedAt"
-- (Phần nâng cao nhưng rất hữu ích)
-- -----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW."UpdatedAt" = now(); 
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_epics_updated_at BEFORE UPDATE ON "Epics" FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_user_stories_updated_at BEFORE UPDATE ON "User_Stories" FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
CREATE TRIGGER update_project_tasks_updated_at BEFORE UPDATE ON "Project_Tasks" FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

\echo '--> Các trigger tự động cập nhật "UpdatedAt" đã được thiết lập.'

-- =============================================================================
\set QUIET on
\echo '>>>>>> HOÀN TẤT! Tất cả các bảng đã được tạo thành công.'
\echo '>>>>>> BƯỚC TIẾP THEO: Vào giao diện NocoDB và nhấn "Sync with DB".'
\set QUIET off
-- =============================================================================