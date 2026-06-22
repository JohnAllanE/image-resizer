"""
Validation runner for image_resizer.py.

Processes every image in the validation/ folder through the CLI exactly as a
user would, saves outputs to validation/output/, and prints a per-file report.
"""

import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

VALIDATION_DIR = Path(__file__).parent / "validation"
OUTPUT_DIR = VALIDATION_DIR / "output"

SUPPORTED_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp",
    ".tif", ".tiff", ".webp", ".heic", ".heif", ".avif",
}

# Run once in JPEG and once in WebP so you can eye-test both outputs
OUTPUT_FORMATS = ["jpeg", "webp"]
DEFAULT_WIDTH = 1000


def run_resize(input_path, output_path, output_format, width=DEFAULT_WIDTH):
    """Invoke image_resizer.py via CLI exactly as a user would."""
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "image_resizer.py"),
        "-i", str(input_path),
        "-o", str(output_path),
        "--format", output_format,
        "--width", str(width),
    ]
    start = time.perf_counter()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.perf_counter() - start
    return result, elapsed


def run_directory_resize(input_dir, output_dir, output_format, width=DEFAULT_WIDTH):
    """Invoke directory mode through the CLI and return process result + elapsed."""
    cmd = [
        sys.executable,
        str(Path(__file__).parent / "image_resizer.py"),
        "-i", str(input_dir),
        "-o", str(output_dir),
        "--format", output_format,
        "--width", str(width),
    ]
    start = time.perf_counter()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.perf_counter() - start
    return result, elapsed


def main():
    if not VALIDATION_DIR.exists():
        print(f"ERROR: validation/ folder not found at {VALIDATION_DIR}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)

    input_files = sorted(
        f for f in VALIDATION_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    )

    if not input_files:
        print("No supported images found in validation/")
        sys.exit(1)

    print(f"Found {len(input_files)} input files")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Formats tested:   {', '.join(OUTPUT_FORMATS)}")
    print(f"Output width:     {DEFAULT_WIDTH}px")
    print("=" * 70)

    results = []

    for fmt in OUTPUT_FORMATS:
        fmt_dir = OUTPUT_DIR / fmt
        if fmt_dir.exists():
            shutil.rmtree(fmt_dir)
        fmt_dir.mkdir(exist_ok=True)

        print(f"\n--- Format: {fmt.upper()} ---")
        ext = "jpg" if fmt == "jpeg" else "webp"

        for input_file in input_files:
            stem = input_file.stem
            src_ext = input_file.suffix.lower().lstrip(".")
            output_file = fmt_dir / f"{stem}__{src_ext}.{ext}"

            result, elapsed = run_resize(input_file, output_file, fmt)

            if result.returncode == 0 and output_file.exists():
                size_kb = output_file.stat().st_size / 1024
                status = "PASS"
                detail = f"{size_kb:.1f} KB  ({elapsed:.2f}s)"
            else:
                status = "FAIL"
                stderr = result.stderr.strip() or result.stdout.strip()
                detail = stderr[:80] if stderr else "no output produced"

            tag = f"[{status}]"
            print(f"  {tag:<7} {input_file.name:<40}  {detail}")
            results.append((fmt, input_file.name, status, detail))

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r[2] == "PASS")
    failed = total - passed

    print("\n" + "=" * 70)
    print(f"Results: {passed}/{total} passed")

    if failed:
        print(f"\nFailed ({failed}):")
        for fmt, name, status, detail in results:
            if status == "FAIL":
                print(f"  [{fmt}] {name}: {detail}")

    # Directory mode smoke test per output format
    print("\n--- Directory Mode Smoke Test ---")
    expected_count = len(input_files)
    smoke_failures = 0

    for fmt in OUTPUT_FORMATS:
        smoke_dir = OUTPUT_DIR / f"dir_{fmt}"
        if smoke_dir.exists():
            shutil.rmtree(smoke_dir)
        smoke_dir.mkdir(exist_ok=True)

        result, elapsed = run_directory_resize(VALIDATION_DIR, smoke_dir, fmt)

        ext = ".jpg" if fmt == "jpeg" else ".webp"
        produced = sorted(
            p for p in smoke_dir.iterdir()
            if p.is_file() and p.suffix.lower() == ext
        )

        if result.returncode == 0 and len(produced) == expected_count:
            print(
                f"  [PASS] {fmt:<5} produced {len(produced)}/{expected_count} files "
                f"({elapsed:.2f}s)"
            )
        else:
            smoke_failures += 1
            print(
                f"  [FAIL] {fmt:<5} produced {len(produced)}/{expected_count} files "
                f"({elapsed:.2f}s)"
            )

    failed_total = failed + smoke_failures

    print(f"\nOutput images saved to: {OUTPUT_DIR}")
    print("Open the jpeg/ and webp/ subfolders to do your eye test.")

    sys.exit(0 if failed_total == 0 else 1)


if __name__ == "__main__":
    main()
