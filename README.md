# Chat_with_paper
A RAG application for q&amp;a with paper

# Tech stack:

1. Core AI (LLM for RAG)

✅ MiniLM – Handles text + query.

💡 Inference Engine: Use llama.cpp for ultra-lightweight deployment.

2. PDF Processing
   
✅ PyMuPDF

✅ PaddleOCR

4. Vector Search (Hybrid Search)
   
✅ MongoDB (Since Milvus does not support windows)

6. Backend & Model Serving
   
✅ FastAPI – Handles async requests efficiently.

✅ llama.cpp

8. Monitoring & Logging
   
✅ Prometheus – Tracks system metrics (RAM, GPU, API requests, etc.).

✅ Grafana – Visualizes logs and performance.

# Workflow

![image](https://github.com/user-attachments/assets/5f4cc49a-d4ba-4102-850f-acadd451d7f9)

# Advanced RAG technique

FOr improving RAG performance, I apply Contextual Chunk Headers by adding contextual headers to text chunks before embedding them. 

This is the CCH workflow:

![image](https://github.com/user-attachments/assets/1b256506-e7e0-4dcc-8017-16a4c7582057)

# CHatbot UI

![image](https://github.com/user-attachments/assets/e4ea2e49-ba0d-4d68-ba34-71b70508917d)




