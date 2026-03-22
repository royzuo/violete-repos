---
name: web-hybrid-search
description: Run hybrid web search across SearchCans and Linkup, merge the results, and deduplicate them into one ranked result set. Use when the user needs broader coverage than a single provider, especially for link discovery and current web research with SEARCHCANS_API_KEY or LINKUP_API_KEY.
---

# Web Hybrid Search

Use this skill when you want one combined result set from multiple web search providers instead of relying on a single API.

## Use this skill when

- The user wants broad web coverage for a topic.
- You want URL discovery from SearchCans plus complementary results from Linkup.
- One provider may miss useful results and you want a merged ranked set.
- You need a saved JSON output for downstream processing.

## Inputs to gather

- Search query
- Desired result count
- Whether to save JSON output to disk
- Whether broad coverage matters more than low latency

## Defaults

- Try SearchCans and Linkup in parallel when both keys are available.
- If only one provider key is available, still return that provider's results.
- Deduplicate by URL first, then by near-duplicate titles.
- Prefer returning a clean merged set over exhaustively preserving duplicates.

## Workflow

1. Check available providers.
   - `SEARCHCANS_API_KEY`
   - `LINKUP_API_KEY`
2. Run the bundled script from the skill root.
   - Use `python3 scripts/hybrid_search.py --query "..."`
3. Inspect the merged result set.
   - Confirm which providers were used.
   - Confirm result count after deduplication.
4. Continue with downstream summarization or URL fetching.

## Constraints

- The bundled script currently merges SearchCans and Linkup only.
- If both providers are unavailable, the script should fail clearly.
- Built-in platform web tools can still be used manually outside this script, but they are not part of the current bundled implementation.

## Bundled resources

- `scripts/hybrid_search.py`: Parallel hybrid search runner with deduplication.
- `references/execution.md`: Command patterns, output shape, and failure handling.
- `references/strategy.md`: Practical guidance for provider combination and result interpretation.
