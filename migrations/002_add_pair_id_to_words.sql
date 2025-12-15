-- Thêm cột pair_id để dễ dàng ghép cặp clean/error
ALTER TABLE "words" ADD COLUMN "pair_id" TEXT;
CREATE INDEX ON "words" ("pair_id");