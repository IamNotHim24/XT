from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_restaurants_nearby(lat, lon, radius=10000):
    # Overpass API query for restaurants
    query = f"""
    [out:json];
    (node["amenity"="restaurant"](around:{radius},{lat},{lon});
    way["amenity"="restaurant"](around:{radius},{lat},{lon});
    relation["amenity"="restaurant"](around:{radius},{lat},{lon}););
    out body;
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    response = requests.get(overpass_url, params={'data': query})
    
    restaurants = []
    if response.status_code == 200:
        data = response.json()
        for element in data['elements']:
            name = element['tags'].get('name', 'N/A')
            address = element['tags'].get('addr:full', 'N/A')
            restaurants.append({'name': name, 'address': address})
    return restaurants

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        lat = float(request.form['latitude'])
        lon = float(request.form['longitude'])
        restaurants = get_restaurants_nearby(lat, lon)
        return render_template('index.html', restaurants=restaurants)
    return render_template('index.html', restaurants=None)

if __name__ == '__main__':
    app.run(debug=True)
