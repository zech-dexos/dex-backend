import requests

TOOL_NAME = "search"
TRIGGERS = ["search", "look up", "find", "what is", "who is", "where is", "when is", "how do", "what are", "weather", "news"]

def run(query: str) -> str:
    try:
        clean = query.lower()
        for t in TRIGGERS:
            clean = clean.replace(t, "").strip()
        
        url = f"https://api.duckduckgo.com/?q={requests.utils.quote(clean)}&format=json&no_redirect=1&no_html=1"
        r = requests.get(url, timeout=8)
        data = r.json()
        
        abstract = data.get("AbstractText", "")
        if abstract:
            return abstract[:300]
        
        related = data.get("RelatedTopics", [])
        if related and isinstance(related[0], dict):
            return related[0].get("Text", "")[:300]
        
        return ""
    except Exception as e:
        return ""
