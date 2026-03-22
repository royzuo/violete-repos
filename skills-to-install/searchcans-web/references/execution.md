# SearchCans Execution

Use this reference when you are ready to run the skill or when execution fails.

## Preconditions

- `SEARCHCANS_API_KEY` must be set in the environment.
- Run commands from the `searchcans-web/` skill root.

## Command patterns

Search for links:

```bash
python3 scripts/searchcans.py search --query "AI agents" --engine google --timeout-ms 20000 --limit 5
```

Return JSON instead of text:

```bash
python3 scripts/searchcans.py search --query "AI agents" --format json
```

Print only the first result URL:

```bash
python3 scripts/searchcans.py search --query "AI agents" --pick-first-url
```

Read URL to markdown:

```bash
python3 scripts/searchcans.py read --url "https://example.com"
```

Use browser rendering for a JS-heavy page:

```bash
python3 scripts/searchcans.py read --url "https://example.com" --browser --wait-ms 5000
```

Truncate long markdown:

```bash
python3 scripts/searchcans.py read --url "https://example.com" --max-chars 12000
```

## Output handling

- `search --format text` prints a readable list of title, URL, and snippet.
- `search --format json` prints `{"data": [...]}`.
- `search --pick-first-url` prints a single URL or an empty string.
- `read --format markdown` prints markdown content.
- `read --format json` prints the raw response JSON.
- For best `read` quality, prefer the direct result URL found by `search` over a generic homepage or redirecting entry page.

## Failure triage

- Missing API key: set `SEARCHCANS_API_KEY`.
- HTTP failure: inspect the printed status code and response body.
- Empty markdown: retry with `--browser` or a longer `--wait-ms`.
- Shell-page or redirect noise: rerun `search` and choose the direct destination URL instead of the entry page.
- Low-quality or noisy output: fall back to another fetch path or reduce the page set.
