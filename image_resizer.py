"""
Image Resizer - A Python utility for resizing images efficiently.
"""

import argparse
import os
import sys
from pathlib import Path

from PIL import Image, ImageOps, UnidentifiedImageError

try:
    from pillow_heif import register_heif_opener
except ImportError:
    register_heif_opener = None


if register_heif_opener is not None:
    register_heif_opener()


SUPPORTED_INPUT_FORMATS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp",
    ".heic",
    ".heif",
    ".avif",
}

RAW_FORMATS = {
    ".3fr",
    ".arw",
    ".cr2",
    ".cr3",
    ".dng",
    ".erf",
    ".kdc",
    ".mos",
    ".mrw",
    ".nef",
    ".nrw",
    ".orf",
    ".pef",
    ".raf",
    ".raw",
    ".rw2",
    ".sr2",
    ".srf",
    ".x3f",
}


def get_output_filename(input_path, output_format='jpeg'):
    """
    Generate output filename with the specified format.
    
    Args:
        input_path (str): Path to the input image file
        output_format (str): Desired output format (jpeg or webp)
    
    Returns:
        str: Output filename with appropriate extension
    """
    source_path = Path(input_path)
    source_stem = source_path.stem
    source_ext = source_path.suffix.lower().lstrip('.')
    output_ext = 'jpg' if output_format.lower() == 'jpeg' else output_format.lower()

    # Keep source extension in directory-mode outputs to avoid name collisions.
    if source_ext:
        return f"{source_stem}__{source_ext}.{output_ext}"
    return f"{source_stem}.{output_ext}"


def is_supported_input_file(file_path):
    suffix = Path(file_path).suffix.lower()
    return suffix in SUPPORTED_INPUT_FORMATS or suffix in RAW_FORMATS


def is_raw_file(file_path):
    return Path(file_path).suffix.lower() in RAW_FORMATS


def normalize_to_rgb(image):
    image = ImageOps.exif_transpose(image)

    if image.mode == "RGB":
        return image

    if image.mode in {"RGBA", "LA"}:
        background = Image.new("RGB", image.size, (255, 255, 255))
        alpha = image.getchannel("A") if "A" in image.getbands() else None
        background.paste(image.convert("RGBA"), mask=alpha)
        return background

    if image.mode == "P":
        if "transparency" in image.info:
            rgba_image = image.convert("RGBA")
            background = Image.new("RGB", rgba_image.size, (255, 255, 255))
            background.paste(rgba_image, mask=rgba_image.getchannel("A"))
            return background
        return image.convert("RGB")

    if image.mode.startswith("I;") or image.mode in {"I", "F"}:
        return image.convert("RGB")

    if image.mode in {"1", "L", "CMYK", "YCbCr", "LAB", "HSV"}:
        return image.convert("RGB")

    return image.convert("RGB")


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
        if is_raw_file(input_path):
            print(
                f"Skipping RAW input {input_path}: RAW formats are intentionally unsupported. "
                "This can happen with phone ProRAW or camera-original uploads."
            )
            return False

        with Image.open(input_path) as image:
            normalized_image = normalize_to_rgb(image)

            if normalized_image.width > max_width:
                ratio = max_width / normalized_image.width
                new_size = (max_width, max(1, int(normalized_image.height * ratio)))
                resized_image = normalized_image.resize(new_size, Image.Resampling.LANCZOS)
            else:
                resized_image = normalized_image.copy()

            if output_format.lower() == 'webp':
                resized_image.save(output_path, 'WEBP', quality=quality, method=6)
            else:
                resized_image.save(output_path, 'JPEG', quality=quality, optimize=True)

        return True
    except UnidentifiedImageError:
        print(
            f"Unsupported or unreadable image: {input_path}. "
            "Install pillow-heif for HEIC/HEIF support if needed."
        )
        return False
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
    
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)

        if os.path.isfile(file_path) and is_supported_input_file(file_path):
            output_filename = get_output_filename(file_path, output_format)
            output_path = os.path.join(output_dir, output_filename)
            if resize_image(file_path, output_path, max_width, output_format, quality):
                print(f"Resized: {filename} -> {output_filename}")
            else:
                print(f"Failed to resize: {filename}")


def print_brief_help():
    print("Image Resizer (brief help)")
    print("Usage:")
    print("  python image_resizer.py -i <input_file_or_dir> -o <output_file_or_dir> [options]")
    print("Options:")
    print("  -w, --width <px>           Output max width (default: 1000)")
    print("  -f, --format <jpeg|webp>   Output format (default: jpeg)")
    print("  -q, --quality <1-100>      Output quality (default: 90)")
    print("  --list-supported-formats   Show accepted/ignored formats and exit")
    print("  --brief-help               Show this short help and exit")
    print("  -h, --help                 Show full help and exit")


def main():
    if '--brief-help' in sys.argv:
        print_brief_help()
        return

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
    
    parser.add_argument('-i', '--input',
                        help='Input image file or directory')
    parser.add_argument('-o', '--output',
                        help='Output image file or directory')
    parser.add_argument('-w', '--width', type=int, default=1000,
                        help='Maximum width in pixels (default: 1000)')
    parser.add_argument('-f', '--format', choices=['jpeg', 'webp'], default='jpeg',
                        help='Output format: jpeg or webp (default: jpeg)')
    parser.add_argument('-q', '--quality', type=int, default=90, choices=range(1, 101),
                        metavar='1-100',
                        help='Quality setting 1-100 (default: 90)')
    parser.add_argument('--list-supported-formats', action='store_true',
                        help='Print supported input formats and exit')
    parser.add_argument('--brief-help', action='store_true',
                        help='Show short help and exit')
    
    args = parser.parse_args()
    
    if args.list_supported_formats:
        print('Standard inputs:', ', '.join(sorted(SUPPORTED_INPUT_FORMATS)))
        print('Ignored RAW inputs:', ', '.join(sorted(RAW_FORMATS)))
        print('Output is normalized to 8-bit RGB and written as JPEG or WebP.')
        return

    if not args.input or not args.output:
        parser.error('the following arguments are required: -i/--input, -o/--output')

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
