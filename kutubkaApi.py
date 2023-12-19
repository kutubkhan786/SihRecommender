
# from flask import Flask, request, jsonify
# import pandas as pd
# from geopy.geocoders import Nominatim
# from sklearn.cluster import KMeans

# app = Flask(__name__)

# # Read the CSV file and perform clustering (similar to your existing code)
# # ... (Your existing code here)

# # API endpoint for similar cities
# @app.route('/api/similar_cities', methods=['GET'])
# def get_similar_cities(df):
#     # Get input city from query parameter
#     input_city = request.args.get('city')

#     # Find cluster for the input city
#     cluster = df.loc[df['location'] == input_city, 'loc_clusters'].iloc[0]

#     # Retrieve cities in the same cluster, excluding the input city
#     similar_cities = df.loc[df['loc_clusters'] == cluster, 'location']
#     similar_cities = similar_cities[similar_cities != input_city]

#     # Return similar cities in JSON format
#     return jsonify({'similar_cities': similar_cities.tolist()})

# if __name__ == '__main__':
#     app.run(debug=True)  # Run the app in debug mode
from flask import Flask, request, jsonify
import pandas as pd
from geopy.geocoders import Nominatim
from sklearn.cluster import KMeans

app = Flask(__name__)

# Read the CSV file and perform clustering
df = pd.read_csv('T_locations.csv')

# Geocode the locations
country = 'India'
geolocator = Nominatim(user_agent="Trips")
locations = []

for city in df['location']:
    location = geolocator.geocode(city + ', ' + country)
    if location:
        locations.append((location.latitude, location.longitude))
    else:
        locations.append((None, None))

# Create a DataFrame for locations
locations_df = pd.DataFrame(locations, columns=['Latitude', 'Longitude'])

# Use KMeans to cluster the locations
kmeans = KMeans(n_clusters=5)  # Adjust the number of clusters as needed
df['loc_clusters'] = kmeans.fit_predict(locations_df)

# API endpoint for similar cities
@app.route('/api/similar_cities', methods=['GET'])
def get_similar_cities():
    input_city = request.args.get('city')

    if input_city not in df['location'].values:
        return jsonify({'error': 'City not found'})

    cluster = df.loc[df['location'] == input_city, 'loc_clusters'].iloc[0]
    similar_cities = df.loc[df['loc_clusters'] == cluster, 'location']
    similar_cities = similar_cities[similar_cities != input_city]

    return jsonify({'similar_cities': similar_cities.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
