# Chat_with_paper
A RAG application for q&amp;a with paper

# Tech stack:

1. Core AI (LLM for RAG)

✅ LLaVA (LLaMA + Vision Adapter) – Handles text + images/tables.

✅ Quantized versions (GGUF with llama.cpp) – Makes inference lightweight and runs on consumer GPUs/CPUs.

💡 Inference Engine: Use llama.cpp for ultra-lightweight deployment.

2. PDF Processing
   
✅ PyMuPDF

✅ PaddleOCR

4. Vector Search (Hybrid Search)
   
✅ Milvus (Lite Mode)

6. Backend & Model Serving
   
✅ FastAPI – Handles async requests efficiently.

✅ llama.cpp

8. Monitoring & Logging
   
✅ Prometheus – Tracks system metrics (RAM, GPU, API requests, etc.).

✅ Grafana – Visualizes logs and performance.

# Project structure

rag_project/

│── backend/                   # Backend server (FastAPI)

│   │── models/                # LLaVA models (GGUF)

│   │── services/              # Core logic (PDF parsing, OCR, embedding)

│   │   │── pdf_processor.py   # PyMuPDF & PaddleOCR for text extraction

│   │   │── vector_store.py    # Milvus integration for storing/retrieving embeddings

│   │   │── llm_inference.py   # LLaVA inference (llama.cpp)

│   │── routes/                # API endpoints

│   │   │── pdf_routes.py      # PDF upload and processing

│   │   │── search_routes.py   # Query retrieval from Milvus

│   │── main.py                # FastAPI entry point

│   │── requirements.txt       # Python dependencies

│

│── frontend/                  # React.js frontend 

│   │── src/                   # React source files

│   │── public/                # Static files

│   │── package.json           # Frontend dependencies

│

│── milvus/                    # Vector search setup

│   │── docker-compose.yml      # Milvus standalone setup 

│   │── config.yaml             # Milvus configuration

│

│── monitoring/                # Prometheus & Grafana

│   │── prometheus.yml          # Prometheus config

│   │── grafana/                # Grafana dashboards

│

│── scripts/                   # Utility scripts

│   │── setup_milvus.py         # Initializes Milvus collections

│   │── download_model.sh       # Downloads LLaVA GGUF model

│

│── config/                    # Configurations for the project

│   │── settings.py             # App settings

│

│── README.md                  # Project documentation

│── .env                        # Environment variables (e.g., Milvus host, API keys)

