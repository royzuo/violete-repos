# Output Quality Bar

Use this reference before drafting `briefing-card.md`, `talkshow-script.md`, `video-prompts.md`, or `video-article.md`.

## Working principle

Do not rely on a fixed sample bundle to complete the skill. If the repo later contains a strong geography sample bundle, you may inspect it as a secondary sense check. The primary bar is the quality contract below.

## `briefing-card.md`

Target shape:

- One title block:
  - `# 《鲸鱼老师讲地理》`
  - `副标题：...`
- Then 4 to 8 content cards in most cases, chosen from the teaching density and narrative needs
- Every card starts with `# 卡片X｜...`
- Every card should usually contain 3 to 5 concise bullets, with 4 as the normal target

Quality rules:

- The first content card should pose the real geographic question, break a naive impression, and name the evidence chain.
- The middle cards should each advance one major explanatory step: spatial setting, formation process, system relation, comparison, challenge, or future.
- The final content card should compress the conclusion into a memorable synthesis or close with a strong question.
- Do not turn one card into a wall of prose.
- Use a line containing only `---` between the title block and each card block.

## `talkshow-script.md`

Target shape:

- One H1 title that signals this is a spoken script
- One `## 卡片 ...` section per content card, aligned to the briefing-card plan
- Card 1 opens with `大家好，我是鲸鱼老师！`
- Each card section should be real spoken paragraphs, not placeholder bullets

Quality rules:

- The script should sound like a recordable monologue, not like notes being read aloud.
- Each card should explain one geographic step and naturally bridge to the next.
- Prefer concrete geographic processes, scales, and examples over travel-copy hype.
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
- Each prompt must visualize the same explanatory step as its matching card. Card 1 should visualize the question, middle cards should visualize formation, spatial relations, human-earth interaction, or challenge, and the final card should visualize the conclusion or synthesis.
- Prefer the Seedance-style formula: camera + subject + action + atmosphere + lighting + concise quality tags.
- Include subject, setting, motion, atmosphere, lighting, and material or terrain texture when relevant.
- Keep each duration at 15 seconds or less.
- Avoid prompts that could fit any geography episode. The shot should feel inseparable from that card's explanation.

## `video-article.md`

Target shape:

- One H1 title
- Greeting paragraph after the title
- One H2 section per major content step, normally aligned to the card plan
- Optional summary or navigation section such as `## 一眼读懂`
- End matter that signals the evidence basis

Quality rules:

- This should read like a standalone knowledge article, not like card notes pasted together.
- The article should expand the evidence chain with more explanation, comparison, interpretation, and scale awareness.
- It should be legible even if the reader has not seen the cards.
- It should preserve caution where evidence is limited, debated, or changing.
- Prefer mixed knowledge presentation over pure prose when useful: tables, mermaid diagrams, maps, sourced images, formulas, or compact code or schema blocks.
- The article should carry the scientific, ecological, spatial, and human-geography detail that is too dense for the briefing card or spoken script.

## Common failure modes to avoid

- Briefing card count is copied from a template instead of being derived from the actual section
- Cards become tourism copy instead of geographic explanation
- Talkshow script reads like an outline instead of a spoken performance
- Video prompts look cinematic but do not actually match what the corresponding card is explaining
- Article repeats the card bullets with no added explanation
- Article stays as plain prose even when the topic clearly needs tables, diagrams, comparisons, or map-like structure
- Claims appear in outputs without support in `sources.json` or `chapter-brief.md`
