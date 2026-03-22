# Research Contract

Use this reference before drafting the final bundle outputs.

## Working files

Every new or refreshed bundle should maintain:

- `chapter-brief.md`
- `sources.json`
- `source-candidates.json` when you run the harvesting helper

These are support artifacts for correctness. They are not the public-facing outputs, but the final outputs should be traceable back to them.

## Candidate harvesting

If you need a quick starting pool of links, run `scripts/harvest_sources.py` with targeted chapter queries.

- Treat `source-candidates.json` as a discovery artifact, not the final source ledger.
- Curate the useful items into `sources.json`.
- Discard weak media rewrites, duplicate URLs, and low-authority pages.
- The harvesting helper uses `web-hybrid-search`; inspect the recorded `runs` in `source-candidates.json` when a query underperforms.
- Prefer query sets that cover wonder uniqueness, location, formation, geographic significance, current threats, sustainability, recent news, and unresolved mysteries.

## `chapter-brief.md` minimum sections

Keep these headings:

- `## 输入章节 / 选题`
- `## 节目框架映射`
- `## 核心问题`
- `## 核心结论`
- `## 证据链`
- `## 现状、挑战与未解之谜`
- `## 卡片规划`
- `## 输出计划`

## `sources.json` preferred shape

```json
{
  "bundle_id": "nile-delta",
  "topic": "尼罗河三角洲：水的史诗如何塑造文明",
  "sources": [
    {
      "title": "尼罗河三角洲地貌演化研究",
      "url": "https://example.com",
      "source_type": "paper",
      "claim_supported": "三角洲的沉积演化决定了农业与聚落格局",
      "notes": "用于支撑形成过程和地理意义部分",
      "confidence": "high"
    }
  ]
}
```

## Source selection rules

- Prefer geoscience institution, scientific paper, observatory, government survey, museum, UNESCO, national park, or high-quality institutional source.
- Use mainstream media and popular science articles as secondary orientation, not as the sole factual support.
- Keep one source item per distinct evidence use when possible.
- Record caution notes when a source is interpretive, dated, or disputed.
- If the wonder has important news within the last three days, include at least one news entry in the ledger.

## Evidence handling rules

- Every major claim in the final bundle should be supported by at least one source entry.
- If a claim is uncertain, keep that uncertainty visible in `chapter-brief.md`.
- Avoid turning unresolved formation debates, climate attributions, or human-impact claims into absolute statements.
- Before drafting the final outputs, map the evidence chain into a card plan inside `chapter-brief.md`. Most geography bundles will need 5 to 8 content cards, but the count should come from the material rather than from a fixed template.
