import requests

# Search eBay for a book
url = "https://api.ebay.com/buy/browse/v1/item_summary/search"

params = {
    "q": "Harry Potter and the Philosopher's Stone",
    "limit": 5
}

headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "X-EBAY-C-MARKETPLACE-ID": "EBAY_DE"
}

response = requests.get(url, params=params, headers=headers)

print(response.status_code)

data = response.json()

for item in data.get("itemSummaries", []):
    print(item["title"])
    print(item["price"]["value"], item["price"]["currency"])
    print(item["itemWebUrl"])