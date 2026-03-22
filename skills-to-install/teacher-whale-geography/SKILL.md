---
name: teacher-whale-geography
description: Build or maintain a chapter or section briefing bundle for 《鲸鱼老师讲地理》 by grounding the requested section in the program brief or outline, collecting evidence, organizing a research brief, and producing the aligned briefing card, Gamma PDF/JPG exports, article, talk script, and video prompts under `scripts/<bundle-id>/`.
---

# Teacher Whale Geography

Use this skill for the series-specific workflow that turns one geography chapter, section, or wonder topic into an evidence-backed briefing bundle.

## Goal

For one requested geography chapter, section, wonder topic, or bundle:

- resolve the requested section or topic first
- collect and organize the relevant evidence
- build a structured briefing brief from that evidence
- produce four aligned content outputs:
  - `briefing-card.md`
  - `video-article.md`
  - `talkshow-script.md`
  - `video-prompts.md`
- export the Gamma briefing bundle to PDF and JPG pages

## Use this skill when

- Roy asks for a new geography chapter, section, or wonder bundle in the Teacher Whale geography series
- an existing bundle needs to be continued, fixed, regenerated, audited, or exported
- the task is not just Gamma generation, but the full geography-brief production workflow

## Inputs to gather

- The target chapter, section, wonder, region, theme, or bundle id
- The intended folder under `scripts/`
- The core geographic question or narrative hook the brief should answer
- Any explicit evidence, claims, or framing constraints from Roy
- Whether Gamma export and Git publishing are needed in this run

## Defaults

- Preserve or create work under `scripts/<bundle-id>/`
- Treat the brief as evidence-backed, not purely generative writing
- Keep the host persona as `鲸鱼老师`
- Let the evidence chain and teaching arc decide the content-card count. Most geography bundles land well with 5 to 8 content cards plus an optional cover block, but do not force a fixed number.
- Keep Gamma output in `social` format with an explicit `themeId`
- Use `references/briefing-guide.md` as the geography-specific narrative guide and `references/output-quality.md` as the production quality bar.
- If a program outline or briefing file exists, use it to scope the section first. In the current repo, `program-outlines/geography-program-water-epic-outline.md` is the main season outline and `prompts/geography_briefing.txt` is the supporting briefing source.
- Do not commit or push unless Roy explicitly asks

## Workflow

1. Resolve the target bundle.
   - If the bundle already exists under `scripts/<bundle-id>/`, inspect it first.
   - If it does not exist, initialize it with `scripts/init_bundle.py`.
   - If Roy gives a chapter or section from a program outline or briefing file, anchor the bundle to that section instead of inventing a fresh topic.
2. Build the evidence base before drafting.
   - Read `references/research-contract.md`.
   - Read `references/delivery-contract.md`.
   - Read `references/briefing-guide.md`.
   - Read `references/output-quality.md`.
   - Use `scripts/harvest_sources.py` when you want to seed candidate links into the bundle quickly.
   - Maintain `chapter-brief.md` and `sources.json` inside the bundle.
   - If the section is not fully specified yet, prefer topics with strong uniqueness, scientific relevance, visual teachability, and discussion value. Recent news and unresolved mysteries are priority boosters.
3. Draft the four aligned outputs.
   - Use the same evidence chain across `briefing-card.md`, `video-article.md`, `talkshow-script.md`, and `video-prompts.md`.
   - Derive the card or section count from the actual material density and narrative closure, then keep all four outputs aligned to that same plan.
   - Keep claims traceable to the source ledger.
   - Keep the main content arc aligned to the geography logic of the section: what this place or system is, where it sits, how it formed, how human and natural systems interact there, and what challenges or futures matter now.
   - Add interaction prompts near the opening and closing when the topic supports it.
   - For `briefing-card.md`, think in terms of card logic, not prose overflow. Each card should land one strong geographic idea with concise bullets.
   - For `talkshow-script.md`, write a real spoken monologue, not outline notes or bullet expansions.
   - For `video-prompts.md`, write production-usable English prompts so the same clip plan can serve both Chinese and English programs.
   - Each video prompt must correspond to the explanatory job of its matching card. Do not describe the topic in the abstract; visualize that card's specific evidence point, process, system relation, challenge, or conclusion.
   - Prefer Seedance-style one-shot prompts built from camera, subject, action, atmosphere, lighting, and a few concise quality tags.
   - For `video-article.md`, write a knowledge-rich article that carries the scientific, spatial, ecological, and human-geography detail that would overload the cards or spoken script. Use tables, mermaid diagrams, sourced images, mind maps, formulas, or compact code or schema blocks when they improve clarity.
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

- This skill is specific to 《鲸鱼老师讲地理》.
- The skill is responsible for evidence collection and brief correctness, not just final formatting.
- Gamma is a downstream export step, not the source of truth for the content.
- The bundled validation script is the source of truth for structural checks.

## Bundled resources

- `scripts/init_bundle.py`: Scaffold a new geography bundle with the required working files.
- `scripts/harvest_sources.py`: Gather candidate source links for one bundle with targeted queries via `web-hybrid-search`.
- `scripts/validate_bundle.py`: Validate bundle completeness, structure, and export presence.
- `scripts/export_gamma_social_bundle.sh`: Export `briefing-card.md` via Gamma and split JPG pages.
- `scripts/publish_episode.sh`: Optional git helper for publishing a finished bundle.
- `references/research-contract.md`: Source ledger and evidence-brief requirements.
- `references/delivery-contract.md`: Folder layout and output contract.
- `references/briefing-guide.md`: Geography-specific topic selection, structure, interaction, and video-prompt requirements.
- `references/output-quality.md`: Output quality bar expressed as reusable heuristics instead of a fixed sample.
- `references/execution.md`: Command patterns for setup, validation, export, and publishing.
