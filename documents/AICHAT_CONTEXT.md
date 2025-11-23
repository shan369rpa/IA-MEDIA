# IA MEDIA - Project Context for GitHub Copilot

## 1. Project Overview
**IA MEDIA** is an open-source pipeline to automate the post-production of dharma talk videos.
- **Input:** Raw video, Edited video, FCPXML file (Final Cut Pro).
- **Core Task:** Align raw/edited audio, transcribe with Whisper, chunk into words/sentences, vectorise using SpeechBrain, and store in PostgreSQL (pgvector).
- **Goal:** Create a rich, multimodal dataset for error detection and future TTS training.

## 2. Tech Stack
- **Language:** Python 3.10
- **Environment:** GitHub Codespaces (Dev), Google Colab (Execution/GPU).
- **Database:** PostgreSQL 16 + `pgvector` extension (Self-hosted via Docker).
- **Key Libraries:**
  - `openai-whisper` (STT)
  - `speechbrain` & `sentence-transformers` (Embedding)
  - `pydub` & `ffmpeg-python` (Audio manipulation)
  - `psycopg2-binary` (DB Connection)
  - `lxml` or `xml.etree` (FCPXML parsing)

## 3. Database Schema (Critical)
Use this schema for all SQL queries and DB interactions. DO NOT hallucinate table names.

```sql
-- Table: sources
CREATE TABLE "sources" (
    "id" SERIAL PRIMARY KEY,
    "video_name" TEXT UNIQUE NOT NULL, -- e.g., '2010-06-15-topic'
    "path_to_raw" TEXT,
    "path_to_edited" TEXT,
    "fcpxml_path" TEXT
);

-- Table: words (Micro-chunks)
CREATE TABLE "words" (
    "id" SERIAL PRIMARY KEY,
    "source_id" INTEGER REFERENCES sources(id), -- Link back to video source
    "word_text" TEXT NOT NULL,
    "language" VARCHAR(5), -- 'vie', 'eng'
    "start_time_ms_edited" BIGINT NOT NULL,
    "end_time_ms_edited" BIGINT NOT NULL,
    "embedding_clean" VECTOR(192), -- Note: Vector dim is 192 (SpeechBrain)
    "embedding_error" VECTOR(192),
    "audio_path_clean" TEXT, -- Relative path in storage
    "audio_path_error" TEXT,
    "video_path_clean" TEXT,
    "video_path_error" TEXT
);
```

## 4. Project Structure & Modules
- `src/utils/fcpxml_parser.py`: Parses `.fcpxml` to map edited timestamps to raw timestamps.
- `src/utils/file_handler.py`: Handles `ffmpeg` calls, audio extraction
- `src/analysis/transcriber.py`: Wraps `whisper` to get word-level timestamps.
- `src/analysis/chunker.py`: Core logic. Cuts audio based on timestamps and alignment map. Creates `metadata.csv`.
- `src/ai/vectorizer.py`: Loads SpeechBrain model, creates embeddings from .wav files.
- `src/database/db_manager.py`: Handles PostgreSQL connection and insertions.
- `main.py`: Orchestrator for the analysis pipeline (Video -> Chunks).
- `vectorize.py`: Orchestrator for the ingestion pipeline (Chunks -> DB).

## 5. Coding Conventions
- **Docstrings:** All functions must have Google-style docstrings.
- **Typing:** Use Python type hints (`def func(a: str) -> int:`).
- **Error Handling:** Use `try-except` blocks and `logging.error` (do not use `print` for errors).
- **Paths:** Use `os.path.join` for cross-platform compatibility.
- **Environment:** Load secrets using `dotenv`.

## 6. File Naming Convention
- Session ID format: `YYYY-MM-DD-topic-name`
- Raw video: `{Session-ID}_raw.mp4`
- Edited video: `{Session-ID}_edited.mp4`
- FCPXML: `{Session-ID}.fcpxml`
```
