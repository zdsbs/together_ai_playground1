import os
from dotenv import load_dotenv
from together import Together
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
import base64

# Load environment variables
load_dotenv()

# Model constants
DEFAULT_MODEL = "black-forest-labs/FLUX.1-dev"
ALTERNATIVE_MODEL = "black-forest-labs/FLUX.1-schnell-Free"

def ensure_images_directory():
    """Create images directory if it doesn't exist"""
    images_dir = "images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    return images_dir

def generate_image(prompt, model, steps, n, height, width, guidance):
    """
    Generate an image using Together.ai's API
    
    Args:
        prompt (str): The text prompt for image generation
        model (str): The model to use for generation
        steps (int): Number of diffusion steps
        n (int): Number of images to generate
        height (int): Height of the generated image
        width (int): Width of the generated image
        guidance (float): Guidance scale for the generation
    
    Returns:
        PIL.Image: The generated image
    """
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("TOGETHER_API_KEY not found in environment variables")

    # Initialize the Together client
    client = Together(api_key=api_key)
    
    # Generate the image
    response = client.images.generate(
        prompt=prompt,
        model=model,
        steps=steps,
        n=n,
        height=height,
        width=width,
        guidance=guidance
    )
    
    if not response or not response.data or not response.data[0].url:
        raise ValueError("No image URL received from API")
    
    # Download the image from URL
    image_response = requests.get(response.data[0].url)
    image_response.raise_for_status()
    
    # Convert to PIL Image
    image = Image.open(BytesIO(image_response.content))
    return image

def generate_image_http(prompt, model, steps, n, height, width, guidance):
    """
    Generate an image using Together.ai's HTTP API directly
    
    Args:
        prompt (str): The text prompt for image generation
        model (str): The model to use for generation
        steps (int): Number of diffusion steps
        n (int): Number of images to generate
        height (int): Height of the generated image
        width (int): Width of the generated image
        guidance (float): Guidance scale for the generation
    
    Returns:
        PIL.Image: The generated image
    """
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("TOGETHER_API_KEY not found in environment variables")

    url = "https://api.together.xyz/v1/images/generations"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "steps": steps,
        "n": n,
        "height": height,
        "width": width,
        "guidance": guidance,
        "output_format": "jpeg",
        "response_format": "base64"
    }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    # Parse the response
    response_data = response.json()
    if not response_data or "data" not in response_data or not response_data["data"]:
        raise ValueError("No image data received from API")
    
    # Get the base64 image data
    image_data = response_data["data"][0]["b64_json"]
    
    # Convert base64 to image
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))
    return image

def save_generated_image(image, method_name, timestamp):
    """Helper function to save generated images"""
    images_dir = ensure_images_directory()
    filename = f"generated_image_{method_name}_{timestamp}.png"
    filepath = os.path.join(images_dir, filename)
    image.save(filepath)
    print(f"Image generated and saved as '{filepath}'")

def main():
    # Example usage
    prompt = "A serene landscape with mountains and a lake at sunset"
    model = DEFAULT_MODEL  # Using the default model that we know works
    
    # Generation parameters
    generation_params = {
        "steps": 20,
        "n": 1,
        "height": 1024,
        "width": 1024,
        "guidance": 3.5
    }
    
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate image using SDK method
        print(f"Generating image using SDK method with model: {model}...")
        image = generate_image(
            prompt=prompt,
            model=model,
            **generation_params
        )
        save_generated_image(image, "sdk", timestamp)
        
        # Generate image using HTTP method
        print(f"\nGenerating image using HTTP method with model: {model}...")
        image_http = generate_image_http(
            prompt=prompt,
            model=model,
            **generation_params
        )
        save_generated_image(image_http, "http", timestamp)
        
        # Uncomment the following lines to test the alternative model
        # print(f"\nTesting alternative model: {ALTERNATIVE_MODEL}")
        # image_alt = generate_image_http(prompt, model=ALTERNATIVE_MODEL, **generation_params)
        # save_generated_image(image_alt, "alt", timestamp)
        
    except Exception as e:
        print(f"Error generating image: {e}")

if __name__ == "__main__":
    main() 