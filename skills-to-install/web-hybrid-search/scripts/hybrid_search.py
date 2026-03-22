#!/usr/bin/env python3
"""Run hybrid search across SearchCans and Linkup and merge the result set."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

SEARCHCANS_API_KEY = os.environ.get("SEARCHCANS_API_KEY")
LINKUP_API_KEY = os.environ.get("LINKUP_API_KEY")
SEARCHCANS_BASE = "https://www.searchcans.com/api"
LINKUP_BASE = "https://api.linkup.so/v1/search"


def request_json(request: urllib.request.Request, timeout: int = 20) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {raw.strip() or exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc.reason}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Invalid JSON response: {raw}") from exc


def search_with_searchcans(query: str, limit: int, timeout_ms: int = 20000) -> list[dict[str, Any]]:
    if not SEARCHCANS_API_KEY:
        return []
    payload = {"s": query, "t": "google", "d": timeout_ms}
    request = urllib.request.Request(
        f"{SEARCHCANS_BASE}/search",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {SEARCHCANS_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "web-hybrid-search/1.0",
        },
        method="POST",
    )
    data = request_json(request)
    return [
        {
            "source": "searchcans",
            "title": item.get("title") or item.get("name") or "",
            "url": item.get("url") or "",
            "content": (item.get("snippet") or item.get("description") or "").strip(),
            "favicon": item.get("favicon") or "",
        }
        for item in (data.get("data") or [])[:limit]
        if item.get("url")
    ]


def search_with_linkup(query: str, limit: int) -> list[dict[str, Any]]:
    if not LINKUP_API_KEY:
        return []
    payload = {"q": query, "depth": "standard", "outputType": "searchResults"}
    request = urllib.request.Request(
        LINKUP_BASE,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {LINKUP_API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "web-hybrid-search/1.0",
        },
        method="POST",
    )
    data = request_json(request)
    return [
        {
            "source": "linkup",
            "title": item.get("name") or item.get("title") or "",
            "url": item.get("url") or "",
            "content": (item.get("content") or item.get("snippet") or "").strip(),
            "favicon": item.get("favicon") or "",
        }
        for item in (data.get("results") or [])[:limit]
        if item.get("url")
    ]


def deduplicate_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_priority = {"linkup": 0, "searchcans": 1}
    by_url: dict[str, dict[str, Any]] = {}
    for result in results:
        url = result.get("url")
        if not url:
            continue
        existing = by_url.get(url)
        if not existing or source_priority.get(result.get("source", ""), 99) < source_priority.get(existing.get("source", ""), 99):
            by_url[url] = result

    deduped: list[dict[str, Any]] = []
    titles_seen: list[str] = []
    for result in sorted(by_url.values(), key=lambda item: source_priority.get(item.get("source", ""), 99)):
        title = result.get("title", "")
        if title and any(SequenceMatcher(None, title, seen).ratio() > 0.9 for seen in titles_seen):
            continue
        if title:
            titles_seen.append(title)
        deduped.append(result)
    return deduped


def hybrid_search(query: str, limit: int, min_results: int) -> dict[str, Any]:
    providers = []
    if SEARCHCANS_API_KEY:
        providers.append(("searchcans", lambda: search_with_searchcans(query, limit)))
    if LINKUP_API_KEY:
        providers.append(("linkup", lambda: search_with_linkup(query, limit)))
    if not providers:
        raise RuntimeError("At least one of SEARCHCANS_API_KEY or LINKUP_API_KEY must be set")

    all_results: list[dict[str, Any]] = []
    tools_used: list[str] = []
    errors: dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=len(providers)) as executor:
        futures = {executor.submit(func): name for name, func in providers}
        for future in as_completed(futures):
            name = futures[future]
            try:
                results = future.result()
            except Exception as exc:
                errors[name] = str(exc)
                continue
            if results:
                tools_used.append(name)
                all_results.extend(results)

    merged = deduplicate_results(all_results)
    if len(merged) < min_results:
        raise RuntimeError(
            f"Hybrid search returned {len(merged)} results, below the required minimum of {min_results}"
        )
    return {
        "query": query,
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tools_used": tools_used,
        "errors": errors,
        "min_results_target": min_results,
        "total_results": len(merged),
        "results": merged,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run merged hybrid search with SearchCans and Linkup.")
    parser.add_argument("--query", "-q", required=True)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--min-results", type=int, default=1)
    parser.add_argument("--output", "-o")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = hybrid_search(query=args.query, limit=args.limit, min_results=args.min_results)
        rendered = json.dumps(payload, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(rendered + "\n", encoding="utf-8")
        print(rendered)
        return 0
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
