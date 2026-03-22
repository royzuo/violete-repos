---
name: gamma-app
description: Generate Gamma presentations and social-card decks with the official Gamma Generations API. Use when the user wants a Gamma deck created, regenerated, themed, exported to PDF/PPTX, or converted from a topic, outline, notes, or markdown while preserving explicit card breaks.
---

# Gamma App

Use this skill to turn a topic, outline, notes, or finished markdown storyboard into a Gamma artifact with `scripts/gamma_builder.py`.

## Use this skill when

- The user asks for a Gamma presentation, Gamma doc, deck, slides, or social cards.
- The user wants existing notes or markdown converted into Gamma.
- The user cares about preserving exact card boundaries with `---`.
- The user wants Gamma output exported as PDF or PPTX.

## Inputs to gather

- Topic, source material, or existing outline
- Audience and goal
- Desired format
- Theme name or theme id, if specified
- Export target: none, `pdf`, or `pptx`
- Any hard constraints on tone, length, or structure

## Defaults

- If the user gives only a topic, research first and then draft the storyboard.
- Default to `presentation` unless the user clearly wants vertical social cards, in which case use `social`.
- Prefer leaving theme unspecified over guessing a theme that may not exist.
- If export is not requested, return the Gamma URL only.

## Workflow

1. Decide whether research is needed.
   - If the user provides current facts, company data, news, or claims that may have changed, verify them with available browsing tools before writing.
   - If the user already provides complete content, skip research and preserve their structure.
2. Draft the storyboard in markdown.
   - Use exact `---` lines to mark hard card breaks.
   - Keep one main idea per card.
   - Use clear headings, concise bullets, and image cues when useful.
   - Preserve user-provided `---` boundaries unless the user asks for restructuring.
   - Read `references/authoring.md` when you need guidance on narrative shape, card density, or adapting to different presentation types.
3. Save the storyboard to a temporary markdown file.
4. Run the builder script.
   - Run commands from the skill root.
   - Prefer `python3 scripts/gamma_builder.py <input_file> [format]`.
   - Add `--theme-name`, `--theme-id`, and `--export-as` only when needed.
   - Read `references/execution.md` for command patterns and failure handling.
5. Inspect the script output and capture the final `gammaUrl=...` and optional `downloadUrl=...`.
6. Return the result.
   - Share the Gamma URL.
   - Share the download URL when export was requested and available.
   - Briefly state key assumptions if you had to choose structure, audience, or format defaults.

## Constraints

- `scripts/gamma_builder.py` is the source of truth for invocation in this skill.
- The script is currently validated for `presentation` and `social`. Do not invent new format values unless the user provides a confirmed Gamma API requirement or the skill gains a validated example.
- The Gamma API respects card boundaries only when the markdown uses exact `---` separators on their own lines.

## Bundled resources

- `scripts/gamma_builder.py`: Posts to Gamma, polls completion, and prints the final URLs.
- `references/authoring.md`: How to shape the storyboard before generation.
- `references/execution.md`: How to run the script and interpret failures.
