import requests
import pandas as pd

# Endpoint for all networks
url_networks = "http://api.citybik.es/v2/networks"

# Fetch data from the networks endpoint
response = requests.get(url_networks)
data = response.json()

# Extract the 'id' for Paris
paris_id = None
for network in data['networks']:
    if network['location']['city'] == 'Paris':
        paris_id = network['id']
        break

# If Paris is found, fetch station details for Paris
if paris_id:
    url_paris = f"http://api.citybik.es/v2/networks/{paris_id}"
    response_paris = requests.get(url_paris)
    data_paris = response_paris.json()

    stations = data_paris['network']['stations']

    # Extract required details: latitude, longitude, and number of bikes
    station_details = [{'Latitude': s['latitude'], 
                        'Longitude': s['longitude'], 
                        'Number_of_Bikes': s['free_bikes']} for s in stations]

    # Convert the data into a Pandas dataframe
    df = pd.DataFrame(station_details)
    print(df)
else:
    print("Paris not found in the list of networks.")

print(df.describe())

df.to_csv('paris_bike_stations.csv', index=False)
