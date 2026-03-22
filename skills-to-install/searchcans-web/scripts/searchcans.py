#!/usr/bin/env python3
"""SearchCans client: web search plus URL reader with a stable CLI."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any

BASE = "https://www.searchcans.com/api"


def api_key() -> str:
    key = os.environ.get("SEARCHCANS_API_KEY")
    if not key:
        raise RuntimeError("SEARCHCANS_API_KEY is not set")
    return key


def post_json(path: str, payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{BASE}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "searchcans-web-skill/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        message = raw.strip() or exc.reason
        raise RuntimeError(f"SearchCans HTTP {exc.code}: {message}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"SearchCans request failed: {exc.reason}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"SearchCans returned invalid JSON: {raw}") from exc


def cmd_search(args: argparse.Namespace) -> int:
    data = post_json(
        "/search",
        {"s": args.query, "t": args.engine, "d": args.timeout_ms},
        timeout=args.client_timeout,
    )
    results = data.get("data", [])
    if args.limit:
        results = results[: args.limit]

    if args.pick_first_url:
        print(results[0].get("url", "") if results else "")
        return 0

    if args.format == "json":
        print(json.dumps({"data": results}, ensure_ascii=False, indent=2))
        return 0

    for result in results:
        title = result.get("title") or result.get("name") or ""
        url = result.get("url") or ""
        snippet = (result.get("snippet") or result.get("description") or "").strip()
        print(f"- {title}\n  {url}\n  {snippet}\n")
    return 0


def cmd_read(args: argparse.Namespace) -> int:
    data = post_json(
        "/url",
        {
            "s": args.url,
            "t": "url",
            "b": bool(args.browser),
            "w": args.wait_ms,
        },
        timeout=args.client_timeout,
    )

    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    markdown = (data.get("data") or {}).get("markdown")
    if not markdown:
        raise RuntimeError("No markdown in SearchCans response")
    if args.max_chars and len(markdown) > args.max_chars:
        markdown = markdown[: args.max_chars] + "\n\n[...truncated...]\n"
    print(markdown)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search the web or extract URL markdown with SearchCans.",
    )
    parser.add_argument("--client-timeout", type=int, default=30)
    subcommands = parser.add_subparsers(dest="cmd", required=True)

    search = subcommands.add_parser("search")
    search.add_argument("--query", required=True)
    search.add_argument("--engine", default="google")
    search.add_argument("--timeout-ms", type=int, default=20000)
    search.add_argument("--limit", type=int, default=5)
    search.add_argument("--format", choices=["text", "json"], default="text")
    search.add_argument("--pick-first-url", action="store_true")
    search.set_defaults(fn=cmd_search)

    read = subcommands.add_parser("read")
    read.add_argument("--url", required=True)
    read.add_argument("--browser", action="store_true")
    read.add_argument("--wait-ms", type=int, default=3000)
    read.add_argument("--format", choices=["markdown", "json"], default="markdown")
    read.add_argument("--max-chars", type=int, default=0)
    read.set_defaults(fn=cmd_read)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.fn(args)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
