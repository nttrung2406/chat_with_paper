import torch
from PIL import Image
from llama_cpp import Llama

MODEL_PATH = "models/llava.gguf"

class LLaVAModel:
    def __init__(self, model_path=MODEL_PATH):
        self.model = Llama(model_path=model_path, n_ctx=4096)  # Adjust context size

    def extract_text(self, text_prompt):
        """Generate response from LLaVA given a text prompt."""
        output = self.model(text_prompt)
        return output["choices"][0]["text"].strip()

    def extract_image(self, image_path):
        """Extract and process image data with LLaVA."""
        img = Image.open(image_path).convert("RGB")
        
        # Convert image to tensor format
        img_tensor = torch.tensor(list(img.getdata()), dtype=torch.float32).view(1, *img.size, -1)

        # Generate response using LLaVA
        prompt = "Describe this image in detail."
        output = self.model(prompt, images=[img_tensor])

        return output["choices"][0]["text"].strip()

llava = LLaVAModel()
