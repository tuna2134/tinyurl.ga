import requests


r = requests.post("http://localhost:8000/api", json={"url": "https://www.google.com"})
print(r.json())