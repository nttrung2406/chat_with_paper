import torch
from transformers import AutoModel, AutoTokenizer
from PIL import Image
from llama_cpp import Llama
import os
root = os.getcwd()

MODEL_PATH = os.path.join(root, "models", "llama-2-7b.gguf")  

class MiniLMEmbedding:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    
    def get_text_embedding(self, text):
        tokens = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        
        with torch.no_grad():
            output = self.model(**tokens)
        
        embedding = output.last_hidden_state[:, 0, :]
        return embedding.squeeze().tolist()


class LLModel:
    def __init__(self, model_path=MODEL_PATH):
        self.model = Llama(model_path=model_path, n_ctx=4096, n_threads=6)

    def extract_text(self, text_prompt, max_tokens=1000, temperature=0.7):
        """Generate a longer response from Gemma."""
        output = self.model(
            text_prompt, 
            max_tokens=max_tokens, 
            temperature=temperature,  
            top_p=0.9  
        )
        return output["choices"][0]["text"].strip()

rag_model = LLModel()
minilm_model = MiniLMEmbedding()
