"""
Image Resizer - A Python utility for resizing images efficiently.
"""

from PIL import Image
import os
from pathlib import Path


def resize_image(input_path, output_path, max_width=800, max_height=600):
    """
    Resize an image to fit within the specified dimensions while maintaining aspect ratio.
    
    Args:
        input_path (str): Path to the input image file
        output_path (str): Path to save the resized image
        max_width (int): Maximum width in pixels
        max_height (int): Maximum height in pixels
    
    Returns:
        bool: True if resize was successful, False otherwise
    """
    try:
        image = Image.open(input_path)
        image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        image.save(output_path, quality=95, optimize=True)
        return True
    except Exception as e:
        print(f"Error resizing image: {e}")
        return False


def resize_directory(input_dir, output_dir, max_width=800, max_height=600):
    """
    Resize all images in a directory.
    
    Args:
        input_dir (str): Path to directory containing images
        output_dir (str): Path to directory where resized images will be saved
        max_width (int): Maximum width in pixels
        max_height (int): Maximum height in pixels
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        
        if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in supported_formats:
            output_path = os.path.join(output_dir, filename)
            if resize_image(file_path, output_path, max_width, max_height):
                print(f"Resized: {filename}")
            else:
                print(f"Failed to resize: {filename}")


if __name__ == "__main__":
    print("Image Resizer utility loaded successfully!")
