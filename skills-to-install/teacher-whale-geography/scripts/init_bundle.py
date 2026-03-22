#!/usr/bin/env python3
"""Scaffold a Teacher Whale geography bundle with the expected working files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a Teacher Whale geography bundle.")
    parser.add_argument("--bundle-id", required=True, help="Bundle directory name under scripts/")
    parser.add_argument("--title", required=True, help="Bundle title shown inside generated templates")
    parser.add_argument(
        "--series-title",
        default="《鲸鱼老师讲地理》",
        help="Series title used in templates",
    )
    parser.add_argument(
        "--output-root",
        help="Optional repo root override; defaults to the current repository root",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    return parser.parse_args()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def render_template(template_text: str, args: argparse.Namespace) -> str:
    return (
        template_text.replace("{{BUNDLE_ID}}", args.bundle_id)
        .replace("{{BUNDLE_TITLE}}", args.title)
        .replace("{{SERIES_TITLE}}", args.series_title)
    )


def write_file(path: Path, content: str, force: bool) -> str:
    if path.exists() and not force:
        return "skipped"
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return "written"


def main() -> int:
    args = parse_args()
    repo_root = Path(args.output_root).resolve() if args.output_root else repo_root_from_script()
    skill_root = Path(__file__).resolve().parents[1]
    template_root = skill_root / "assets" / "templates"
    bundle_dir = repo_root / "scripts" / args.bundle_id
    bundle_dir.mkdir(parents=True, exist_ok=True)

    template_map = {
        "chapter-brief.md": "chapter-brief.md",
        "sources.json": "sources.json",
        "briefing-card.md": "briefing-card.md",
        "video-article.md": "video-article.md",
        "talkshow-script.md": "talkshow-script.md",
        "video-prompts.md": "video-prompts.md",
    }

    statuses: list[str] = []
    for output_name, template_name in template_map.items():
        template_path = template_root / template_name
        if not template_path.exists():
            raise RuntimeError(f"Missing template: {template_path}")
        rendered = render_template(template_path.read_text(encoding="utf-8"), args)
        status = write_file(bundle_dir / output_name, rendered, force=args.force)
        statuses.append(f"{output_name}={status}")

    print(f"bundle_dir={bundle_dir}")
    for status in statuses:
        print(status)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
