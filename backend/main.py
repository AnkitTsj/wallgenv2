from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from diffusers import StableDiffusionPipeline, LCMScheduler
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import random
import io
import base64
from typing import Optional

print("Loading model at startup...")
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

pipe = StableDiffusionPipeline.from_pretrained(
    "SimianLuo/LCM_Dreamshaper_v7",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    safety_checker=None,
    requires_safety_checker=False,
    low_cpu_mem_usage=True,
    cache_dir = "../models"
)
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe = pipe.to(device)

if device == "cuda":
    pipe.enable_model_cpu_offload()
else:
    pipe.enable_attention_slicing()
print("Model has been loaded successfully!")

# --- Helper Functions (Refactored for API) ---
def extract_colors(image: Image.Image, num_colors=6):
    img_array = np.array(image)
    pixels = img_array.reshape(-1, 3)
    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)
    hex_colors = ['#{:02x}{:02x}{:02x}'.format(r, g, b) for r, g, b in colors]
    return hex_colors

def resize_image(image: Image.Image, width: int, height: int):
    return image.resize((width, height), Image.Resampling.LANCZOS)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationRequest(BaseModel):
    style: str = "Gradient"
    seed: int = 42
    resolution: str = "Desktop (1920x1080)"
    steps: int = 4
    color: Optional[str] = None

@app.post("/generate-wallpaper/")
async def generate_wallpaper_endpoint(request: GenerationRequest):
    prompts = {
        "Geometric": "abstract waves, ethereal, high resolution seamless geometric pattern, isometric shapes, bright vivid color blocking, ultra-sharp lines, elegant 8k wallpaper, inspired by Bauhaus, center-focused composition",
        "Organic": "flowing organic forms, silky fluid textures, soft lighting, high-detail depth, oil painting feel, zen abstract design",
        "Vibrant": "futuristic neon shapes, cyberpunk color palette, dark citylight background, glowing fractals, high contrast, vivid reflections, perfect for phone wallpaper, neon geometric shapes, cyberpunk style, dark background",
        "Minimal": "abstract triangular shapes, bright pastel colors, modern wallpaper",
    "Fractal": "complex fractal spirals, infinite zoom illusion, glowing edges, depth of field blur, mathematical precision, cosmic art, Mandelbrot-inspired structure",
    "Gradient": "smooth color gradients, organic flowing lines, watercolor style, soft gradients",
    "Crystal": "high-resolution crystal surfaces, prism reflections, iridescent colors, shattered glass texture, futuristic diamond shapes, cinematic lighting",
    "Retro Wave": "synthwave aesthetic, neon grid lines, 1980s retro futuristic, purple pink gradients",
    "Botanical": "botanical illustrations, detailed leaves and flowers, vintage naturalist style, earth tones",
    "Space Cosmic": "deep space nebula, cosmic dust clouds, distant galaxies, purple blue cosmic colors",
    "Psychedelic": "trippy psychedelic patterns, kaleidoscope effects, vibrant swirling colors, mind-bending",
    "Industrial": "metal textures, rust patterns, industrial materials, concrete and steel aesthetics"
    }

    resolutions = {
        "Mobile Portrait (1080x1920)": (1080, 1920),
        "Desktop (1920x1080)": (1920, 1080),
        "Square (1080x1080)": (1080, 1080),
        "Ultrawide (2560x1080)": (2560, 1080),
        "4K Desktop (3840x2160)": (3840, 2160),
    }
    final_prompt = prompts.get(request.style)

    if request.color and request.color.strip():
            final_prompt += f", with a color theme of {request.color.strip()}"
    try:
        # Set seed
        torch.manual_seed(request.seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(request.seed)

        # Generate base image
        with torch.no_grad():
            base_image = pipe(
                final_prompt,
                num_inference_steps=request.steps,
                guidance_scale=1.0,
                height=512,
                width=512
            ).images[0]

        # Resize image
        target_width, target_height = resolutions.get(request.resolution, (1920, 1080))
        resized_image = resize_image(base_image, target_width, target_height)

        # Extract colors
        colors = extract_colors(resized_image)

        # Convert image to Base64 string to send via JSON
        buffered = io.BytesIO()
        resized_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return JSONResponse(content={
            "image": f"data:image/png;base64,{img_str}",
            "palette": colors,
            "seed": request.seed,
            "style": request.style,
            "steps": request.steps,
            "resolution": f"{target_width}x{target_height}"
        })
    except Exception as e:
        print(f"Error during generation: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/random-seed/")
async def random_seed_endpoint():
    return {"seed": random.randint(1, 999999)}