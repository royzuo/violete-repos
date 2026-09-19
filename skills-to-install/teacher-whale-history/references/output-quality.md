# Output Quality Bar

Use this reference before drafting `briefing-card.md`, `talkshow-script.md`, `video-prompts.md`, or `video-article.md`.

## Working principle

Do not rely on a fixed sample bundle to complete the skill. If the repo happens to contain a mature local bundle that is close to the target topic, you may inspect it as a secondary sense check. The primary bar is the quality contract below.

## `briefing-card.md`

Target shape:

- One title block:
  - `# 《鲸鱼老师讲历史系列.中国通史特辑》`
  - `副标题：...`
- Then 4 to 8 content cards in most cases, chosen from the evidence density and narrative needs
- Every card starts with `# 卡片X｜...`
- Every card should usually contain 3 to 5 concise bullets, with 4 as the normal target

Quality rules:

- The first content card should pose the real problem, break the naive impression, and name the evidence chain.
- The middle cards should each advance one key evidence step, mechanism step, or interpretation move.
- The final content card should compress the conclusion into a memorable synthesis or close with a strong question.
- Do not write essay paragraphs inside cards.
- Do not let one card absorb the whole argument.
- Use a line containing only `---` between the title block and each card block.

## `talkshow-script.md`

Target shape:

- One H1 title that signals this is a deep spoken script
- One `## 卡片 ...` section per content card, aligned to the briefing-card plan
- Card 1 opens with `大家好，我是鲸鱼老师！`
- Each card section should be real spoken paragraphs, not placeholder bullets

Quality rules:

- The script should feel like a coherent monologue that can be recorded directly.
- Each card should explain one step and naturally bridge to the next.
- Prefer concrete archaeological evidence, not abstract textbook slogans.
- The final card should end with either a CTA, a comment prompt, or a next-episode bridge.

## `video-prompts.md`

Target shape:

- One `## Video ...` block per content card, aligned to the same narrative plan
- Every block contains:
  - `**Prompt**: ...`
  - `**Duration**: ...`

Quality rules:

- Prompt text should be English only.
- Prompts should be directly usable for video generation.
- Each prompt must visualize the same argumentative step as its matching card. Card 1 should visualize the question, middle cards should visualize evidence or mechanism, and the final card should visualize the conclusion or synthesis.
- Prefer the Seedance-style formula: camera + subject + action + atmosphere + lighting + concise quality tags.
- Include subject, setting, motion, lighting, atmosphere, and material texture when relevant.
- Keep each duration at 15 seconds or less.
- Avoid generic phrases like "show the scene" or meta-notes like "fill this later".
- Avoid prompts that could fit any card in the episode. The shot should feel inseparable from that card's spoken explanation.

## `video-article.md`

Target shape:

- One H1 title
- Greeting paragraph after the title
- One H2 section per major content step, normally aligned to the card plan
- End matter that signals the evidence basis

Quality rules:

- This should read like a standalone article, not like card notes pasted together.
- The article should expand the evidence chain with more explanation, comparison, and interpretation.
- It should be legible even if the reader has not seen the cards.
- It should preserve caution where evidence is limited or disputed.
- Prefer mixed knowledge presentation over pure prose when useful: tables, mermaid diagrams, mind maps, sourced images, formulas, or compact code or schema blocks.
- The article should carry the scientific, archaeological, and interpretive detail that is too dense for the briefing card or spoken script.

## Common failure modes to avoid

- Briefing card turns into one overloaded page or one long block of prose
- Briefing card count is copied from a template instead of being derived from the actual topic
- Talkshow script reads like an outline instead of a spoken performance
- Video prompts remain half in Chinese, half in notes, and are not generation-ready
- Video prompts look cinematic but do not actually match what the corresponding card is explaining
- Article repeats the card bullets with no added explanation
- Article stays as plain prose even when the topic clearly needs tables, diagrams, timelines, or visual comparison aids
- Claims appear in outputs without support in `sources.json` or `chapter-brief.md`
