# Hybrid Search Execution

Use this reference when you are ready to run the hybrid search script or when it fails.

## Preconditions

- At least one of these must be set:
  - `SEARCHCANS_API_KEY`
  - `LINKUP_API_KEY`
- Run commands from the `web-hybrid-search/` skill root.

## Command patterns

Basic search:

```bash
python3 scripts/hybrid_search.py --query "OpenAI API docs"
```

Increase the per-provider result limit:

```bash
python3 scripts/hybrid_search.py --query "OpenAI API docs" --limit 8
```

Require a higher minimum result threshold:

```bash
python3 scripts/hybrid_search.py --query "OpenAI API docs" --min-results 8
```

Write output to a file:

```bash
python3 scripts/hybrid_search.py --query "OpenAI API docs" --output results.json
```

## Output handling

- The script prints JSON to stdout.
- The JSON includes:
  - `query`
  - `timestamp`
  - `tools_used`
  - `total_results`
  - `results`

## Failure triage

- No provider key available: set `SEARCHCANS_API_KEY` or `LINKUP_API_KEY`
- Returned fewer than `--min-results`: lower the threshold or increase `--limit`
- Provider-specific failures: inspect the returned `errors` map
- Weak coverage: increase `--limit` or follow up with manual fetching on the best URLs
