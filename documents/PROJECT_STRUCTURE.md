# IA MEDIA - Project Structure
## Cấu trúc Dự án IA MEDIA

This document outlines the directory and file structure of the IA MEDIA project.
Tài liệu này mô tả cấu trúc thư mục và file của dự án IA MEDIA.

```
.
├── .devcontainer/                #> Configuration for the GitHub Codespaces development environment
│   ├── devcontainer.json         #  - Defines VS Code settings, extensions, and port forwarding
│   └── Dockerfile                #  - Defines the OS, system packages (ffmpeg, psql), and Python libraries
│
├── .github/                      # Configuration for GitHub features (e.g., CI/CD workflows)
│
├── IA_PineLine_Assistant/        #> Module for automating AI context updates
│   ├── PROJECT_CONTEXT.md        #  - The AI's "long-term memory" about the project
│   ├── README.md                 #  - Explains how the assistant module works
│   └── SYSTEM_MESSAGE.md         #  - Template used by n8n to generate the final context prompt
│
├── server_configs/               #> Custom configuration files for the production server
│   ├── custom_pg_hba.conf        #  - PostgreSQL host-based authentication rules
│   └── custom_postgresql.conf    #  - PostgreSQL server settings (e.g., listen_addresses)
│
├── src/                          #> Main source code for the AI pipeline
│   ├── __init__.py
│   ├── analysis/                 #  - Modules related to core data analysis
│   │   ├── __init__.py
│   │   ├── chunker.py            #  - Logic for slicing and saving audio chunks
│   │   └── transcriber.py        #  - Logic for running Whisper to get word timestamps
│   ├── database/                 #  - Modules for database interaction
│   │   ├── __init__.py
│   │   └── db_manager.py         #  - Functions to connect, insert, and query the PostgreSQL DB
│   └── utils/                    #  - Utility functions used across the project
│       ├── __init__.py
│       ├── fcpxml_parser.py      #  - Functions to parse FCPXML files and create time maps
│       └── file_handler.py       #  - Functions for file operations (extract audio, sanitize names)
│
├── tests/                        #> Automated tests for the project
│   ├── __init__.py
│   ├── fixtures/                 #  - Mock data files used for testing (e.g., sample XML)
│   │   └── sample_project.fcpxml
│   ├── test_db_manager.py        #  - Unit tests for database manager functions
│   └── test_fcpxml_parser.py     #  - Unit tests for FCPXML parsing logic
│
├── .env.example                  # Example environment variables file
├── .gitignore                    # Specifies intentionally untracked files to ignore
├── database_setup.sql            # SQL script to set up the vector database schema (`audio_chunks`)
├── GUIDE.md                      # Step-by-step guide for common operational tasks (SSH, DB setup)
├── main.py                       # Main entry point script for the analysis pipeline (Video -> Chunks)
├── nocodb_setup.sql              # SQL script to set up project management tables for NocoDB
├── PROJECT_STRUCTURE.md          # This file - explains the project structure
├── README.md                     # Main project overview and documentation (bilingual)
├── requirements.txt              # List of Python dependencies
└── vectorize.py                  # Main entry point script for the vectorization pipeline (Chunks -> DB)

```