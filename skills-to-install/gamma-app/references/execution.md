# Gamma Execution

Use this reference only when you are ready to run the skill or when execution fails.

## Preconditions

- `GAMMA_API_KEY` must be set in the environment.
- The markdown file must exist on disk.
- The markdown should already contain final `---` card breaks.
- Run commands from the `gamma-app/` skill root.
- Valid format values for this skill are `presentation` and `social`.

## Command patterns

Basic presentation:

```bash
python3 scripts/gamma_builder.py /tmp/gamma.md
```

Vertical social cards:

```bash
python3 scripts/gamma_builder.py /tmp/gamma.md social
```

With theme and export:

```bash
python3 scripts/gamma_builder.py /tmp/gamma.md presentation --theme-name ash --export-as pdf
```

Using a theme id instead of a theme name:

```bash
python3 scripts/gamma_builder.py /tmp/gamma.md presentation --theme-id <theme_id>
```

Save the final API response and download the export:

```bash
python3 scripts/gamma_builder.py /tmp/gamma.md presentation --export-as pdf --save-response /tmp/gamma-response.json --download-to /tmp/gamma.pdf
```

Use inline markdown for automation:

```bash
python3 scripts/gamma_builder.py --input-text $'# Title\n---\n# Card 2' --format-name presentation --output json
```

Validate payload shape without calling Gamma:

```bash
python3 scripts/gamma_builder.py /tmp/gamma.md social --theme-id my-theme --export-as pdf --dry-run
```

## Output handling

- Default text mode prints parseable `key=value` lines such as `gammaUrl=...` and `downloadUrl=...`.
- `--output json` prints the final response JSON plus normalized fields like `generationId`, `downloadUrl`, and optional local file paths.
- `--save-response` writes the raw final API response to disk.
- `--download-to` downloads the exported file when the response contains an export URL.

## Failure triage

- Missing API key: set `GAMMA_API_KEY` before running.
- Missing file: verify the input path and write the markdown file first.
- API failure: inspect the JSON payload printed by the script.
- Poor card boundaries: check that separators are exact `---` lines with no extra text.
- Timeout: increase `--timeout` for slower generations.
