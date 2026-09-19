#!/usr/bin/env python3
"""Report whether the environment is ready for authoring, research, and export."""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def has_adjacent_skill(skill_name: str, relative_file: str) -> bool:
    skill_root = skill_root_from_script()
    candidate_paths = [
        skill_root.parent / skill_name / relative_file,
    ]
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        candidate_paths.append(Path(codex_home).expanduser() / "skills" / skill_name / relative_file)
    return any(path.exists() for path in candidate_paths)


def item(name: str, status: str, kind: str, detail: str) -> dict[str, str]:
    return {
        "name": name,
        "status": status,
        "kind": kind,
        "detail": detail,
    }


def main() -> int:
    checks: list[dict[str, str]] = []

    checks.append(
        item(
            "authoring_core",
            "ready",
            "required",
            "Markdown authoring, bundle planning, and validation are bundled in this skill.",
        )
    )

    if os.environ.get("GAMMA_API_KEY"):
        checks.append(item("gamma_api_key", "ready", "optional", "GAMMA export can call the public Gamma API."))
    else:
        checks.append(
            item(
                "gamma_api_key",
                "missing",
                "optional",
                "Set GAMMA_API_KEY to export PDF/JPG artifacts. Missing this does not block research or drafting.",
            )
        )

    if shutil.which("pdftoppm"):
        checks.append(item("pdftoppm", "ready", "optional", "PDF to JPG conversion is available through poppler."))
    elif shutil.which("magick"):
        checks.append(item("magick", "ready", "optional", "PDF to JPG conversion is available through ImageMagick."))
    else:
        checks.append(
            item(
                "pdf_rasterizer",
                "missing",
                "optional",
                "Install poppler (`pdftoppm`) or ImageMagick (`magick`) for JPG export. Missing this does not block authoring.",
            )
        )

    if has_adjacent_skill("web-hybrid-search", "scripts/hybrid_search.py"):
        checks.append(
            item(
                "web_hybrid_search",
                "ready",
                "optional",
                "Automated source harvesting helper is available.",
            )
        )
    else:
        checks.append(
            item(
                "web_hybrid_search",
                "missing",
                "optional",
                "Install the `web-hybrid-search` skill for automated harvesting, or gather sources manually with built-in browsing/search tools.",
            )
        )

    if os.environ.get("LINKUP_API_KEY") or os.environ.get("SEARCHCANS_API_KEY"):
        checks.append(item("search_provider_key", "ready", "optional", "Hybrid search has at least one provider key available."))
    else:
        checks.append(
            item(
                "search_provider_key",
                "missing",
                "optional",
                "Set LINKUP_API_KEY or SEARCHCANS_API_KEY for the harvesting helper, or research manually.",
            )
        )

    summary = {
        "ready_for_authoring": True,
        "ready_for_research_automation": any(
            check["name"] == "web_hybrid_search" and check["status"] == "ready" for check in checks
        )
        and any(check["name"] == "search_provider_key" and check["status"] == "ready" for check in checks),
        "ready_for_gamma_export": any(check["name"] == "gamma_api_key" and check["status"] == "ready" for check in checks),
        "ready_for_jpg_export": any(check["name"] in {"pdftoppm", "magick"} and check["status"] == "ready" for check in checks),
        "checks": checks,
    }

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
