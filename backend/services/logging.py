from fastapi import Request
import time
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    'http_request_count_total',
    'Total count of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_LATENCY = Histogram(
    'http_request_latency_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

PDF_PROCESSING_TIME = Histogram(
    'pdf_processing_time_seconds',
    'Time taken to process PDF files',
    ['status']
)

EMBEDDING_GENERATION_TIME = Histogram(
    'embedding_generation_time_seconds',
    'Time taken to generate embeddings',
    ['type']
)

LLM_RESPONSE_TIME = Histogram(
    'llm_response_time_seconds',
    'Time taken for LLM to generate response'
)

async def logging_middleware(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code
    ).inc()
    
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response