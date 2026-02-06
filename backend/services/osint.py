from duckduckgo_search import DDGS
import datetime

class OSINTService:
    def __init__(self):
        self.ddgs = DDGS()

    def search_claim(self, query: str, max_results=10):
        print(f"--- START SEARCH: {query} ---")
        results = []
        try:
            # Use context manager for better session handling
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                # text() returns a generator
                search_gen = ddgs.text(query, max_results=max_results)
                for r in search_gen:
                    print(f"Found match: {r.get('title')[:30]}...")
                    results.append({
                        "title": r.get("title"),
                        "url": r.get("href"),
                        "snippet": r.get("body"),
                        "domain": r.get("href", "").split("/")[2] if r.get("href") else "unknown",
                        "published_at": None 
                    })
        except Exception as e:
            print(f"!!! OSINT ERROR: {e}")
        
        print(f"--- END SEARCH: Found {len(results)} results ---")
        return results

osint_service = OSINTService()
