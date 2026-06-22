"""
Image Resizer - A Python utility for resizing images efficiently.
"""

from PIL import Image
import os
import argparse
from pathlib import Path


def get_output_filename(input_path, output_format='jpeg'):
    """
    Generate output filename with the specified format.
    
    Args:
        input_path (str): Path to the input image file
        output_format (str): Desired output format (jpeg or webp)
    
    Returns:
        str: Output filename with appropriate extension
    """
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    ext = 'jpg' if output_format.lower() == 'jpeg' else output_format.lower()
    return f"{base_name}.{ext}"


def resize_image(input_path, output_path, max_width=1000, output_format='jpeg', quality=90):
    """
    Resize an image to fit within the specified width while maintaining aspect ratio.
    
    Args:
        input_path (str): Path to the input image file
        output_path (str): Path to save the resized image
        max_width (int): Maximum width in pixels (default: 1000)
        output_format (str): Output format - 'jpeg' or 'webp' (default: 'jpeg')
        quality (int): Quality setting for output (1-100, default: 90)
    
    Returns:
        bool: True if resize was successful, False otherwise
    """
    try:
        image = Image.open(input_path)
        
        # Calculate height maintaining aspect ratio
        ratio = max_width / image.width if image.width > max_width else 1
        new_height = int(image.height * ratio)
        
        # Resize image
        resized_image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert RGBA to RGB if saving as JPEG
        if output_format.lower() == 'jpeg' and resized_image.mode in ('RGBA', 'LA', 'P'):
            rgb_image = Image.new('RGB', resized_image.size, (255, 255, 255))
            rgb_image.paste(resized_image, mask=resized_image.split()[-1] if resized_image.mode == 'RGBA' else None)
            resized_image = rgb_image
        
        # Save with appropriate format
        if output_format.lower() == 'webp':
            resized_image.save(output_path, 'WEBP', quality=quality, method=6)
        else:  # JPEG
            resized_image.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        return True
    except Exception as e:
        print(f"Error resizing image {input_path}: {e}")
        return False


def resize_directory(input_dir, output_dir, max_width=1000, output_format='jpeg', quality=90):
    """
    Resize all images in a directory.
    
    Args:
        input_dir (str): Path to directory containing images
        output_dir (str): Path to directory where resized images will be saved
        max_width (int): Maximum width in pixels (default: 1000)
        output_format (str): Output format - 'jpeg' or 'webp' (default: 'jpeg')
        quality (int): Quality setting for output (1-100, default: 90)
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        
        if os.path.isfile(file_path) and os.path.splitext(filename)[1].lower() in supported_formats:
            output_filename = get_output_filename(file_path, output_format)
            output_path = os.path.join(output_dir, output_filename)
            if resize_image(file_path, output_path, max_width, output_format, quality):
                print(f"Resized: {filename} → {output_filename}")
            else:
                print(f"Failed to resize: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description='Resize images to consistent dimensions and format.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i image.jpg -o resized.jpg
  %(prog)s -i input/ -o output/ --width 800 --format webp
  %(prog)s -i image.png -o resized.jpg --quality 85
        """
    )
    
    parser.add_argument('-i', '--input', required=True,
                        help='Input image file or directory')
    parser.add_argument('-o', '--output', required=True,
                        help='Output image file or directory')
    parser.add_argument('-w', '--width', type=int, default=1000,
                        help='Maximum width in pixels (default: 1000)')
    parser.add_argument('-f', '--format', choices=['jpeg', 'webp'], default='jpeg',
                        help='Output format: jpeg or webp (default: jpeg)')
    parser.add_argument('-q', '--quality', type=int, default=90, choices=range(1, 101),
                        metavar='1-100',
                        help='Quality setting 1-100 (default: 90)')
    
    args = parser.parse_args()
    
    input_path = args.input
    output_path = args.output
    
    # Check if input is a directory or file
    if os.path.isdir(input_path):
        print(f"Processing directory: {input_path}")
        resize_directory(input_path, output_path, args.width, args.format, args.quality)
        print(f"Batch resize complete. Output saved to: {output_path}")
    elif os.path.isfile(input_path):
        print(f"Resizing: {input_path}")
        if resize_image(input_path, output_path, args.width, args.format, args.quality):
            file_size = os.path.getsize(output_path) / 1024  # KB
            print(f"✓ Image resized successfully")
            print(f"  Output: {output_path}")
            print(f"  Size: {file_size:.1f} KB")
        else:
            print(f"✗ Failed to resize image")
    else:
        print(f"Error: Input path not found: {input_path}")


if __name__ == "__main__":
    main()
