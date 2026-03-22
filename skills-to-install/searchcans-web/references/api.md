# SearchCans API notes

Endpoints used by this skill:

## POST /api/search
Headers:
- Authorization: Bearer $SEARCHCANS_API_KEY

Body:
- s: query string
- t: engine (e.g., google)
- d: server timeout ms (e.g., 20000)

## POST /api/url
Headers:
- Authorization: Bearer $SEARCHCANS_API_KEY

Body:
- s: URL
- t: "url"
- b: boolean, use browser rendering
- w: wait ms for JS render

Response:
- data.markdown: LLM-ready markdown
