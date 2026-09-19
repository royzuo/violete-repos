#!/usr/bin/env bash
set -euo pipefail

PUSH_AFTER=1
REPO_ROOT="${REPO_ROOT:-}"
BUNDLE_ID=""
BUNDLE_DIR=""
POSITIONAL=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-push)
      PUSH_AFTER=0
      shift
      ;;
    --bundle-id)
      BUNDLE_ID="${2:-}"
      shift 2
      ;;
    --bundle-dir)
      BUNDLE_DIR="${2:-}"
      shift 2
      ;;
    --repo-root)
      REPO_ROOT="${2:-}"
      shift 2
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;
  esac
done

if [[ -n "$BUNDLE_ID" && -n "$BUNDLE_DIR" ]]; then
  echo "Provide either --bundle-id or --bundle-dir, not both" >&2
  exit 1
fi

if [[ -n "$BUNDLE_DIR" ]]; then
  TARGET_DIR="$(cd "$BUNDLE_DIR" && pwd)"
elif [[ -n "$BUNDLE_ID" ]]; then
  if [[ -z "$REPO_ROOT" ]]; then
    echo "--repo-root is required when using --bundle-id" >&2
    exit 1
  fi
  TARGET_DIR="$(cd "$REPO_ROOT/scripts/$BUNDLE_ID" && pwd)"
else
  if [[ ${#POSITIONAL[@]} -lt 1 || ${#POSITIONAL[@]} -gt 2 ]]; then
    echo "Usage: $0 [--bundle-dir <dir> | --bundle-id <id> --repo-root <root>] [commit-message] [--no-push]" >&2
    exit 1
  fi
  BUNDLE_ID="${POSITIONAL[0]}"
  POSITIONAL=("${POSITIONAL[@]:1}")
  if [[ -z "$REPO_ROOT" ]]; then
    echo "--repo-root is required when using positional bundle-id" >&2
    exit 1
  fi
  TARGET_DIR="$(cd "$REPO_ROOT/scripts/$BUNDLE_ID" && pwd)"
fi

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Bundle directory not found: $TARGET_DIR" >&2
  exit 1
fi

CUSTOM_MESSAGE="${POSITIONAL[0]:-}"

if [[ -z "$REPO_ROOT" ]]; then
  REPO_ROOT="$(git -C "$TARGET_DIR" rev-parse --show-toplevel)"
fi

RELATIVE_TARGET="$(python3 - <<'PY' "$REPO_ROOT" "$TARGET_DIR"
from pathlib import Path
import sys
print(Path(sys.argv[2]).resolve().relative_to(Path(sys.argv[1]).resolve()))
PY
)"

COMMIT_MESSAGE="$CUSTOM_MESSAGE"
if [[ -z "$COMMIT_MESSAGE" ]]; then
  COMMIT_MESSAGE="Add $(basename "$TARGET_DIR") Teacher Whale geography bundle"
fi

git -C "$REPO_ROOT" add "$RELATIVE_TARGET"

if git -C "$REPO_ROOT" diff --cached --quiet -- "$RELATIVE_TARGET"; then
  echo "No staged changes for $RELATIVE_TARGET"
  exit 0
fi

git -C "$REPO_ROOT" commit -m "$COMMIT_MESSAGE"

if [[ "$PUSH_AFTER" -eq 1 ]]; then
  git -C "$REPO_ROOT" push origin main
fi
