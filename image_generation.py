from PIL import Image, ImageDraw, ImageFont
import io
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='C:\\Users\\VAISHNAVI\\Desktop\\vaishnavi\\project\\data.env')

DREAMSTUDIO = os.getenv('DREAMSTUDIO_API')

def generate_image(text):
    # Placeholder image generation
    img = Image.new('RGB', (800, 600), color='white')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", size=36)
    draw.text((10, 10), text, fill='black', font=font)
    
    # Display the generated image
    img.show()
