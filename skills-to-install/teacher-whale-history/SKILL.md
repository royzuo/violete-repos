---
name: teacher-whale-history
description: Build or maintain a chapter or section briefing bundle for 《鲸鱼老师讲历史.中国史特辑》 by collecting evidence for the requested chapter, organizing a research brief, and producing the aligned briefing card, Gamma PDF/JPG exports, article, talk script, and video prompts under `scripts/<bundle-id>/`.
---

# Teacher Whale History

Use this skill for the series-specific workflow that turns one input chapter or section into an evidence-backed briefing bundle.

## Goal

For one requested chapter, section, or summary bundle:

- collect and organize the relevant evidence first
- build a structured chapter brief from that evidence
- produce four aligned content outputs:
  - `briefing-card.md`
  - `video-article.md`
  - `talkshow-script.md`
  - `video-prompts.md`
- export the Gamma briefing bundle to PDF and JPG pages

## Use this skill when

- Roy asks for a new chapter or section bundle in the Teacher Whale history series
- an existing bundle needs to be continued, fixed, regenerated, audited, or exported
- the task is not just Gamma generation, but the full chapter-brief production workflow

## Inputs to gather

- The target chapter, section, or bundle id
- The intended folder under `scripts/`
- The core question or thesis the chapter brief should answer
- Any explicit evidence, claims, or framing constraints from Roy
- Whether Gamma export and Git publishing are needed in this run

## Defaults

- Preserve or create work under `scripts/<bundle-id>/`
- Treat the chapter brief as evidence-backed, not purely generative writing
- Keep the host persona as `鲸鱼老师`
- Let the evidence chain decide the content-card count. Most chapters land well with 5 to 8 content cards plus an optional cover block, but do not force a fixed number.
- Keep Gamma output in `social` format with an explicit `themeId`
- Use `references/output-quality.md` as the primary quality bar. A local finished bundle can be inspected as an optional sense check, not as a required dependency.
- Do not commit or push unless Roy explicitly asks

## Workflow

1. Resolve the target bundle.
   - If the bundle already exists under `scripts/<bundle-id>/`, inspect it first.
   - If it does not exist, initialize it with `scripts/init_bundle.py`.
2. Build the evidence base before drafting.
   - Read `references/research-contract.md`.
   - Read `references/delivery-contract.md`.
   - Read `references/output-quality.md`.
   - Read `program-outlines/archaeology-program-renjiao-outline.md` when the outline helps scope the chapter.
   - Use `scripts/harvest_sources.py` when you want to seed candidate links into the bundle quickly.
   - The harvesting helper should use `web-hybrid-search`, not a single-provider search path.
   - Maintain `chapter-brief.md` and `sources.json` inside the bundle.
3. Draft the four aligned outputs.
   - Use the same evidence chain across `briefing-card.md`, `video-article.md`, `talkshow-script.md`, and `video-prompts.md`.
   - Derive the card or section count from the actual material density and narrative closure, then keep all four outputs aligned to that same plan.
   - Keep claims traceable to the source ledger.
   - When historical interpretation is contested, prefer cautious mainstream archaeological framing.
   - For `briefing-card.md`, think in terms of card logic, not prose overflow. Each card should land one strong idea with concise bullets.
   - For `talkshow-script.md`, write a real spoken monologue, not outline notes or bullet expansions.
   - For `video-prompts.md`, write production-usable English prompts so the same clip plan can serve both Chinese and English programs.
   - Each video prompt must correspond to the explanatory job of its matching card. Do not describe the topic in the abstract; visualize that card's specific argument step, evidence point, mechanism, or conclusion.
   - Prefer Seedance-style one-shot prompts built from camera, subject, action, atmosphere, lighting, and a few concise quality tags.
   - For `video-article.md`, write a knowledge-rich article with structured exposition, not just the card bullets pasted longer.
   - Use richer knowledge presentation when it helps: tables, mermaid diagrams, mind maps, sourced images, formulas, code or schema snippets. The article should carry the detailed scientific and historical explanation that the cards and spoken script cannot fully unpack.
4. Export Gamma artifacts when needed.
   - Use `scripts/export_gamma_social_bundle.sh <bundle_dir>/briefing-card.md [theme-id]`.
   - This should produce `briefing-card.pdf` and `briefing-card_jpg/*.jpg`.
5. Validate the bundle before handoff.
   - Run `python3 scripts/validate_bundle.py --bundle-id <bundle-id>`.
   - Use `--require-exports` when PDF/JPG output is expected in the current run.
   - Use `--strict-support` when you want missing research artifacts to fail validation.
6. Publish only on request.
   - If Roy asks to commit or push, use `scripts/publish_episode.sh`.

## Constraints

- This skill is specific to 《鲸鱼老师讲历史.中国史特辑》.
- The skill is responsible for evidence collection and chapter-brief correctness, not just final formatting.
- Gamma is a downstream export step, not the source of truth for the content.
- The bundled validation script is the source of truth for structural checks.

## Bundled resources

- `scripts/init_bundle.py`: Scaffold a new chapter bundle with the required working files.
- `scripts/harvest_sources.py`: Gather candidate source links for one bundle with targeted queries via `web-hybrid-search`.
- `scripts/validate_bundle.py`: Validate bundle completeness, structure, and export presence.
- `scripts/export_gamma_social_bundle.sh`: Export `briefing-card.md` via Gamma and split JPG pages.
- `scripts/publish_episode.sh`: Optional git helper for publishing a finished bundle.
- `references/research-contract.md`: Source ledger and evidence-brief requirements.
- `references/delivery-contract.md`: Folder layout and output contract.
- `references/output-quality.md`: Output quality bar expressed as reusable heuristics instead of a fixed sample.
- `references/execution.md`: Command patterns for setup, validation, export, and publishing.
