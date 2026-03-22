#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <bundle-id> [commit-message] [--no-push]" >&2
  exit 1
fi

PUSH_AFTER=1
POSITIONAL=()
for arg in "$@"; do
  case "$arg" in
    --no-push)
      PUSH_AFTER=0
      ;;
    *)
      POSITIONAL+=("$arg")
      ;;
  esac
done

set -- "${POSITIONAL[@]}"

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <bundle-id> [commit-message] [--no-push]" >&2
  exit 1
fi

BUNDLE_ID="$1"
CUSTOM_MESSAGE="${2:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="${REPO_ROOT:-$(cd "$SKILL_DIR/../.." && pwd)}"
TARGET_DIR="$REPO_ROOT/scripts/$BUNDLE_ID"

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Bundle directory not found: $TARGET_DIR" >&2
  exit 1
fi

COMMIT_MESSAGE="$CUSTOM_MESSAGE"
if [[ -z "$COMMIT_MESSAGE" ]]; then
  COMMIT_MESSAGE="Add ${BUNDLE_ID} Teacher Whale geography bundle"
fi

git -C "$REPO_ROOT" add "scripts/$BUNDLE_ID"

if git -C "$REPO_ROOT" diff --cached --quiet -- "scripts/$BUNDLE_ID"; then
  echo "No staged changes for scripts/$BUNDLE_ID"
  exit 0
fi

git -C "$REPO_ROOT" commit -m "$COMMIT_MESSAGE"

if [[ "$PUSH_AFTER" -eq 1 ]]; then
  git -C "$REPO_ROOT" push origin main
fi
