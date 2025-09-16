from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
<<<<<<< HEAD
import uvicorn
from fastapi.staticfiles import StaticFiles
=======
>>>>>>> 1e1ffb2ebcf55de845344befc5de48bb2fbbf3e1
from diffusers import StableDiffusionPipeline, LCMScheduler
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import random
import io
import base64
from typing import Optional
<<<<<<< HEAD
import os
# port = int(os.getenv("PORT", 7860))


print("Model will load on first request...")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
device = "cpu"  # "cuda" if torch.cuda.is_available() else "cpu"
MODEL_CACHE_DIR = os.getenv("MODEL_CACHE_DIR", os.path.abspath(os.path.join(BASE_DIR, "..", "models")))
pipe = None  # lazy-loaded on first generation request

def load_pipeline():
    global pipe
    if pipe is not None:
        return pipe
    print("Loading model into memory...")
    local_device = "cuda" if torch.cuda.is_available() else device

    # Preferred local directory storing .bin weights to avoid safetensors duplication
    local_model_dir_name = "SimianLuo_LCM_Dreamshaper_v7_bin"
    local_model_dir = os.path.join(MODEL_CACHE_DIR, local_model_dir_name)
    
    # Check if we already have the converted .bin directory
    if os.path.isdir(local_model_dir) and os.path.exists(os.path.join(local_model_dir, "model_index.json")):
        print(f"Loading from local .bin directory: {local_model_dir}")
        # Load from our local converted .bin directory
        p = StableDiffusionPipeline.from_pretrained(
            local_model_dir,
            torch_dtype=torch.float32,
            safety_checker=None,
            requires_safety_checker=False,
            low_cpu_mem_usage=True,
            use_safetensors=False,
            local_files_only=True,
        )
    else:
        # Check if we have the model in huggingface cache format (safetensors)
        hf_cache_path = os.path.join(MODEL_CACHE_DIR, "models--SimianLuo--LCM_Dreamshaper_v7")
        if os.path.isdir(hf_cache_path):
            print("Found existing model in HuggingFace cache (safetensors format), converting to .bin...")
            # Load from the existing cached model
            p = StableDiffusionPipeline.from_pretrained(
                "SimianLuo/LCM_Dreamshaper_v7",
                torch_dtype=torch.float32,
                safety_checker=None,
                requires_safety_checker=False,
                low_cpu_mem_usage=True,
                cache_dir=MODEL_CACHE_DIR,
                use_safetensors=True,
                local_files_only=True,
            )
        else:
            print("Model not found locally, downloading...")
            # First-time: fetch from hub, prefer .bin. If unavailable, fallback to safetensors then convert.
            try:
                p = StableDiffusionPipeline.from_pretrained(
                    "SimianLuo/LCM_Dreamshaper_v7",
                    torch_dtype=torch.float32,
                    safety_checker=None,
                    requires_safety_checker=False,
                    low_cpu_mem_usage=True,
                    cache_dir=MODEL_CACHE_DIR,
                    use_safetensors=False,
                )
            except Exception as e:
                print(f".bin weights not available: {e}")
                print("Downloading with safetensors format for one-time conversion...")
                p = StableDiffusionPipeline.from_pretrained(
                    "SimianLuo/LCM_Dreamshaper_v7",
                    torch_dtype=torch.float32,
                    safety_checker=None,
                    requires_safety_checker=False,
                    low_cpu_mem_usage=True,
                    cache_dir=MODEL_CACHE_DIR,
                    use_safetensors=True,
                )
        
        # Convert and save in .bin format to a dedicated local directory
        print(f"Converting model to .bin format and saving to: {local_model_dir}")
        os.makedirs(local_model_dir, exist_ok=True)
        try:
            p.save_pretrained(local_model_dir, safe_serialization=False)
            print(f"Successfully saved model in .bin format to {local_model_dir}")
            
            # Reload strictly from .bin-only directory to ensure we use it going forward
            print("Reloading from .bin directory to verify...")
            p = StableDiffusionPipeline.from_pretrained(
                local_model_dir,
                torch_dtype=torch.float32,
                safety_checker=None,
                requires_safety_checker=False,
                low_cpu_mem_usage=True,
                use_safetensors=False,
                local_files_only=True,
            )
            print("Successfully reloaded from .bin directory")
        except Exception as save_err:
            print(f"Error during .bin conversion: {save_err}")
            print("Continuing with original model...")

    p.scheduler = LCMScheduler.from_config(p.scheduler.config)
    p = p.to(local_device)
    if local_device == "cuda":
        p.enable_model_cpu_offload()
    else:
        p.enable_attention_slicing()
    pipe = p
    print("Model has been loaded successfully!")
    return pipe

