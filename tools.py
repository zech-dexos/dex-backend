import requests

def search_web(query: str, max_results: int = 3) -> str:
    try:
        url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
        r = requests.get(url, params=params, timeout=5)
        data = r.json()
        results = []
        if data.get("AbstractText"):
            results.append(data["AbstractText"])
        for topic in data.get("RelatedTopics", [])[:max_results]:
            if "Text" in topic:
                results.append(topic["Text"])
        return "\n".join(results) if results else "No results found."
    except Exception as e:
        return f"Search error: {e}"
