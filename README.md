# Image Resizer

A Python utility for resizing images to consistent dimensions and formats while maintaining aspect ratio.

## Features

- Resize individual images or directories
- Maintains aspect ratio automatically
- Accepts a defined set of input extensions for batch processing
- Output to JPEG (default) or WebP format
- Configurable width (default 1000px) and quality settings
- Normalizes output to 8-bit RGB
- CLI interface

## Installation

### Requirements

- Python 3.12
- Pillow
- pillow-heif

### Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
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

Directory output naming note:

- Generated filenames include the source extension to avoid collisions.
- Example: `photo.jpg` -> `photo__jpg.jpg`, `photo.png` -> `photo__png.jpg`

Adjust quality:

```bash
python image_resizer.py -i input.jpg -o resized.jpg --quality 85
```

List supported and ignored formats:

```bash
python image_resizer.py --list-supported-formats
```

Show a short help summary:

```bash
python image_resizer.py --brief-help
```

### CLI Arguments

- `-i, --input` (required): Input image file or directory
- `-o, --output` (required): Output image file or directory
- `-w, --width` (optional): Maximum width in pixels (default: 1000)
- `-f, --format` (optional): Output format - `jpeg` or `webp` (default: `jpeg`)
- `-q, --quality` (optional): Quality 1-100 (default: 90)
- `--list-supported-formats`: Print supported standard formats, ignored RAW formats, and exit
- `--brief-help`: Print a concise help summary and exit

## Format Reference

### Allowed Input Formats

The script accepts these input file extensions:

- `.jpg`
- `.jpeg`
- `.png`
- `.gif`
- `.bmp`
- `.tif`
- `.tiff`
- `.webp`
- `.heic`
- `.heif`
- `.avif`

Notes:

- `.heic`, `.heif`, and `.avif` depend on the installed Pillow/`pillow-heif` codecs.
- Directory mode filters by extension using this exact allowlist.
- Single-file mode attempts to open the provided file directly and will fail cleanly if Pillow cannot decode it.

### Ignored RAW Formats

These RAW and camera-original formats are detected and skipped intentionally:

- `.3fr`
- `.arw`
- `.cr2`
- `.cr3`
- `.dng`
- `.erf`
- `.kdc`
- `.mos`
- `.mrw`
- `.nef`
- `.nrw`
- `.orf`
- `.pef`
- `.raf`
- `.raw`
- `.rw2`
- `.sr2`
- `.srf`
- `.x3f`

Phone-upload note:

- A user can upload RAW from a phone without realizing it if Apple ProRAW or an Android RAW capture mode was enabled, but this is not the default behavior for standard phone photos.

### Allowed Output Formats

The CLI and Python API support these output formats:

- `jpeg`: writes a `.jpg` file
- `webp`: writes a `.webp` file

### Output Color and Bit Depth

All successful outputs are normalized before save:

- 8-bit RGB output
- EXIF orientation applied before resizing
- Alpha/transparency flattened onto a white background
- Non-RGB and higher-bit input modes converted to RGB before output

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

## Validation Tests Performed

Validation assets are kept in `validation/` and are exercised through the CLI, not direct function calls.

### Single-file CLI tests

- Script used: `run_validation.py`
- Method: iterates each file in `validation/` and invokes `image_resizer.py` as a subprocess per file
- Output modes tested: `jpeg` and `webp`
- Purpose: verify decode + normalize + resize + encode path for each sample file

### Directory-mode CLI smoke tests

- Script used: `run_validation.py`
- Method: invokes `image_resizer.py -i validation -o validation/output/dir_<format>`
- Output modes tested: `jpeg` and `webp`
- Pass criteria: process exits successfully and output file count matches expected input count
- Collision behavior verified: files with same stem but different source extensions are preserved uniquely

### How to run validation

```bash
source .venv/bin/activate
python run_validation.py
```

The script writes outputs to `validation/output/` for visual inspection.

## License

MIT

