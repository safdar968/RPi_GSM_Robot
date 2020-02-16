
from flask import Flask

import folium

app = Flask(__name__)


@app.route('/')
def index():
    start_coords = (28.704059, 77.102490)
    folium_map = folium.Map(location=start_coords, zoom_start=14)
    folium.Marker([28.704059, 77.102490], 
              popup = 'Delhi').add_to(folium_map)
    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)