=======

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
>>>>>>> 1e1ffb2ebcf55de845344befc5de48bb2fbbf3e1
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
<<<<<<< HEAD
# app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")
=======
>>>>>>> 1e1ffb2ebcf55de845344befc5de48bb2fbbf3e1

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
<<<<<<< HEAD
        "Geometric": "sharp geometric patterns, triangular tessellations, hexagonal grids, precise angular shapes, colorful polygon arrangements, geometric mandala designs, crystalline symmetric patterns, abstract mathematical forms, vector art precision, clean geometric compositions, bright geometric color blocks, structured pattern design, 8k wallpaper",
        
        "Organic": "flowing organic forms, silky fluid textures, soft ethereal lighting, high-detail depth, oil painting feel, zen abstract design, bioluminescent flowing lines, translucent silk ribbons, watercolor blending, natural formations",
        
        "Vibrant": "futuristic neon shapes, cyberpunk color palette, dark background, glowing fractals, high contrast, vivid reflections, neon geometric patterns, electric plasma effects, holographic surfaces, laser light trails, ultra bright colors",
        
        "Minimal": "watercolor drops on white canvas, circular water color spots, bright colored water drops spreading on paper, wet watercolor bleeding circles, vibrant color drops with soft edges, colorful water stains on clean background, translucent watercolor circles, artistic water drops pattern, high contrast bright drops, clean minimalist watercolor design",
        
        "Ink Flow": "flowing liquid ink patterns, organic ink bleeds, watercolor paint flows, dynamic brush strokes, fluid color transitions, ink spreading on wet paper, abstract paint movements, colorful ink drops merging, artistic liquid patterns, paint flow dynamics",
        
        "Gradient": "smooth color gradients, organic flowing waves, ethereal abstract patterns, bright vivid color transitions, watercolor style blending, soft gradient meshes, flowing energy patterns, color field painting, seamless color flows, high resolution gradients",
        
        "Crystal": "high-resolution crystal surfaces, prism reflections, iridescent colors, shattered glass texture, futuristic diamond shapes, cinematic lighting, dichroic glass effects, crystalline structures, refracting light patterns",
        
        "Retro Wave": "synthwave aesthetic, neon grid lines, 1980s retro futuristic, purple pink gradients, chrome reflections, vintage synthesizer vibes, outrun highway aesthetic, neon palm trees, retrowave sunset",
        
        "Botanical": "botanical illustrations, detailed leaves and flowers, vintage naturalist style, earth tones, Art Nouveau vine patterns, organic plant geometry, natural forms, herbarium specimens, botanical cross-sections",
        
        "Space Cosmic": "deep space nebula, cosmic dust clouds, distant galaxies, purple blue cosmic colors, stellar formations, aurora borealis patterns, cosmic energy flows, nebula formations, space photography aesthetic",
        
        "Psychedelic": "trippy psychedelic patterns, kaleidoscope effects, vibrant swirling colors, mind-bending fractals, mandala patterns, liquid light shows, synesthetic color flows, geometric portals, infinite pattern recursion",
        
        "Industrial": "metal textures, rust patterns, industrial materials, concrete and steel aesthetics, weathered surfaces, industrial photography, high contrast lighting, urban decay patterns, metallic reflections"
=======
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
>>>>>>> 1e1ffb2ebcf55de845344befc5de48bb2fbbf3e1
    }

    resolutions = {
        "Mobile Portrait (1080x1920)": (1080, 1920),
        "Desktop (1920x1080)": (1920, 1080),
        "Square (1080x1080)": (1080, 1080),
        "Ultrawide (2560x1080)": (2560, 1080),
        "4K Desktop (3840x2160)": (3840, 2160),
    }
<<<<<<< HEAD
    base_prompt = prompts.get(request.style, prompts["Gradient"])
    
    # Add quality enhancers and style variations
    quality_modifiers = [
        "masterpiece", "best quality", "ultra-detailed", "8k resolution", 
        "professional", "award-winning", "trending on artstation", "highly detailed"
    ]
    
    # Randomly select 2-3 quality modifiers to add variety
    selected_modifiers = random.sample(quality_modifiers, k=random.randint(2, 3))
    
    # Build the final prompt with variations
    final_prompt = f"{base_prompt}, {', '.join(selected_modifiers)}"
    
    # Add artistic style variations occasionally
    if random.random() > 0.7:
        artistic_styles = [
            "oil painting style", "digital art", "photorealistic", "concept art",
            "matte painting", "volumetric lighting", "ray tracing", "octane render"
        ]
        final_prompt += f", {random.choice(artistic_styles)}"
    
    # Add composition variations
    if random.random() > 0.6:
        compositions = [
            "rule of thirds", "golden ratio composition", "symmetrical balance",
            "dynamic composition", "centered composition", "diagonal flow"
        ]
        final_prompt += f", {random.choice(compositions)}"
    
    if request.color and request.color.strip():
        # Enhanced color integration
        color_integration = random.choice([
            f"dominated by {request.color.strip()} tones",
            f"featuring prominent {request.color.strip()} accents",
            f"with {request.color.strip()} color palette",
            f"infused with {request.color.strip()} hues",
            f"{request.color.strip()} color harmony"
        ])
        final_prompt += f", {color_integration}"
    
    # Add negative prompt to avoid common issues and maintain abstract focus
    negative_prompt = "low quality, blurry, pixelated, watermark, text, logo, signature, artifacts, distorted, people, person, human, face, car, vehicle, building, realistic objects, photography, portrait, landscape"
=======
    final_prompt = prompts.get(request.style)

    if request.color and request.color.strip():
            final_prompt += f", with a color theme of {request.color.strip()}"
>>>>>>> 1e1ffb2ebcf55de845344befc5de48bb2fbbf3e1
    try:
        # Set seed
        torch.manual_seed(request.seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(request.seed)

        # Generate base image
<<<<<<< HEAD
        # Ensure pipeline is loaded lazily
        p = load_pipeline()
        with torch.no_grad():
            base_image = p(
                final_prompt,
                num_inference_steps=request.steps,
                guidance_scale=1.0,
                negative_prompt=negative_prompt,
=======
        with torch.no_grad():
            base_image = pipe(
                final_prompt,
                num_inference_steps=request.steps,
                guidance_scale=1.0,
>>>>>>> 1e1ffb2ebcf55de845344befc5de48bb2fbbf3e1
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
<<<<<<< HEAD
    return {"seed": random.randint(1, 999999)}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "AI Wallpaper Generator API is running"}

if __name__ == "__main__":
    print("Starting AI Wallpaper Generator API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)

=======
    return {"seed": random.randint(1, 999999)}
>>>>>>> 1e1ffb2ebcf55de845344befc5de48bb2fbbf3e1
