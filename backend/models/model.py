import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
from llama_cpp import Llama
import os
root = os.getcwd()

MODEL_PATH = os.path.join(root, "models", "gemma-2b.gguf")  

class CLIPEmbedding:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    
    def get_text_embedding(self, text):
        max_length = 77 
        tokens = self.processor.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
        
        with torch.no_grad():
            embedding = self.model.get_text_features(**tokens)
        
        return embedding.squeeze().tolist()
    
    def get_image_embedding(self, image):
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            embedding = self.model.get_image_features(**inputs)
        return embedding.squeeze().tolist()


class GemmaModel:
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

rag_model = GemmaModel()
clip_model = CLIPEmbedding()
