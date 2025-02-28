# Chat_with_paper
A RAG application for q&amp;a with paper

**Tech stack:**

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
