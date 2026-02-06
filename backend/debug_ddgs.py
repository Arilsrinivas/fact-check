from ddgs import DDGS
import json

def test_search(query):
    print(f"\n--- Testing Query: '{query}' ---")
    try:
        with DDGS() as ddgs:
            # Try to fetch 5 results
            results = list(ddgs.text(query, max_results=5))
            print(f"Status: Success | Count: {len(results)}")
            if results:
                print(f"Top Result: {results[0].get('title')} ({results[0].get('href')})")
            else:
                print("Status: Empty Response (No results found)")
    except Exception as e:
        print(f"Status: ERROR | Message: {str(e)}")

if __name__ == "__main__":
    test_search("Elon Musk acquired Twitter")
    test_search("Python 3.14 release date")
    test_search("Moon is made of cheese")
