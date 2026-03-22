#!/usr/bin/env python3
"""Validate a Teacher Whale geography bundle."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

RECOMMENDED_CARD_MIN = 5
RECOMMENDED_CARD_MAX = 8
HARD_CARD_MIN = 3
HARD_CARD_MAX = 10


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a Teacher Whale geography bundle.")
    parser.add_argument("--bundle-id", help="Bundle directory name under scripts/")
    parser.add_argument("--bundle-dir", help="Absolute or relative path to the bundle directory")
    parser.add_argument("--output-root", help="Optional repo root override")
    parser.add_argument("--require-exports", action="store_true", help="Require Gamma PDF and JPG exports")
    parser.add_argument("--strict-support", action="store_true", help="Treat missing support artifacts as errors")
    return parser.parse_args()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[3]


def resolve_bundle_dir(args: argparse.Namespace) -> Path:
    if args.bundle_dir:
        return Path(args.bundle_dir).resolve()
    if not args.bundle_id:
        raise RuntimeError("Either --bundle-id or --bundle-dir must be provided")
    repo_root = Path(args.output_root).resolve() if args.output_root else repo_root_from_script()
    return (repo_root / "scripts" / args.bundle_id).resolve()


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def add_issue(container: list[str], message: str) -> None:
    if message not in container:
        container.append(message)


def extract_heading_blocks(text: str, pattern: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(pattern, text, flags=re.MULTILINE))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(0), text[match.end() : end]))
    return blocks


def validate_chapter_brief(path: Path, errors: list[str], warnings: list[str], checks: dict[str, Any], strict: bool) -> None:
    if not path.exists():
        add_issue(errors if strict else warnings, "Missing chapter-brief.md")
        return

    text = load_text(path)
    headings = [
        "## 输入章节 / 选题",
        "## 节目框架映射",
        "## 核心问题",
        "## 核心结论",
        "## 证据链",
        "## 现状、挑战与未解之谜",
        "## 卡片规划",
        "## 输出计划",
    ]
    missing = [heading for heading in headings if heading not in text]
    checks["chapter_brief_headings_present"] = len(headings) - len(missing)
    if missing:
        add_issue(errors if strict else warnings, f"chapter-brief.md missing headings: {', '.join(missing)}")


def validate_sources(path: Path, errors: list[str], warnings: list[str], checks: dict[str, Any], strict: bool) -> None:
    if not path.exists():
        add_issue(errors if strict else warnings, "Missing sources.json")
        return

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_issue(errors, f"sources.json is not valid JSON: {exc}")
        return

    if isinstance(payload, dict):
        sources = payload.get("sources")
    else:
        sources = None
    if not isinstance(sources, list):
        add_issue(errors if strict else warnings, "sources.json should contain a top-level 'sources' list")
        return

    checks["source_count"] = len(sources)
    if not sources:
        add_issue(errors if strict else warnings, "sources.json contains no sources yet")
        return

    required_fields = ("title", "url", "claim_supported")
    for index, item in enumerate(sources, start=1):
        if not isinstance(item, dict):
            add_issue(errors if strict else warnings, f"sources.json source #{index} is not an object")
            continue
        missing = [field for field in required_fields if not item.get(field)]
        if missing:
            add_issue(errors if strict else warnings, f"sources.json source #{index} missing fields: {', '.join(missing)}")


def validate_briefing_card(path: Path, errors: list[str], warnings: list[str], checks: dict[str, Any]) -> int | None:
    if not path.exists():
        add_issue(errors, "Missing briefing-card.md")
        return None

    text = load_text(path)
    card_blocks = extract_heading_blocks(text, r"^# 卡片[^\n]+$")
    card_headings = [heading for heading, _ in card_blocks]
    bullet_count = len(re.findall(r"(?m)^- ", text))
    separators = len(re.findall(r"(?m)^---\s*$", text))
    bullets_per_card = [len(re.findall(r"(?m)^- ", body)) for _, body in card_blocks]
    checks["briefing_card_count"] = len(card_headings)
    checks["briefing_card_bullet_count"] = bullet_count
    checks["briefing_card_separator_count"] = separators
    checks["briefing_card_bullets_per_card"] = bullets_per_card
    if len(card_headings) < HARD_CARD_MIN:
        add_issue(errors, f"briefing-card.md should contain at least {HARD_CARD_MIN} content cards, found {len(card_headings)}")
    elif len(card_headings) > HARD_CARD_MAX:
        add_issue(errors, f"briefing-card.md should contain no more than {HARD_CARD_MAX} content cards, found {len(card_headings)}")
    elif not (RECOMMENDED_CARD_MIN <= len(card_headings) <= RECOMMENDED_CARD_MAX):
        add_issue(warnings, f"briefing-card.md has {len(card_headings)} content cards; most geography bundles work best with {RECOMMENDED_CARD_MIN} to {RECOMMENDED_CARD_MAX}")
    if separators < len(card_headings):
        add_issue(errors, "briefing-card.md should contain at least one standalone '---' separator per content card so Gamma can split the cards correctly")
    if bullet_count < max(12, len(card_headings) * 3):
        add_issue(warnings, f"briefing-card.md looks sparse: found {bullet_count} bullets across {len(card_headings)} cards")
    if "副标题：" not in text:
        add_issue(warnings, "briefing-card.md is missing the subtitle line")
    if any(count < 3 for count in bullets_per_card):
        add_issue(warnings, "one or more briefing cards contain fewer than 3 bullets")
    if any(count > 5 for count in bullets_per_card):
        add_issue(warnings, "one or more briefing cards contain more than 5 bullets and may be overloaded")
    return len(card_headings)


def validate_talkshow(path: Path, errors: list[str], warnings: list[str], checks: dict[str, Any], expected_sections: int | None) -> int | None:
    if not path.exists():
        add_issue(errors, "Missing talkshow-script.md")
        return None

    text = load_text(path)
    section_count = len(re.findall(r"^## 卡片[^\n]+$", text, flags=re.MULTILINE))
    char_count = len(text.strip())
    checks["talkshow_card_count"] = section_count
    checks["talkshow_char_count"] = char_count
    if expected_sections is not None and section_count != expected_sections:
        add_issue(errors, f"talkshow-script.md should align with briefing-card.md card count ({expected_sections}), found {section_count}")
    elif section_count < HARD_CARD_MIN:
        add_issue(errors, f"talkshow-script.md should contain at least {HARD_CARD_MIN} card sections, found {section_count}")
    if "大家好，我是鲸鱼老师！" not in text:
        add_issue(errors, "talkshow-script.md must include the opening line '大家好，我是鲸鱼老师！'")
    minimum_chars = max(1000, 180 * max(section_count, expected_sections or 0, 1))
    if char_count < minimum_chars:
        add_issue(warnings, "talkshow-script.md looks unusually short for a full geography episode script")
    if "评论区" not in text and "下期" not in text and "咱们下期见" not in text:
        add_issue(warnings, "talkshow-script.md is missing a clear closing CTA or next-episode bridge")
    if "【" in text:
        add_issue(warnings, "talkshow-script.md still contains placeholder brackets")
    return section_count


def validate_article(path: Path, errors: list[str], warnings: list[str], checks: dict[str, Any], expected_sections: int | None) -> int | None:
    if not path.exists():
        add_issue(errors, "Missing video-article.md")
        return None

    text = load_text(path)
    h2_headings = re.findall(r"^## .+$", text, flags=re.MULTILINE)
    content_h2_headings = [heading for heading in h2_headings if heading.strip() != "## 一眼读懂"]
    h2_count = len(h2_headings)
    content_h2_count = len(content_h2_headings)
    char_count = len(text.strip())
    has_table = "|" in text and re.search(r"(?m)^\|.+\|\s*$", text) is not None
    has_mermaid = "```mermaid" in text
    has_image = re.search(r"!\[[^\]]*\]\([^)]+\)", text) is not None
    has_code = re.search(r"```(?!mermaid)[a-zA-Z0-9_-]*\n", text) is not None
    has_formula = "$" in text or "∝" in text or "≠" in text or "≈" in text
    checks["video_article_h2_count"] = h2_count
    checks["video_article_content_h2_count"] = content_h2_count
    checks["video_article_char_count"] = char_count
    checks["video_article_has_table"] = has_table
    checks["video_article_has_mermaid"] = has_mermaid
    checks["video_article_has_image"] = has_image
    checks["video_article_has_code"] = has_code
    checks["video_article_has_formula"] = has_formula
    if not text.startswith("# "):
        add_issue(errors, "video-article.md should start with an H1 title")
    if expected_sections is not None and content_h2_count != expected_sections:
        add_issue(errors, f"video-article.md should align with briefing-card.md card count ({expected_sections}), found {content_h2_count} content sections")
    elif content_h2_count < HARD_CARD_MIN:
        add_issue(warnings, f"video-article.md contains only {content_h2_count} content H2 sections")
    if "大家好，我是鲸鱼老师！" not in text:
        add_issue(warnings, "video-article.md is missing the standard Teacher Whale greeting")
    minimum_chars = max(1800, 260 * max(content_h2_count, expected_sections or 0, 1))
    if char_count < minimum_chars:
        add_issue(warnings, "video-article.md looks unusually short for a standalone reading text")
    if "来源" not in text and "版权" not in text:
        add_issue(warnings, "video-article.md is missing a closing source or copyright note")
    if "【" in text:
        add_issue(warnings, "video-article.md still contains placeholder brackets")
    if sum([has_table, has_mermaid, has_image, has_code, has_formula]) < 2:
        add_issue(warnings, "video-article.md should usually include richer knowledge structures such as tables, mermaid diagrams, images, code blocks, or formulas")
    return content_h2_count


def validate_video_prompts(path: Path, errors: list[str], warnings: list[str], checks: dict[str, Any], expected_sections: int | None) -> int | None:
    if not path.exists():
        add_issue(errors, "Missing video-prompts.md")
        return None

    text = load_text(path)
    prompt_sections = len(re.findall(r"^## ", text, flags=re.MULTILINE))
    prompt_bodies = len(re.findall(r"^\*\*Prompt\*\*:", text, flags=re.MULTILINE))
    duration_bodies = len(re.findall(r"^\*\*Duration\*\*:", text, flags=re.MULTILINE))
    prompt_matches = re.findall(r"(?m)^\*\*Prompt\*\*:\s*(.+)$", text)
    duration_matches = re.findall(r"(?m)^\*\*Duration\*\*:\s*(\d+)\s+seconds\.", text)
    camera_terms = (
        "close-up",
        "wide shot",
        "tracking shot",
        "dolly",
        "push-in",
        "pull-back",
        "pan",
        "tilt",
        "overhead",
        "macro",
        "lateral",
        "zoom",
        "crane shot",
        "aerial",
    )
    action_terms = (
        "reveals",
        "unfolding",
        "emerging",
        "rising",
        "drifting",
        "moving",
        "glowing",
        "fading",
        "curling",
        "tracking",
        "descending",
        "turning",
        "opening",
        "closing",
        "pulling back",
        "pushing in",
        "flowing",
        "eroding",
        "sweeping",
    )
    checks["video_prompt_section_count"] = prompt_sections
    checks["video_prompt_body_count"] = prompt_bodies
    checks["video_prompt_duration_count"] = duration_bodies
    checks["video_prompt_max_duration"] = max([int(item) for item in duration_matches], default=0)
    if expected_sections is not None and prompt_sections != expected_sections:
        add_issue(errors, f"video-prompts.md should align with briefing-card.md card count ({expected_sections}), found {prompt_sections}")
    elif prompt_sections < HARD_CARD_MIN:
        add_issue(errors, f"video-prompts.md should contain at least {HARD_CARD_MIN} prompt sections, found {prompt_sections}")
    if expected_sections is not None and prompt_bodies != expected_sections:
        add_issue(errors, f"video-prompts.md should contain {expected_sections} '**Prompt**' entries, found {prompt_bodies}")
    elif prompt_bodies != prompt_sections:
        add_issue(errors, f"video-prompts.md should contain one '**Prompt**' entry per section, found {prompt_bodies} prompts for {prompt_sections} sections")
    if expected_sections is not None and duration_bodies != expected_sections:
        add_issue(warnings, f"video-prompts.md should contain {expected_sections} '**Duration**' entries, found {duration_bodies}")
    elif duration_bodies != prompt_sections:
        add_issue(warnings, f"video-prompts.md should contain one '**Duration**' entry per section, found {duration_bodies} durations for {prompt_sections} sections")
    if any(int(item) > 15 for item in duration_matches):
        add_issue(errors, "video-prompts.md contains a duration longer than 15 seconds")
    if any(re.search(r"[\u4e00-\u9fff]", prompt) for prompt in prompt_matches):
        add_issue(warnings, "video-prompts.md still contains Chinese text inside one or more prompt bodies")
    if any(len(prompt.split()) < 12 for prompt in prompt_matches):
        add_issue(warnings, "one or more video prompt bodies are too short to be production-usable")
    if any(not any(term in prompt.lower() for term in camera_terms) for prompt in prompt_matches):
        add_issue(warnings, "one or more video prompt bodies are missing explicit camera language")
    if any(not any(term in prompt.lower() for term in action_terms) for prompt in prompt_matches):
        add_issue(warnings, "one or more video prompt bodies feel too static and may not match a Seedance-style shot prompt")
    return prompt_sections


def validate_exports(bundle_dir: Path, errors: list[str], warnings: list[str], checks: dict[str, Any], require_exports: bool) -> None:
    pdf_path = bundle_dir / "briefing-card.pdf"
    jpg_dir = bundle_dir / "briefing-card_jpg"
    jpg_files = sorted(jpg_dir.glob("*.jpg")) if jpg_dir.exists() else []
    checks["has_briefing_pdf"] = pdf_path.exists()
    checks["briefing_jpg_count"] = len(jpg_files)

    if require_exports and not pdf_path.exists():
        add_issue(errors, "Missing briefing-card.pdf")
    elif not pdf_path.exists():
        add_issue(warnings, "briefing-card.pdf has not been generated yet")

    if require_exports and not jpg_files:
        add_issue(errors, "Missing briefing-card_jpg/*.jpg exports")
    elif not jpg_files:
        add_issue(warnings, "briefing-card_jpg/*.jpg exports have not been generated yet")


def main() -> int:
    args = parse_args()
    bundle_dir = resolve_bundle_dir(args)
    bundle_id = bundle_dir.name
    errors: list[str] = []
    warnings: list[str] = []
    checks: dict[str, Any] = {}

    if not bundle_dir.exists():
        raise RuntimeError(f"Bundle directory not found: {bundle_dir}")

    validate_chapter_brief(bundle_dir / "chapter-brief.md", errors, warnings, checks, args.strict_support)
    validate_sources(bundle_dir / "sources.json", errors, warnings, checks, args.strict_support)
    content_card_count = validate_briefing_card(bundle_dir / "briefing-card.md", errors, warnings, checks)
    validate_talkshow(bundle_dir / "talkshow-script.md", errors, warnings, checks, content_card_count)
    validate_article(bundle_dir / "video-article.md", errors, warnings, checks, content_card_count)
    validate_video_prompts(bundle_dir / "video-prompts.md", errors, warnings, checks, content_card_count)
    validate_exports(bundle_dir, errors, warnings, checks, args.require_exports)

    payload = {
        "bundle_id": bundle_id,
        "bundle_dir": str(bundle_dir),
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
