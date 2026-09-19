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

## `chapter-brief.md` minimum sections

Keep these headings:

- `## 输入章节`
- `## 核心问题`
- `## 核心结论`
- `## 证据链`
- `## 争议与边界`
- `## 卡片规划`
- `## 输出计划`

## `sources.json` preferred shape

```json
{
  "bundle_id": "ep06",
  "topic": "第06讲｜大汉气象——丝路起点与西域往事",
  "sources": [
    {
      "title": "悬泉置遗址相关研究",
      "url": "https://example.com",
      "source_type": "paper",
      "claim_supported": "悬泉置承担驿传与接待功能",
      "notes": "用于支撑第二卡和正文第二部分",
      "confidence": "high"
    }
  ]
}
```

## Source selection rules

- Prefer museum, excavation report, academic publication, major reference work, or high-quality institutional source.
- Use popular articles only as secondary orientation, not as the sole factual support.
- Keep one source item per distinct evidence use when possible.
- Record caution notes when a source is interpretive, dated, or disputed.

## Evidence handling rules

- Every major claim in the final bundle should be supported by at least one source entry.
- If a claim is uncertain, keep that uncertainty visible in `chapter-brief.md`.
- Avoid turning contested identity, ethnicity, or civilizational claims into absolute statements.
- Before drafting the final outputs, map the evidence chain into a card plan inside `chapter-brief.md`. Most chapters will need 5 to 8 content cards, but the count should come from the material rather than from a fixed template.
