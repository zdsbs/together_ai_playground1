import os
from dotenv import load_dotenv
from together import Together
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime

# Load environment variables
load_dotenv()

def ensure_images_directory():
    """Create images directory if it doesn't exist"""
    images_dir = "images"
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    return images_dir

def generate_image(prompt, model="black-forest-labs/FLUX.1-dev", steps=10, n=1):
    """
    Generate an image using Together.ai's API
    
    Args:
        prompt (str): The text prompt for image generation
        model (str): The model to use for generation
        steps (int): Number of diffusion steps
        n (int): Number of images to generate
    
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
        n=n
    )
    
    if not response or not response.data or not response.data[0].url:
        raise ValueError("No image URL received from API")
    
    # Download the image from URL
    image_response = requests.get(response.data[0].url)
    image_response.raise_for_status()
    
    # Convert to PIL Image
    image = Image.open(BytesIO(image_response.content))
    return image

def main():
    # Example usage
    prompt = "A serene landscape with mountains and a lake at sunset"
    try:
        image = generate_image(prompt)
        
        # Ensure images directory exists
        images_dir = ensure_images_directory()
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_image_{timestamp}.png"
        filepath = os.path.join(images_dir, filename)
        
        # Save the image
        image.save(filepath)
        print(f"Image generated and saved as '{filepath}'")
    except Exception as e:
        print(f"Error generating image: {e}")

if __name__ == "__main__":
    main() 