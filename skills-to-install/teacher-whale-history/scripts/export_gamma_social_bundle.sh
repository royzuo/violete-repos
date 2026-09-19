#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <briefing-card.md> [theme-id]" >&2
  exit 1
fi

MD_PATH="$1"
THEME_ID="${2:-cigar}"
FORMAT="social"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
WORKSPACE_ROOT="${WORKSPACE_ROOT:-$(cd "$SKILL_DIR/../.." && pwd)}"
GAMMA_BUILDER="$WORKSPACE_ROOT/skills/gamma-app/scripts/gamma_builder.py"
PDF_TO_JPG="$WORKSPACE_ROOT/skills/gamma-app/scripts/pdf_to_jpg.py"

run_python() {
  if command -v uv >/dev/null 2>&1; then
    uv run python "$@"
  else
    python3 "$@"
  fi
}

if [[ ! -f "$MD_PATH" ]]; then
  echo "Markdown file not found: $MD_PATH" >&2
  exit 1
fi

if [[ ! -f "$GAMMA_BUILDER" ]]; then
  echo "gamma_builder.py not found: $GAMMA_BUILDER" >&2
  exit 1
fi

if [[ ! -f "$PDF_TO_JPG" ]]; then
  echo "pdf_to_jpg.py not found: $PDF_TO_JPG" >&2
  exit 1
fi

if [[ -z "${GAMMA_API_KEY:-}" ]]; then
  echo "GAMMA_API_KEY is required" >&2
  exit 1
fi

OUT_DIR="$(dirname "$MD_PATH")"
BASE_NAME="$(basename "$MD_PATH" .md)"
PDF_PATH="$OUT_DIR/${BASE_NAME}.pdf"
JPG_DIR="$OUT_DIR/${BASE_NAME}_jpg"

TMP_OUT="$(mktemp)"
run_python "$GAMMA_BUILDER" "$MD_PATH" "$FORMAT" --theme-id "$THEME_ID" --export-as pdf | tee "$TMP_OUT"
EXPORT_URL="$(run_python - <<'PY' "$TMP_OUT"
from pathlib import Path
import re, sys
text = Path(sys.argv[1]).read_text(encoding='utf-8')
match = re.search(r'"exportUrl": "([^"]+)"', text) or re.search(r'DOWNLOAD_URL: (\S+)', text)
if not match:
    raise SystemExit('Could not parse export URL from Gamma output')
print(match.group(1))
PY
)"
rm -f "$TMP_OUT"

curl -L -A "curl/8.5.0" -o "$PDF_PATH" "$EXPORT_URL"
run_python "$PDF_TO_JPG" "$PDF_PATH" --output-dir "$JPG_DIR" --prefix "$BASE_NAME" --dpi 220 --quality 92

echo "PDF: $PDF_PATH"
echo "JPG_DIR: $JPG_DIR"
