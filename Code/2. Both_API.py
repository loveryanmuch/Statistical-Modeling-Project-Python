import requests
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
foursquare_csv_path = os.path.join(script_dir, 'foursquare_results.csv')
yelp_csv_path = os.path.join(script_dir, 'yelp_results.csv')

YELP_SEARCH_URL = "https://api.yelp.com/v3/businesses/search"
FOURSQUARE_SEARCH_URL = "https://api.foursquare.com/v3/places/search"

# Get Paris network ID
url_networks = "http://api.citybik.es/v2/networks"
response = requests.get(url_networks)
data = response.json()

paris_id = next((network['id'] for network in data['networks'] if network['location']['city'] == 'Paris'), None)

if not paris_id:
    print("Paris not found in the list of networks.")
    exit()

# Paris bike station details
url_paris = f"http://api.citybik.es/v2/networks/{paris_id}"
response_paris = requests.get(url_paris)
data_paris = response_paris.json()
bike_stations = data_paris['network']['stations']
num_stations = len(bike_stations)
foursquare_data = []
yelp_data = []

# Loop through the first 50 bike stations in Paris and gather data from Foursquare and Yelp for each station
for station in range(50):
    station = bike_stations[station % num_stations]
    lat, lon = station['latitude'], station['longitude']  # Define lat and lon here

    # Query Foursquare API for cafes and bars near the current station
    foursquare_params = {
        "query": "cafe,bar",
        "ll": f"{lat},{lon}",
        "open_now": "true",
        "sort":"DISTANCE"
    }

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3Nw/fR0XoqtoRT5LtvGCoAEz1vkHCNj32ho57y6khuzM="
    }

    foursquare_response = requests.request("GET", FOURSQUARE_SEARCH_URL, params=foursquare_params, headers=headers)
    foursquare_response_json = foursquare_response.json()

    # Check if the Foursquare API response has any errors
    if foursquare_response.status_code != 200:
        print(f"Error with Foursquare API request for station at ({lat}, {lon}): {foursquare_response.status_code}")
    
    # Parse the Foursquare API response and extract relevant data
    for result in foursquare_response_json["results"]:
        chain_data = result.get("chains", [])
        if chain_data:
            chain_name = chain_data[0].get("name", "")
        else:
            # If "chains" is empty, fall back to the "name" attribute from the main part of the response
            chain_name = result.get("name", "")
        latitude = result["geocodes"]["main"]["latitude"]
        longitude = result["geocodes"]["main"]["longitude"]
        category_name = result["categories"][0]["name"]

        foursquare_data.append([
            chain_name, latitude, longitude, category_name
        ])

    # Query Yelp API for cafes and bars near the current station
    yelp_headers = {
        "Accept": "application/json",        
        "Authorization": f"Bearer {'9W3Ud31Ji8Kpg5dC3iufULCUIiMoggC9VrpbC36s-eyL1KNmUSW7YwaptH-erVWJwd5vVEH8NbZWjJJJuYlLQx97jgowRSQF0oRDlOIPPYe3kb_GWp7C5WutYD42ZXYx'}"
    }
    yelp_params = {
        'latitude': lat,
        'longitude': lon,
        'categories': 'cafe,bar',
        'limit': 50
    }

    yelp_response = requests.get(YELP_SEARCH_URL, headers=yelp_headers, params=yelp_params).json()

    # Parse the Yelp API response and extract relevant data
    for business in yelp_response.get('businesses', []):
        yelp_data.append([
            business['name'],
            business['coordinates']['latitude'],
            business['coordinates']['longitude'],
            business['review_count'],
            business['rating'],
            business.get('categories', [{}])[0].get('title', '')
        ])

    # Convert lists to pandas DataFrames and save them
    df_foursquare = pd.DataFrame(foursquare_data, columns=['Name', 'Latitude', 'Longitude', 'Category'])
    df_yelp = pd.DataFrame(yelp_data, columns=['Name', 'Latitude', 'Longitude', 'Review Count', 'Rating', 'Category'])
    # append them to CSV files
    with open(foursquare_csv_path, 'a') as f:
        df_foursquare.to_csv(f, index=False, header=f.tell()==0, lineterminator='\n')
    with open(yelp_csv_path, 'a') as f:
        df_yelp.to_csv(f, index=False, header=f.tell()==0, lineterminator='\n')

    # Clear the data lists for the next iteration
    foursquare_data.clear()
    yelp_data.clear()

# save the final versions of DataFrames outside the loop
df_foursquare.to_csv('foursquare_results.csv', index=False)
df_yelp.to_csv('yelp_results.csv', index=False)
