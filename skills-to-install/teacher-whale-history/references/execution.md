# Teacher Whale Execution

Use this reference when you are ready to scaffold, validate, export, or publish a bundle.

## Preconditions

- Run commands from the `teacher-whale-history/` skill root.
- `GAMMA_API_KEY` is required for Gamma export.
- `uv` is preferred, but the helpers fall back to `python3` when possible.
- Before drafting, inspect `references/output-quality.md`. If a strong local finished bundle exists, you may inspect it as an optional comparison sample.

## Command patterns

Initialize a new bundle:

```bash
python3 scripts/init_bundle.py --bundle-id ch02-summary --title "第二章合集｜秦汉大一统国家的建立与巩固"
```

Validate a bundle without export requirements:

```bash
python3 scripts/validate_bundle.py --bundle-id ep06
```

Harvest candidate sources into a bundle:

```bash
python3 scripts/harvest_sources.py --bundle-id ep06 --query "悬泉置 汉简 遗址" --query "楼兰 尼雅 五星出东方利中国"
```

The harvesting helper now uses `web-hybrid-search`, so at least one of `LINKUP_API_KEY` or `SEARCHCANS_API_KEY` should be available in the environment.

Require PDF and JPG exports:

```bash
python3 scripts/validate_bundle.py --bundle-id ep06 --require-exports
```

Require support artifacts such as `chapter-brief.md` and `sources.json`:

```bash
python3 scripts/validate_bundle.py --bundle-id ep06 --strict-support
```

Export Gamma PDF and JPG pages:

```bash
bash scripts/export_gamma_social_bundle.sh /absolute/path/to/scripts/ep06/briefing-card.md cigar
```

Commit a finished bundle without pushing:

```bash
bash scripts/publish_episode.sh ep06 "Add ep06 Teacher Whale bundle" --no-push
```

Commit and push a finished bundle:

```bash
bash scripts/publish_episode.sh ep06 "Add ep06 Teacher Whale bundle"
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
