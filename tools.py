import requests
from urllib.parse import quote
import re

def search_web(query: str, max_results: int = 3) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        # Hit the static HTML endpoint
        url = f"https://duckduckgo.com/html/?q={quote(query)}"
        r = requests.get(url, headers=headers, timeout=8)
        
        # FIX: Catch everything inside the result__snippet container dynamically
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</div>', r.text, re.DOTALL)
        
        # If DuckDuckGo uses table cells instead of divs in your region, this fallback catches it:
        if not snippets:
            snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</td|div|a>', r.text, re.DOTALL)

        # Clean HTML tags out of the extracted snippets
        clean = [re.sub(r'<.*?>', '', s).strip() for s in snippets[:max_results]]
        
        # Reformat whitespace and breaks
        clean = [re.sub(r'\s+', ' ', s) for s in clean if s]
        
        return "\n\n".join(clean) if clean else "No structural snippets found in page parsing."
    except Exception as e:
        return f"Search error: {e}"
