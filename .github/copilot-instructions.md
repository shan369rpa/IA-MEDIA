<!--
  .github/copilot-instructions.md
  Purpose: concise, repo-specific guidance for AI coding assistants working on IA-MEDIA.
  Keep this file short (20-50 lines) and focused on immediately-actionable facts discovered in the codebase.
-->

# IA-MEDIA — Copilot / AI agent instructions

Summary
- Phonetic-first audio QA pipeline. Two operational modes:
  - Demo (fast): silence-based semantic chunking → embeddings → To-Do markers (FCPXML).
  - Phonetic (accurate): Whisper word-level timestamps → micro-pair extraction (edited vs raw) → phonetic DB queries → anomaly labels.

Fast entry points (what to edit or call)
- Extract audio (ffmpeg):
  ```bash
  ffmpeg -y -hide_banner -loglevel error -i input.mp4 -ac 1 -ar 16000 -vn -af "aresample=16000" output.wav
  ```
- DB schema: `vector_db_setup.sql` (root). Use env vars: `DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD`.
- Useful code to inspect:
  - `src/analysis/transcriber.py` — Whisper + word timestamps and resampling behavior.
  - `src/analysis/chunker.py` — demo vs phonetic chunking and time-map logic.
  - `src/ai/vectorizer.py` — model selection, resampling, L2 normalization, `vector_dim` handling.
  - `src/database/db_manager.py` — connection helpers, upsert patterns, and failure handling.

Project-specific rules and conventions
- Phonetic-first: prioritize accurate per-word micro-pairs when implementing detection features. The demo path is acceptable for quick QA and integration tests.
- File naming: `{session_id}_raw.mp4`, `{session_id}_edited.mp4` → `{session_id}_raw.wav`, `{session_id}_edited.wav`; FCPXML → `{session_id}_ai_markers.fcpxml`.
- Storage: store audio on SSD and save only paths in DB. Chunks live under `workspace/chunks/{session_id}/{clean|error}/` per conventions in `tools/agents`.
- Dual-vector tables: `clean` and `error` logical collections — always validate `vector_dim` before inserting; split batches if dims mix.

Agent & automation contract highlights
- Prompts & specs live in `tools/prompts/` and `.github/prompts/` (system + role files). Use `system.prompt.md` + `role_*.prompt.md` to seed agent runs.
- Agents are documented in `.github/agents/` (audio_extractor, chunker, vectorizer, db_ingestor, fcpxml_generator, editor_assistant). Follow their I/O contracts exactly when writing scripts.
- Scripts should be idempotent, write diagnostic JSON to `failed_batches/` on error, and log metadata (model names, `vector_dim`, sample rates).

Implementable script checklist (priority order)
1. `scripts/extract_audio_pair.py` — ffmpeg + ffprobe wrapper, idempotent, returns JSON `{raw_wav, edited_wav}`.
2. `scripts/transcribe_whisper.py` — Whisper wrapper exposing `word_timestamps`; resample fallback; GPU warning.
3. `scripts/create_chunks.py` — demo & phonetic modes; produce `metadata.csv` with fields used by DB ingestor.
4. `scripts/run_vectorizer.py` + `scripts/ingest_db.py` — batch embedding creation and `ON CONFLICT` upsert into Postgres+pgvector.
5. `scripts/make_fcpxml.py` — convert anomalies to To-Do markers with `value` and `note` containing evidence.

Safety & developer workflow rules (must follow)
- Never suggest destructive DB operations (DROP/TRUNCATE) without explicit human approval. Propose migrations instead.
- Small PRs only: one behavioral change per PR with a short README and example usage.
- Add GPU/CPU notes whenever touching ML code. Use CPU fallback paths in scripts and warn in outputs.

Testing & quick runtimes
- Unit tests: `pytest -q tests/`.
- Quick dry-run:
  ```bash
  python -c "from main import main_pipeline; main_pipeline('./data/Batch_01','./workspace')"
  ```

Files to reference when authoring changes
- `vector_db_setup.sql`, `src/database/db_manager.py`, `src/analysis/transcriber.py`, `src/analysis/chunker.py`, `src/ai/vectorizer.py`, `tools/` and `.github/prompts/`, `.github/agents/`.

If you want, I can now (pick one):
- (A) expand this file with exact DB table/column names (I will inspect `vector_db_setup.sql` and `src/database/db_manager.py`);
- (B) implement `scripts/extract_audio_pair.py` (create file + tests + README);
- (C) prepare a PR that adds the scripts and docs above.
