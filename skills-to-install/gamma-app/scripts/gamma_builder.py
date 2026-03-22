#!/usr/bin/env python3
"""Generate Gamma artifacts from markdown with a stable CLI.

The script posts to Gamma's Generations API, polls until completion, and
prints parseable output for downstream automation.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

API_BASE = "https://public-api.gamma.app/v1.0"
DEFAULT_TIMEOUT_SECONDS = 300
DEFAULT_POLL_INTERVAL_SECONDS = 3.0


def build_payload(
    input_text,
    format_name="presentation",
    theme_name=None,
    theme_id=None,
    export_as=None,
):
    payload = {
        "inputText": input_text,
        "textMode": "preserve",
        "format": format_name,
        "cardSplit": "inputTextBreaks",
        "cardOptions": {
            "dimensions": "9x16" if format_name == "social" else "fluid",
        },
    }
    if theme_name:
        payload["themeName"] = theme_name
    if theme_id:
        payload["themeId"] = theme_id
    if export_as:
        payload["exportAs"] = export_as
    return payload


def request_json(method, url, api_key, payload=None):
    body = None
    headers = {
        "Accept": "application/json",
        "User-Agent": "gamma-app-skill/1.0",
        "X-API-KEY": api_key,
    }
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        message = raw.strip() or exc.reason
        raise RuntimeError(f"Gamma API HTTP {exc.code}: {message}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Gamma API request failed: {exc.reason}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Gamma API returned invalid JSON: {raw}") from exc


def start_generation(api_key, payload):
    response = request_json(
        "POST",
        f"{API_BASE}/generations",
        api_key,
        payload=payload,
    )
    generation_id = response.get("generationId")
    if not generation_id:
        raise RuntimeError(
            "Gamma API did not return generationId: "
            + json.dumps(response, ensure_ascii=False)
        )
    return generation_id, response


def poll_generation(api_key, generation_id, poll_interval, timeout_seconds):
    deadline = time.monotonic() + timeout_seconds
    last_status = None

    while time.monotonic() < deadline:
        response = request_json(
            "GET",
            f"{API_BASE}/generations/{generation_id}",
            api_key,
        )
        status = response.get("status")

        if status == "completed":
            return response
        if status == "failed":
            raise RuntimeError(
                "Gamma generation failed: "
                + json.dumps(response, ensure_ascii=False)
            )

        last_status = status
        time.sleep(poll_interval)

    status_text = last_status or "unknown"
    raise RuntimeError(
        f"Timed out after {timeout_seconds}s waiting for generation "
        f"{generation_id} (last status: {status_text})"
    )


def read_input_text(input_file, inline_text):
    if inline_text is not None:
        return inline_text
    if not input_file:
        raise RuntimeError("Provide either an input file or --input-text.")

    path = Path(input_file)
    if not path.exists():
        raise RuntimeError(f"Input file not found: {path}")
    return path.read_text(encoding="utf-8")


def save_text(path_str, content):
    path = Path(path_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path.resolve()


def download_file(url, destination):
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "gamma-app-skill/1.0"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request) as response, path.open("wb") as handle:
            handle.write(response.read())
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        message = raw.strip() or exc.reason
        raise RuntimeError(f"Export download HTTP {exc.code}: {message}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Export download failed: {exc.reason}") from exc
    return path.resolve()


def print_text_result(result):
    ordered_keys = [
        "generationId",
        "status",
        "gammaUrl",
        "downloadUrl",
        "savedExport",
        "responseFile",
    ]
    for key in ordered_keys:
        value = result.get(key)
        if value:
            print(f"{key}={value}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a Gamma deck or social-card set from markdown.",
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="Path to the markdown storyboard file.",
    )
    parser.add_argument(
        "format",
        nargs="?",
        choices=["presentation", "social"],
        help="Gamma format to generate. Deprecated when using --input-text; prefer --format-name.",
    )
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--input-text",
        help="Inline markdown input. Use instead of input_file for automation.",
    )
    theme_group = parser.add_mutually_exclusive_group()
    theme_group.add_argument("--theme-name")
    theme_group.add_argument("--theme-id")
    parser.add_argument("--export-as", choices=["pdf", "pptx"])
    parser.add_argument(
        "--format-name",
        dest="format_name",
        choices=["presentation", "social"],
        help="Explicit Gamma format. Use this with --input-text to avoid positional ambiguity.",
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format for the final result.",
    )
    parser.add_argument(
        "--save-response",
        help="Write the final JSON response to this file.",
    )
    parser.add_argument(
        "--download-to",
        help="Download the exported file to this path when export URL is present.",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=DEFAULT_POLL_INTERVAL_SECONDS,
        help="Seconds between polling attempts.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Maximum seconds to wait for completion.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request payload and exit without calling Gamma.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    api_key = os.environ.get("GAMMA_API_KEY")

    try:
        format_name = args.format_name or args.format or "presentation"
        input_text = read_input_text(args.input_file, args.input_text)
        payload = build_payload(
            input_text=input_text,
            format_name=format_name,
            theme_name=args.theme_name,
            theme_id=args.theme_id,
            export_as=args.export_as,
        )

        if args.dry_run:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0

        if not api_key:
            raise RuntimeError("GAMMA_API_KEY environment variable not set.")
        if args.poll_interval <= 0:
            raise RuntimeError("--poll-interval must be greater than 0.")
        if args.timeout <= 0:
            raise RuntimeError("--timeout must be greater than 0.")

        generation_id, _ = start_generation(api_key, payload)
        final_response = poll_generation(
            api_key=api_key,
            generation_id=generation_id,
            poll_interval=args.poll_interval,
            timeout_seconds=args.timeout,
        )

        result = dict(final_response)
        result["generationId"] = generation_id
        result["downloadUrl"] = (
            final_response.get("downloadUrl")
            or final_response.get("exportUrl")
            or final_response.get("exportFileUrl")
        )

        if args.save_response:
            result["responseFile"] = str(
                save_text(
                    args.save_response,
                    json.dumps(final_response, ensure_ascii=False, indent=2) + "\n",
                )
            )

        if args.download_to and result.get("downloadUrl"):
            result["savedExport"] = str(
                download_file(result["downloadUrl"], args.download_to)
            )

        if args.output == "json":
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_text_result(result)
        return 0
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
