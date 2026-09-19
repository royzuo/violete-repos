# Teacher Whale Geography Execution

Use this reference when you are ready to scaffold, validate, export, or publish a bundle.

## Preconditions

- Run commands from the `teacher-whale-geography/` skill root unless you are using absolute paths.
- Prefer explicit `--bundle-dir` paths over implicit repo-relative bundle ids.
- The first priority is a correct, evidence-backed bundle. Helper automation is secondary.
- `GAMMA_API_KEY` is required for Gamma export.
- Gamma export talks to Gamma's public HTTPS API through `scripts/gamma_builder.py`; it does not need an `acpx` backend.
- If Gamma export or source harvesting fails because the sandbox blocks network access, rerun the command with escalated permissions.
- `uv` is preferred, but the helpers fall back to `python3` when possible.
- The harvesting helper uses the separately installed `web-hybrid-search` skill, so at least one of `LINKUP_API_KEY` or `SEARCHCANS_API_KEY` should be available in the environment.
- For JPG conversion, prefer having `pdftoppm` available; the helper also tries `magick` when present.
- Before drafting, inspect `references/briefing-guide.md`, `references/output-quality.md`, and any season outline in the working tree. In this repo snapshot the active outline is `../../tasks/teacher-whale-geography/ch02/geography-program-water-epic-outline.md`.

## Command patterns

Inspect environment readiness:

```bash
python3 scripts/check_environment.py
```

Initialize a new bundle:

```bash
python3 scripts/init_bundle.py --bundle-dir ../../tasks/teacher-whale-geography/ch02/ep06 --title "天空之镜——乌尤尼盐沼为什么能在最干旱的高原上变成一片海"
```

Validate a bundle without export requirements:

```bash
python3 scripts/validate_bundle.py --bundle-dir ../../tasks/teacher-whale-geography/ch02/ep06
```

Harvest candidate sources into a bundle:

```bash
python3 scripts/harvest_sources.py --bundle-dir ../../tasks/teacher-whale-geography/ch02/ep06 --query "乌尤尼盐沼 形成过程 地理意义" --query "乌尤尼盐沼 近三天 新闻"
```

If harvesting automation is unavailable, use direct browsing/search tools and curate `sources.json` manually. Do not lower the evidence bar.

Require PDF and JPG exports:

```bash
python3 scripts/validate_bundle.py --bundle-dir ../../tasks/teacher-whale-geography/ch02/ep06 --require-exports
```

Require support artifacts such as `chapter-brief.md` and `sources.json`:

```bash
python3 scripts/validate_bundle.py --bundle-dir ../../tasks/teacher-whale-geography/ch02/ep06 --strict-support
```

Export Gamma PDF and JPG pages:

```bash
bash scripts/export_gamma_social_bundle.sh /absolute/path/to/tasks/teacher-whale-geography/ch02/ep06/briefing-card.md cigar
```

Commit a finished bundle without pushing:

```bash
bash scripts/publish_episode.sh --bundle-dir ../../tasks/teacher-whale-geography/ch02/ep06 "Add ep06 Teacher Whale geography bundle" --no-push
```

Commit and push a finished bundle:

```bash
bash scripts/publish_episode.sh --bundle-dir ../../tasks/teacher-whale-geography/ch02/ep06 "Add ep06 Teacher Whale geography bundle"
```

## Validation output

- The validator prints a JSON payload with:
  - `bundle_id`
  - `bundle_dir`
  - `errors`
  - `warnings`
  - `checks`
- The checks cover not only file presence and counts, but also card-plan alignment and `sources.json` richness.
- Exit code `0` means the bundle passed.
- Exit code `1` means one or more validation errors were found.

## Fallback policy

- If `web-hybrid-search` or its provider keys are unavailable, research manually and keep `sources.json` rigorous.
- If `GAMMA_API_KEY` or outbound network access is unavailable, complete the markdown bundle first and report export as the only blocked downstream artifact.
- Do not weaken the factual support, article depth, or output alignment just because an automation helper is missing.
