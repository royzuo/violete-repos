#!/usr/bin/env python3
"""Convert a PDF into one JPG per page using available local rasterizers."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert a PDF into JPG pages.")
    parser.add_argument("pdf_path", help="Input PDF file")
    parser.add_argument("--output-dir", required=True, help="Directory for rendered JPG pages")
    parser.add_argument("--prefix", default="page", help="Output filename prefix")
    parser.add_argument("--dpi", type=int, default=220, help="Rasterization DPI")
    parser.add_argument("--quality", type=int, default=92, help="JPG quality 1-100")
    return parser.parse_args()


def run_command(command: list[str]) -> None:
    completed = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        stdout = completed.stdout.strip()
        detail = stderr or stdout or "unknown error"
        raise RuntimeError(detail)


def convert_with_pdftoppm(pdf_path: Path, output_dir: Path, prefix: str, dpi: int, quality: int) -> None:
    base = output_dir / prefix
    command = [
        shutil.which("pdftoppm") or "pdftoppm",
        "-jpeg",
        "-jpegopt",
        f"quality={quality}",
        "-r",
        str(dpi),
        str(pdf_path),
        str(base),
    ]
    run_command(command)


def convert_with_magick(pdf_path: Path, output_dir: Path, prefix: str, dpi: int, quality: int) -> None:
    command = [
        shutil.which("magick") or "magick",
        "-density",
        str(dpi),
        str(pdf_path),
        "-quality",
        str(quality),
        str(output_dir / f"{prefix}-%d.jpg"),
    ]
    run_command(command)


def main() -> int:
    args = parse_args()
    pdf_path = Path(args.pdf_path).resolve()
    output_dir = Path(args.output_dir).resolve()

    if not pdf_path.exists():
        raise RuntimeError(f"PDF file not found: {pdf_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    tool_errors: list[str] = []
    if shutil.which("pdftoppm"):
        try:
            convert_with_pdftoppm(pdf_path, output_dir, args.prefix, args.dpi, args.quality)
        except RuntimeError as exc:
            tool_errors.append(f"pdftoppm failed: {exc}")
        else:
            rendered = sorted(output_dir.glob(f"{args.prefix}-*.jpg"))
            if rendered:
                for path in rendered:
                    print(path)
                return 0
            tool_errors.append("pdftoppm did not create any JPG files")

    if shutil.which("magick"):
        try:
            convert_with_magick(pdf_path, output_dir, args.prefix, args.dpi, args.quality)
        except RuntimeError as exc:
            tool_errors.append(f"magick failed: {exc}")
        else:
            rendered = sorted(output_dir.glob(f"{args.prefix}-*.jpg"))
            if rendered:
                for path in rendered:
                    print(path)
                return 0
            tool_errors.append("magick did not create any JPG files")

    message = [
        "No usable PDF rasterizer succeeded.",
        "Install `poppler` for `pdftoppm` or ImageMagick for `magick`, then rerun the export.",
    ]
    if tool_errors:
        message.extend(tool_errors)
    raise RuntimeError(" ".join(message))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
