# Teacher Whale Geography Delivery Contract

Use this contract for every geography chapter, section, or wonder bundle in 《鲸鱼老师讲地理》.

## Preferred folder layout

```text
scripts/<bundle-id>/
  chapter-brief.md
  sources.json
  briefing-card.md
  briefing-card.pdf
  briefing-card_jpg/*.jpg
  video-article.md
  talkshow-script.md
  video-prompts.md
```

## Bundle contract

- `chapter-brief.md` is the working research brief for the bundle.
- `sources.json` is the source ledger that supports factual claims.
- `briefing-card.md` is the Gamma source of truth for the visual briefing.
- `video-article.md`, `talkshow-script.md`, and `video-prompts.md` must all follow the same evidence chain.
- `briefing-card.pdf` and `briefing-card_jpg/*.jpg` are downstream exports, not the authoring source.

## Briefing-card rules

- Keep one optional cover block at the top.
- Decide the content-card count from the section's material density and narrative needs. In most cases, 5 to 8 content cards is the right range.
- Use explicit `---` separators between cards.
- Each content card should map to one content step in the geography narrative.
- Each content card should usually contain 3 to 5 concise bullets, not prose paragraphs.
- The first card should define the real question and evidence chain.
- The final card should compress the conclusion into a memorable synthesis.

## Talkshow-script rules

- Open with `大家好，我是鲸鱼老师！`
- Keep one `## 卡片 ...` section per content card.
- Use spoken language, but do not add claims that are absent from the research brief.
- Keep the script concise enough for short-form delivery, but do not force an exact runtime mention inside the text.
- End with a closing line or CTA that matches the bundle topic.

## Video-article rules

- Keep one clear H1 title.
- Keep a long-form explanatory structure, not a bullet dump.
- Make the evidence chain legible to a reader who has not seen the briefing card.
- Keep H2 sections aligned to the card logic instead of forcing a fixed count.
- Use tables, mermaid diagrams, sourced images, mind maps, formulas, or compact code or schema blocks when they improve knowledge delivery.
- Let the article absorb the dense explanatory content that would overload the card deck or spoken script.
- End with a short source note that signals the evidence basis.

## Video-prompts rules

- Provide one prompt block per content card.
- Each prompt block should include a prompt body and a duration.
- Keep the prompt body in English only.
- Use English because the same visual plan should be reusable in both Chinese and English program versions.
- Keep each clip at 15 seconds or less.
- Make each prompt directly generation-ready with subject, scene, camera, motion, and texture.
- Make each prompt correspond to the matching card's explanation, not just the bundle topic. A viewer should be able to tell which card the shot belongs to.
- Prefer the Seedance-style structure: camera + subject + action + atmosphere + lighting + concise quality tags.
- Keep the visual language geographic, scientific, and cinematic rather than fantastical.

## Quality bar

- Prefer geoscience, ecology, cartography, field-observation, and source-aware wording over travel-copy hype.
- Separate measured facts, scientific interpretation, and media-friendly simplification.
- When a claim is controversial or unresolved, express the uncertainty clearly.
- Do not auto-publish by default. Publishing is a separate explicit step.
