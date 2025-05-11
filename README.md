# Together.ai Image Generation Project

This project demonstrates how to use Together.ai's API for image generation using the official Together Python library.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the project root and add your Together.ai API key:
```
TOGETHER_API_KEY=your_api_key_here
```

You can get your API key by signing up at [Together.ai](https://www.together.ai/).

## Usage

Run the image generation script:
```bash
python image_generation.py
```

The script will generate an image based on the default prompt and save it as `generated_image.png` in the current directory.

## Customization

You can modify the following parameters in the `generate_image` function:
- `prompt`: The text description of the image you want to generate
- `model`: The model to use (default is "black-forest-labs/FLUX.1-dev")
- `steps`: Number of diffusion steps (default is 10)
- `n`: Number of images to generate (default is 1)

## Requirements

- Python 3.10+
- Together.ai API key
- Required packages (see requirements.txt)
