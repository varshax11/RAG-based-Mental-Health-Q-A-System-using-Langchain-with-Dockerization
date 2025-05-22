import requests

url = "http://127.0.0.1:8000/query"
payload = {
    "query": "what self care to do to reduce stress?"
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("Response from RAG system:")
    print(response.json()["response"])
else:
    print("Error:")
    print(response.status_code, response.text)
