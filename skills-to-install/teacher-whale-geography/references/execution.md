# Teacher Whale Geography Execution

Use this reference when you are ready to scaffold, validate, export, or publish a bundle.

## Preconditions

- Run commands from the `teacher-whale-geography/` skill root.
- `GAMMA_API_KEY` is required for Gamma export.
- `uv` is preferred, but the helpers fall back to `python3` when possible.
- The harvesting helper uses `web-hybrid-search`, so at least one of `LINKUP_API_KEY` or `SEARCHCANS_API_KEY` should be available in the environment.
- Before drafting, inspect `references/briefing-guide.md`, `references/output-quality.md`, and `program-outlines/geography-program-water-epic-outline.md` when the bundle is tied to the current season plan.

## Command patterns

Initialize a new bundle:

```bash
python3 scripts/init_bundle.py --bundle-id nile-delta --title "尼罗河三角洲：水的史诗如何塑造文明"
```

Validate a bundle without export requirements:

```bash
python3 scripts/validate_bundle.py --bundle-id nile-delta
```

Harvest candidate sources into a bundle:

```bash
python3 scripts/harvest_sources.py --bundle-id nile-delta --query "尼罗河三角洲 形成过程 地理意义" --query "尼罗河三角洲 近三天 新闻"
```

Require PDF and JPG exports:

```bash
python3 scripts/validate_bundle.py --bundle-id nile-delta --require-exports
```

Require support artifacts such as `chapter-brief.md` and `sources.json`:

```bash
python3 scripts/validate_bundle.py --bundle-id nile-delta --strict-support
```

Export Gamma PDF and JPG pages:

```bash
bash scripts/export_gamma_social_bundle.sh /absolute/path/to/scripts/nile-delta/briefing-card.md cigar
```

Commit a finished bundle without pushing:

```bash
bash scripts/publish_episode.sh nile-delta "Add nile-delta Teacher Whale geography bundle" --no-push
```

Commit and push a finished bundle:

```bash
bash scripts/publish_episode.sh nile-delta "Add nile-delta Teacher Whale geography bundle"
```

## Validation output

- The validator prints a JSON payload with:
  - `bundle_id`
  - `bundle_dir`
  - `errors`
  - `warnings`
  - `checks`
- Exit code `0` means the bundle passed.
- Exit code `1` means one or more validation errors were found.
