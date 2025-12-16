from ipyleaflet import Map, Marker
from ipywidgets.embed import embed_minimal_html
from flask import Flask, render_template, render_template_string
from waitress import serve
import folium
from folium.plugins import FeatureGroupSubGroup, Search, MarkerCluster
import requests
from tqdm import tqdm
import logging

from api import landmark_to_coords
from build import titles, markers

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,  # INFO level logs and above
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)


START_ZOOM = 4
MIN_ZOOM = 2
MAX_ZOOM = 20
MIN_LON = -360
MAX_LON = 360
MIN_LAT = -180
MAX_LAT = 1800

try:
    with open("asia-save.txt", "r", encoding="utf-8") as file:
        landmarks = eval(file.read())
except:
    with open("app/asia-save.txt", "r", encoding="utf-8") as file:
        landmarks = eval(file.read())


# country_code,latitude,longitude,country,usa_state_code,usa_state_latitude,usa_state_longitude,usa_state
# test_coords_file = []
# with open("world_country_and_usa_states_latitude_and_longitude_values.csv", "r") as file:
#    for i in file.readlines():
#        test_coords_file.append(i.split(","))


def main():
    # m = Map(center=(52.2, 0.1), zoom=10)
    # m.add(Marker(location=(52.2, 0.1)))
    #
    # embed_minimal_html("templates/map.html", views=[m], title="Leaflet map")

    m = folium.Map(location=[0, 0],
                   zoom_start=START_ZOOM,
                   min_zoom=MIN_ZOOM,
                   max_zoom=MAX_ZOOM,
                   min_lat=MIN_LAT,
                   max_lat=MAX_LAT,
                   min_lon=MIN_LON,
                   max_lon=MAX_LON,
                   zoom_control=True,
                   max_bounds=True
                   )
    # main_group = folium.FeatureGroup(name='All Markers').add_to(m)
    learning_group = folium.FeatureGroup(name='learning')
    text_group = folium.FeatureGroup(name='text', show=False)
    test_group = folium.FeatureGroup(name='test', show=False)

    for i in landmarks:
        landmark_name_touple = list(i[0][1].items())[0]
        logger.info(i)
        folium.Marker(
            location=[float(i[1][0]), float(i[1][1])],
            tooltip=str(landmark_name_touple[0]),
            popup=str(landmark_name_touple[0]),
            title=str(landmark_name_touple[0]),
            icon=folium.Icon(icon=markers[i[0][0]][1], color=markers[i[0][0]][0]),

        ).add_to(learning_group)
        folium.Marker(
            location=[float(i[1][0]), float(i[1][1])],
            tooltip=str(landmark_name_touple[0]),
            popup=str(landmark_name_touple[0]),
            icon=folium.DivIcon(html=f"""
                                     <div style="
                                         position: relative;
                                         top: -50px;
                                         left: -10px;
                                         color: black;
                                         font-size: 12px;
                                         font-weight: bold;
                                         background: rgba(255,255,255,0);
                                         padding: 2px 4px;
                                         border-radius: 3px;
                                         min-width:200px
                                     ">
                                         {landmark_name_touple[0]}
                                     </div>
                                     """
                                ),

        ).add_to(text_group)
        folium.Marker(
            location=[float(i[1][0]), float(i[1][1])],
            tooltip="Reveal!",
            popup=str(landmark_name_touple[0]),
            icon=folium.Icon(icon="cloud", color="red"),
        ).add_to(test_group)
    learning_group.add_to(m)
    text_group.add_to(m)
    test_group.add_to(m)
    folium.Marker(
        location=[52.204793, 0.121558],
        tooltip="Click me!",
        popup="""
Not all those who wander are lost
― J.R.R. Tolkien, The Fellowship of the Ring""",
        icon=folium.Icon(icon="info-sign")
    ).add_to(m)

    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png',
        attr='light-nolabels',
        name='light-nolabels',
        min_zoom=MIN_ZOOM
    ).add_to(m)

    folium.TileLayer(
        tiles='https://tiles.stadiamaps.com/tiles/stamen_toner_lite/{z}/{x}/{y}{r}.png',
        attr='toner-light',
        name='Toner-Light',
        min_zoom=MIN_ZOOM,
    ).add_to(m)

    folium.TileLayer(
        tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
        attr='OpenTopoMap',
        name='Topo Map',
        min_zoom=MIN_ZOOM
    ).add_to(m)

    geojson_data = requests.get(
        "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"
    ).json()

    folium.GeoJson(geojson_data, name="country outlines").add_to(m)

    folium.LayerControl().add_to(m)

    search = Search(
        layer=learning_group,
        geom_type='Point',
        search_label="title",  # or "popup"
        placeholder="Search city",
        collapsed=False
    ).add_to(m)

    # m.save("templates/map.html")
    # m.save("map.html")

    # @app.route("/")
    # def home():
    #     return render_template("map.html")

    @app.route("/")
    def fullscreen():
        return m.get_root().render()


if __name__ == "__main__":
    main()
    app.run(port=5000)
