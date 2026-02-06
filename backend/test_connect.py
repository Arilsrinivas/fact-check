import requests
import sys

try:
    print("Testing GET / ...")
    r = requests.get("http://localhost:8000/")
    print(f"Root status: {r.status_code}")

    print("\nFetching OpenAPI Schema...")
    r = requests.get("http://localhost:8000/openapi.json")
    if r.status_code == 200:
        data = r.json()
        print("Registered Paths:")
        for path, methods in data.get("paths", {}).items():
            print(f" - {path} {list(methods.keys())}")
    else:
        print("Could not fetch openapi.json")

    print("\nTesting POST /api/claims/analyze ...")
    payload = {"text": "Test claim connectivity"}
    # Note: We need to match the Pydantic schema
    r = requests.post("http://localhost:8000/api/claims/analyze", json=payload)
    print(f"Analyze status: {r.status_code}")
    if r.status_code != 200:
        print(r.text)
    else:
        print("Success! Connectivity confirmed.")
except Exception as e:
    print(f"CONNECTION FAILED: {e}")
    sys.exit(1)
