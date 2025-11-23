# Implementation Tasks for Copilot

## Phase 1: Core Analysis Pipeline (Current Focus)

### 1. Refactoring & Orchestration
- [x] Create project structure and `src` modules.
- [x] Implement `fcpxml_parser.py` (Unit tests passed).
- [x] Implement `db_manager.py` basics (Unit tests passed).
- [ ] **Refactor `main.py`:**
    - Update to use `argparse` or function arguments to accept `source_dir` and `workspace_dir`.
    - Ensure it iterates through all valid sessions in the source folder based on the Naming Convention.
- [ ] **Refactor `vectorize.py`:**
    - Similar to `main.py`, make it a callable function accepting `chunk_dir`.

### 2. Completing Logic Modules
- [ ] **`src/utils/file_handler.py`:**
    - Implement `extract_audio_pair` using `ffmpeg-python` or `subprocess`.
- [ ] **`src/analysis/chunker.py`:**
    - Finalize `create_and_save_chunks`.
    - Logic: Loop through whisper timestamps -> Convert time (FCPXML) -> Cut Clean Audio -> Cut Error Audio -> Cut Clean Video -> Cut Error Video -> Save paths to List.
    - Dump the list to `metadata.csv` using Pandas.
- [ ] **`src/ai/vectorizer.py`:**
    - Implement `load_embedding_model` (SpeechBrain/ECAPA).
    - Implement `create_embedding` (Audio Path -> List[float]).
    - Ensure vector dimension is 192.

### 3. Integration Testing
- [ ] Create a `tests/integration_test.py` to run the full pipeline on dummy data.
- [ ] Verify that `metadata.csv` aligns with the database schema.

## Phase 1.5: Colab Notebook
- [ ] Create `notebooks/demo_pipeline.ipynb`.
- [ ] Code cells to mount Google Drive.
- [ ] Code cells to install `requirements.txt`.
- [ ] Code cells to import and run `main.py` and `vectorize.py` functions directly.
```

---

### **Cách "Prompt" để Bàn giao cho Copilot**

Khi bạn mở VS Code lên và bắt đầu làm việc với Copilot, hãy thực hiện các bước sau:

1.  **Mở file `AICHAT_CONTEXT.md`** (để nó nằm trong tab đang mở - active context).
2.  **Mở file `TODO.md`**.
3.  **Mở khung Chat Copilot (Ctrl+I hoặc Ctrl+Alt+I)** và gõ prompt khởi động: