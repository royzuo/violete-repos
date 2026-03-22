# Seedance Execution

Use this reference when you are ready to run the skill or when generation fails.

## Preconditions

- `VOLC_ACCESSKEY` must be set
- `VOLC_SECRETKEY` must be set
- Run commands from the `bytedance-seedance-2-fast/` skill root

## Command patterns

Prepare a prompt from a topic:

```bash
python3 scripts/optimize_prompt.py "The Terracotta Army"
```

Text-to-video:

```bash
python3 scripts/generate_video.py --prompt "Slow tracking shot of terracotta warriors in a dim underground chamber, dust in the air, warm torchlight, cinematic realism" --output terracotta.mp4
```

Image-guided video:

```bash
python3 scripts/generate_video.py --prompt "The girl smiles softly as the camera pushes in" --image first.jpg --output clip.mp4
```

Start and end frame guidance:

```bash
python3 scripts/generate_video.py --prompt "Spring gradually transforms into autumn" --image spring.jpg --end-image autumn.jpg --duration 10 --output seasons.mp4
```

Dry run the request payload without calling the API:

```bash
python3 scripts/generate_video.py --prompt "A tiger walks through neon rain" --dry-run
```

## Output handling

- On success, the script prints `task_id=...`, `video_url=...`, and `output_file=...`
- `--dry-run` prints the request payload and exits

## Failure triage

- Missing credentials: set `VOLC_ACCESSKEY` and `VOLC_SECRETKEY`
- Signature errors: inspect auth-related API responses
- Timeout: rerun or increase wait tolerance in the script if needed
- Download failure: verify the returned video URL is reachable
