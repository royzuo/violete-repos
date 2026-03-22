---
name: bytedance-seedance-2-fast
description: Generate short Seedance 3.0 720p videos with Volcengine Jimeng APIs, including topic-to-prompt preparation and optional image-guided generation. Use when the user wants a ByteDance Seedance clip, a structured cinematic prompt, or a fast T2V or I2V workflow with VOLC_ACCESSKEY and VOLC_SECRETKEY.
---

# ByteDance Seedance 2 Fast

Use this skill to create short cinematic video prompts and generate Seedance 3.0 720p clips with the Volcengine visual API.

## Use this skill when

- The user wants a short AI video clip.
- The user gives a topic and wants help turning it into a good video prompt.
- The user wants text-to-video generation.
- The user wants image-to-video generation with a start frame or start/end frames.

## Inputs to gather

- Topic or finalized prompt
- Output file path
- Duration: `5` or `10`
- Whether the run is text-to-video or image-guided
- Optional start image and end image

## Defaults

- Default to `720p`
- Default to `5` seconds
- Prefer a concise cinematic prompt over a long generic paragraph
- If the user provides only a topic, prepare the prompt first before generation

## Workflow

1. Decide whether prompt preparation is needed.
   - If the user already provides a finalized prompt, keep it.
   - If the user provides only a topic or rough idea, use `scripts/optimize_prompt.py` first.
2. Prepare the prompt.
   - Use the cinematic formula in `references/prompt-formula.md`.
   - Use `references/prompt-template.txt` as a starting scaffold when needed.
3. Run the generator from the skill root.
   - Use `python3 scripts/generate_video.py ...`
   - Read `references/execution.md` for command patterns.
4. Inspect the result.
   - Confirm task submission succeeded.
   - If not using `--dry-run`, confirm the output video was downloaded.

## Constraints

- This skill is specific to Seedance 3.0 720p on Volcengine.
- It requires `VOLC_ACCESSKEY` and `VOLC_SECRETKEY`.
- It is optimized for short clips, not long-form video assembly.
- Prompt preparation should improve visual specificity, not add filler.

## Bundled resources

- `scripts/generate_video.py`: Submit, poll, and download Seedance video generation results.
- `scripts/optimize_prompt.py`: Expand a topic into a structured prompt scaffold.
- `references/prompt-formula.md`: Prompt construction guidance.
- `references/execution.md`: Command patterns and failure handling.
