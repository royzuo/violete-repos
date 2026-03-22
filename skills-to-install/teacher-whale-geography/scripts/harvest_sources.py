#!/usr/bin/env python3
"""Harvest candidate source links for a Teacher Whale geography bundle."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Harvest candidate source links with web-hybrid-search.")
    parser.add_argument("--bundle-id", help="Bundle directory name under scripts/")
    parser.add_argument("--bundle-dir", help="Absolute or relative path to the bundle directory")
    parser.add_argument("--output-root", help="Optional repo root override")
    parser.add_argument("--query", action="append", required=True, help="Search query; pass multiple times for multiple queries")
    parser.add_argument("--limit", type=int, default=5, help="Max results per query")
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


_HYBRID_MODULE: Any | None = None


def hybrid_module() -> Any:
    global _HYBRID_MODULE
    if _HYBRID_MODULE is not None:
        return _HYBRID_MODULE

    module_path = repo_root_from_script() / "skills" / "web-hybrid-search" / "scripts" / "hybrid_search.py"
    spec = importlib.util.spec_from_file_location("teacher_whale_web_hybrid_search", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load web-hybrid-search module from: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _HYBRID_MODULE = module
    return module


def run_hybrid_search(query: str, limit: int) -> dict[str, Any]:
    module = hybrid_module()
    return module.hybrid_search(query=query, limit=limit, min_results=0)


def domain_for_url(url: str) -> str:
    return urllib.parse.urlparse(url).netloc.lower()


def truncate_text(text: str, max_chars: int = 500) -> str:
    normalized = re.sub(r"\s+", " ", (text or "").strip())
    return normalized[:max_chars].strip()


def harvest_query(query: str, limit: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    payload = run_hybrid_search(query=query, limit=limit)
    harvested: list[dict[str, Any]] = []
    for item in payload.get("results", [])[:limit]:
        url = item.get("url") or item.get("link")
        if not url:
            continue
        harvested.append(
            {
                "title": item.get("title") or item.get("name") or "",
                "url": url,
                "summary": truncate_text(item.get("content") or item.get("summary") or ""),
                "query": query,
                "source": domain_for_url(url),
                "provider": item.get("source"),
                "retrieval_stage": "web_hybrid_search",
            }
        )
    run_record = {
        "query": query,
        "tools_used": payload.get("tools_used", []),
        "errors": payload.get("errors", {}),
        "result_count": len(harvested),
    }
    return harvested, run_record


def deduplicate(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for item in items:
        url = item.get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        unique.append(item)
    return unique


def main() -> int:
    args = parse_args()
    bundle_dir = resolve_bundle_dir(args)
    if not bundle_dir.exists():
        raise RuntimeError(f"Bundle directory not found: {bundle_dir}")

    results: list[dict[str, Any]] = []
    runs: list[dict[str, Any]] = []
    for query in args.query:
        harvested, run_record = harvest_query(query, args.limit)
        results.extend(harvested)
        runs.append(run_record)

    deduped = deduplicate(results)
    payload = {
        "bundle_id": bundle_dir.name,
        "queries": args.query,
        "runs": runs,
        "results": deduped,
    }
    output_path = bundle_dir / "source-candidates.json"
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"bundle_dir={bundle_dir}")
    print(f"candidate_file={output_path}")
    print(f"result_count={len(deduped)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
