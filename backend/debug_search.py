from services.osint import osint_service
import json

def test_search():
    query = "Python programming language released 1991"
    print(f"Testing search for: '{query}'")
    
    results = osint_service.search_claim(query, max_results=5)
    
    print(f"\nResults found: {len(results)}")
    if results:
        print(json.dumps(results, indent=2, default=str))
    else:
        print("No results found. Possible blocking or API change.")

if __name__ == "__main__":
    test_search()
