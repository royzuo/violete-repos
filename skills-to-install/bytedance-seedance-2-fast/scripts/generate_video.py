#!/usr/bin/env python3
"""Generate short videos with the Volcengine Seedance API."""

import argparse
import base64
import hashlib
import hmac
import json
import logging
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

VOLC_ACCESSKEY = os.environ.get("VOLC_ACCESSKEY")
VOLC_SECRETKEY = os.environ.get("VOLC_SECRETKEY")
SERVICE = "cv"
REGION = "cn-north-1"
HOST = "visual.volcengineapi.com"
CONTENT_TYPE = "application/json; charset=utf-8"
MAX_WAIT_TIME = 600
POLL_INTERVAL = 5


def sha256_hex(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def hmac_sha256(key: bytes, content: str) -> bytes:
    return hmac.new(key, content.encode("utf-8"), hashlib.sha256).digest()


def norm_query(params: dict[str, Any]) -> str:
    query = ""
    for key in sorted(params.keys()):
        value = params[key]
        if isinstance(value, list):
            for item in value:
                query += urllib.parse.quote(key, safe="-_.~") + "=" + urllib.parse.quote(str(item), safe="-_.~") + "&"
        else:
            query += urllib.parse.quote(key, safe="-_.~") + "=" + urllib.parse.quote(str(value), safe="-_.~") + "&"
    return query[:-1].replace("+", "%20")


def sign_request(method: str, path: str, query_params: dict[str, Any], body: str, now: datetime) -> dict[str, str]:
    x_date = now.strftime("%Y%m%dT%H%M%SZ")
    short_x_date = x_date[:8]
    x_content_sha256 = sha256_hex(body)
    signed_headers_str = ";".join(["content-type", "host", "x-content-sha256", "x-date"])

    canonical_request_str = "\n".join(
        [
            method.upper(),
            path,
            norm_query(query_params),
            "\n".join(
                [
                    f"content-type:{CONTENT_TYPE}",
                    f"host:{HOST}",
                    f"x-content-sha256:{x_content_sha256}",
                    f"x-date:{x_date}",
                ]
            ),
            "",
            signed_headers_str,
            x_content_sha256,
        ]
    )

    hashed_canonical_request = sha256_hex(canonical_request_str)
    credential_scope = "/".join([short_x_date, REGION, SERVICE, "request"])
    string_to_sign = "\n".join(["HMAC-SHA256", x_date, credential_scope, hashed_canonical_request])

    k_date = hmac_sha256(VOLC_SECRETKEY.encode("utf-8"), short_x_date)
    k_region = hmac_sha256(k_date, REGION)
    k_service = hmac_sha256(k_region, SERVICE)
    k_signing = hmac_sha256(k_service, "request")
    signature = hmac_sha256(k_signing, string_to_sign).hex()

    return {
        "Host": HOST,
        "X-Content-Sha256": x_content_sha256,
        "X-Date": x_date,
        "Content-Type": CONTENT_TYPE,
        "Authorization": (
            f"HMAC-SHA256 Credential={VOLC_ACCESSKEY}/{credential_scope}, "
            f"SignedHeaders={signed_headers_str}, Signature={signature}"
        ),
    }


def request_json(query_params: dict[str, Any], body: dict[str, Any]) -> dict[str, Any]:
    now = datetime.now(timezone.utc)
    body_text = json.dumps(body)
    headers = sign_request("POST", "/", query_params, body_text, now)
    url = f"https://{HOST}/?{urllib.parse.urlencode(query_params)}"
    request = urllib.request.Request(
        url=url,
        data=body_text.encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Volcengine HTTP {exc.code}: {raw.strip() or exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Volcengine request failed: {exc.reason}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Volcengine returned invalid JSON: {raw}") from exc


def build_payload(prompt: str, duration: int, image_path: str | None, end_image_path: str | None) -> dict[str, Any]:
    frames = 121 if duration <= 5 else 241
    payload: dict[str, Any] = {
        "req_key": "jimeng_t2v_v30",
        "model": "seedance-3-0-720p",
        "prompt": prompt,
        "frames": frames,
        "aspect_ratio": "16:9",
    }

    if image_path:
        with open(image_path, "rb") as handle:
            payload["image"] = base64.b64encode(handle.read()).decode("utf-8")
    if end_image_path:
        with open(end_image_path, "rb") as handle:
            payload["end_image"] = base64.b64encode(handle.read()).decode("utf-8")
    return payload


def extract_task_id(result: dict[str, Any]) -> str:
    error = result.get("ResponseMetadata", {}).get("Error", {})
    if error:
        raise RuntimeError(error.get("Message", "Unknown task submission error"))
    task_id = result.get("data", {}).get("task_id") or result.get("data", {}).get("id")
    if not task_id:
        raise RuntimeError(f"Task submission did not return task_id: {json.dumps(result, ensure_ascii=False)}")
    return task_id


def submit_task(payload: dict[str, Any]) -> str:
    logger.info("提交视频生成任务...")
    result = request_json(
        {"Action": "CVSync2AsyncSubmitTask", "Version": "2022-08-31"},
        payload,
    )
    task_id = extract_task_id(result)
    logger.info(f"任务已提交：{task_id}")
    return task_id


def get_result(task_id: str) -> tuple[str | None, str]:
    result = request_json(
        {"Action": "CVSync2AsyncGetResult", "Version": "2022-08-31"},
        {"req_key": "jimeng_t2v_v30", "task_id": task_id},
    )
    if result.get("code") not in (None, 0, 10000) and result.get("status") not in (None, 0, 10000):
        error = result.get("ResponseMetadata", {}).get("Error", {})
        raise RuntimeError(error.get("Message", "Unknown task query error"))

    data = result.get("data", {})
    status = data.get("status", "PENDING")
    video_url = None
    if status in ("success", "completed", "SUCCESS", "done"):
        video_url = data.get("video_url") or data.get("output", {}).get("video_url") or data.get("result", {}).get("video_url")
    return video_url, status


def download_video(url: str, output_path: str) -> None:
    logger.info(f"下载视频：{output_path}")
    request = urllib.request.Request(url, headers={"User-Agent": "seedance-skill/1.0"}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=300) as response, open(output_path, "wb") as handle:
            handle.write(response.read())
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Video download HTTP {exc.code}: {exc.reason}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Video download failed: {exc.reason}") from exc


def generate_video(payload: dict[str, Any]) -> tuple[str, str]:
    task_id = submit_task(payload)
    logger.info("等待视频生成完成...")
    start_time = time.time()

    while True:
        elapsed = int(time.time() - start_time)
        if elapsed >= MAX_WAIT_TIME:
            raise RuntimeError("等待视频生成超时")
        time.sleep(POLL_INTERVAL)
        video_url, status = get_result(task_id)
        logger.info(f"任务状态：{status} (已等待 {elapsed}s)")
        if video_url:
            return task_id, video_url
        if status in ("failed", "ERROR"):
            raise RuntimeError(f"任务失败，状态={status}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate short videos with ByteDance Seedance 3.0 720p.")
    parser.add_argument("--prompt", "-p", required=True, help="Video prompt")
    parser.add_argument("--output", "-o", default="output.mp4", help="Output video path")
    parser.add_argument("--duration", "-d", type=int, default=5, choices=[5, 10])
    parser.add_argument("--image", "-i", help="Start image path")
    parser.add_argument("--end-image", "-e", help="End image path")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Print the request payload and exit")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    try:
        payload = build_payload(
            prompt=args.prompt,
            duration=args.duration,
            image_path=args.image,
            end_image_path=args.end_image,
        )

        if args.dry_run:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0

        if not VOLC_ACCESSKEY or not VOLC_SECRETKEY:
            raise RuntimeError("VOLC_ACCESSKEY or VOLC_SECRETKEY is not set")

        task_id, video_url = generate_video(payload)
        print(f"task_id={task_id}")
        print(f"video_url={video_url}")
        output_path = str(Path(args.output).resolve())
        download_video(video_url, output_path)
        print(f"output_file={output_path}")
        return 0
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
