import requests

# Yelp
YELP_SEARCH_URL = "https://api.yelp.com/v3/businesses/search"

yelp_headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {'9W3Ud31Ji8Kpg5dC3iufULCUIiMoggC9VrpbC36s-eyL1KNmUSW7YwaptH-erVWJwd5vVEH8NbZWjJJJuYlLQx97jgowRSQF0oRDlOIPPYe3kb_GWp7C5WutYD42ZXYx'}"
}
yelp_params = {
    'latitude': 47.606,
    'longitude': -122.349358,
    'categories': 'restaurants,bars',
    'limit': 1
}
yelp_response = requests.get(YELP_SEARCH_URL, headers=yelp_headers, params=yelp_params)

print(yelp_response.json())
