# Image Resizer

A Python utility for efficiently resizing images while maintaining aspect ratio.

## Features

- Resize individual images with configurable dimensions
- Batch resize all images in a directory
- Maintains aspect ratio automatically
- Supports multiple image formats (JPG, PNG, GIF, BMP, WebP)
- Optimized output for web use

## Installation

### Requirements

- Python 3.7+
- Pillow (PIL)

### Setup

```bash
pip install pillow
```

## Usage

### Resize a Single Image

```python
from image_resizer import resize_image

resize_image('input.jpg', 'output.jpg', max_width=800, max_height=600)
```

### Resize a Directory

```python
from image_resizer import resize_directory

resize_directory('input_folder/', 'output_folder/', max_width=800, max_height=600)
```

## Parameters

- `input_path/input_dir`: Path to the image or directory
- `output_path/output_dir`: Path to save the resized image(s)
- `max_width`: Maximum width in pixels (default: 800)
- `max_height`: Maximum height in pixels (default: 600)

## License

MIT
