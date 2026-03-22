---
name: searchcans-web
description: Search the web and extract LLM-ready page markdown with the SearchCans API. Use when the user needs SearchCans as an alternative search tool, especially for JS-rendered pages, URL-to-markdown extraction, or fast link discovery with SEARCHCANS_API_KEY.
---

# SearchCans Web

Use this skill when SearchCans is the preferred or fallback web retrieval path and you want a small CLI for search results or URL-to-markdown extraction.

## Use this skill when

- The user needs SearchCans specifically.
- You want quick web search results from SearchCans SERP.
- You want markdown extraction from a URL.
- Browser rendering may be needed for a JS-heavy page.
- You need a fallback when the primary fetch path is blocked or poor quality.

## Inputs to gather

- Search query or target URL
- Whether the task is search or read
- Whether browser rendering is needed
- Desired output shape: text, json, or markdown
- Any truncation requirement for long markdown

## Defaults

- Prefer `search` to discover candidate URLs.
- Use `read` only for the URLs you actually need.
- Keep result counts small unless broad coverage is explicitly needed.
- Prefer plain markdown output for page extraction and JSON output for automation.

## Workflow

1. Confirm `SEARCHCANS_API_KEY` is available.
2. Decide the mode.
   - Use `search` for discovery.
   - Use `read` for URL extraction.
   - Prefer the direct final URL returned by search over a homepage, redirect page, or generic landing page.
3. Run the script from the skill root.
   - Use `python3 scripts/searchcans.py ...`
   - Read `references/execution.md` for command patterns and failure handling.
4. Inspect the output.
   - For `search`, prefer a small list of relevant URLs before reading content.
   - For `read`, verify markdown quality before summarizing.
5. Continue with your downstream task using only the URLs or markdown you actually need.

## Constraints

- SearchCans is primarily for finding links and extracting markdown, not for final answer synthesis.
- Browser rendering adds latency; only enable it when the page likely needs JS execution.
- Do not use SearchCans reader by default when another fetch path already returns clean content.
- `read` is more reliable on direct content URLs than on entry pages that redirect or render shell content.

## Bundled resources

- `scripts/searchcans.py`: SearchCans CLI for search and URL read flows.
- `references/api.md`: Minimal API contract for the endpoints used by the script.
- `references/execution.md`: Command patterns, output shapes, and failure triage.
