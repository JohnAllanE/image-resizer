# Image Resizer

A Python utility for efficiently resizing images to consistent dimensions and formats while maintaining aspect ratio.

## Features

- Resize individual images or entire directories
- Maintains aspect ratio automatically
- Supports multiple input formats (JPG, PNG, GIF, BMP, WebP)
- Output to JPEG (default) or WebP format
- Configurable width (default 1000px) and quality settings
- Optimized output for web and database use
- CLI interface with flexible options

## Installation

### Requirements

- Python 3.7+
- Pillow (PIL)

### Setup

```bash
pip install pillow
```

## Usage

### Command Line Interface

Basic usage:
```bash
python image_resizer.py -i input.jpg -o resized.jpg
```

Resize to 800px width in WebP format:
```bash
python image_resizer.py -i input.jpg -o resized.webp --width 800 --format webp
```

Batch resize a directory:
```bash
python image_resizer.py -i input_folder/ -o output_folder/ --width 1200 --format webp
```

Adjust quality:
```bash
python image_resizer.py -i input.jpg -o resized.jpg --quality 85
```

### CLI Arguments

- `-i, --input` (required): Input image file or directory
- `-o, --output` (required): Output image file or directory
- `-w, --width` (optional): Maximum width in pixels (default: 1000)
- `-f, --format` (optional): Output format - `jpeg` or `webp` (default: `jpeg`)
- `-q, --quality` (optional): Quality 1-100 (default: 90)

### Python API

```python
from image_resizer import resize_image, resize_directory

# Resize single image
resize_image('input.jpg', 'output.jpg', max_width=1000, output_format='jpeg', quality=90)

# Batch resize directory
resize_directory('input_folder/', 'output_folder/', max_width=1000, output_format='webp', quality=90)
```

## Format Recommendations

- **JPEG**: Best for photos, maximum compatibility, good compression
- **WebP**: Better compression than JPEG (30-40% smaller), modern format with excellent browser support

## License

MIT

