
import requests
import json

def test_gp_json():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    })
    
    query = "biodiesel production from waste oil"
    # Testing a known XHR/JSON endpoint pattern for Google Patents
    url = "https://patents.google.com/xhr/query"
    params = {
        "url": f"q=({query})",
        "exp": ""
    }
    
    print(f"Testing URL: {url} with params: {params}")
    try:
        response = session.get(url, params=params, timeout=15)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Successfully parsed JSON!")
            print(f"Results keys: {data.keys()}")
            if 'results' in data and 'cluster' in data['results']:
                results = data['results']['cluster'][0]['result']
                print(f"Found {len(results)} results in JSON.")
                for r in results[:2]:
                    print(f"Patent: {r['patent']['publication_number']}")
        else:
            print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_gp_json()
