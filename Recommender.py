import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from geopy.geocoders import Nominatim
from sklearn.cluster import KMeans

# Read the CSV file
df = pd.read_csv('T_locations.csv')

# Geocoding the locations
country = 'India'
city_names = df['location']

geolocator = Nominatim(user_agent="Trips")
locations = []

for c in city_names:
    location = geolocator.geocode(c + ', ' + country)
    if location is None:
        print("Error finding coordinates for: " + c)
    else:
        locations.append((location.latitude, location.longitude))

# Create a DataFrame for locations
locations_df = pd.DataFrame(locations, columns=['Latitude', 'Longitude'])

# Use KMeans to cluster the locations
kmeans = KMeans(n_clusters=5)  # Adjust the number of clusters as needed
df['loc_clusters'] = kmeans.fit_predict(locations_df)

# Get input city from user
input_city = input("Enter a city name: ")

# Find cluster for the input city
cluster = df.loc[df['location'] == input_city, 'loc_clusters'].iloc[0]

# Retrieve cities in the same cluster, excluding the input city
similar_cities = df.loc[df['loc_clusters'] == cluster, 'location']
similar_cities = similar_cities[similar_cities != input_city]

# Display similar cities in the same cluster
for city in similar_cities:
    print(city)
