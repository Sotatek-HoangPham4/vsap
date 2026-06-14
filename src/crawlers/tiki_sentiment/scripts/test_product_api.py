# scripts/test_product_api.py

import requests

url = "https://tiki.vn/api/personalish/v1/blocks/listings"

params = {
    "category": 320,
    "page": 1,
    "limit": 40,
}

r = requests.get(
    url,
    params=params,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
)

print(r.status_code)
print(r.json().keys())