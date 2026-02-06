from ddgs import DDGS
import datetime

class OSINTService:
    def __init__(self):
        self.ddgs = DDGS()

    def search_claim(self, query: str, max_results=10):
        print(f"--- START SEARCH: {query} ---")
        results = []
        
        # 1. Try DuckDuckGo
        try:
            from ddgs import DDGS
            with DDGS() as ddgs:
                search_gen = ddgs.text(query, max_results=max_results)
                for r in search_gen:
                    results.append({
                        "title": r.get("title"),
                        "url": r.get("href"),
                        "snippet": r.get("body"),
                        "domain": r.get("href", "").split("/")[2] if r.get("href") else "unknown",
                        "published_at": None,
                        "source_type": "web"
                    })
        except Exception as e:
            print(f"DDGS Warning: {e}")

        # 2. Key Fallback: Wikipedia (Great for general knowledge/facts)
        if not results:
            print("--- DDG Failed. Trying Wikipedia ---")
            try:
                import wikipedia
                # Search for pages
                wiki_pages = wikipedia.search(query, results=3)
                for page_title in wiki_pages:
                    try:
                        page = wikipedia.page(page_title, auto_suggest=False)
                        results.append({
                            "title": f"Wikipedia: {page.title}",
                            "url": page.url,
                            "snippet": page.summary[:300] + "...",
                            "domain": "wikipedia.org",
                            "published_at": None,
                            "source_type": "encyclopedia"
                        })
                    except:
                        continue
            except Exception as e:
                 print(f"Wikipedia Warning: {e}")

        # 3. Fallback: Google Search (Scraper)
        if not results:
             print("--- Wikipedia Failed. Trying Google Scraper ---")
             try:
                 from googlesearch import search
                 # output of search() is URLs
                 for url in search(query, stop=5, pause=2.0):
                     results.append({
                         "title": "Google Result",
                         "url": url,
                         "snippet": "Result found via Google Search fallback.",
                         "domain": url.split("/")[2] if len(url.split("/")) > 2 else "unknown",
                         "published_at": None, 
                         "source_type": "web_fallback"
                     })
             except Exception as e:
                 print(f"Google Warning: {e}")

        print(f"--- END SEARCH: Found {len(results)} results ---")
        return results

osint_service = OSINTService()
