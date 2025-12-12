from ipyleaflet import Map, Marker
from ipywidgets.embed import embed_minimal_html
from flask import Flask, render_template
import folium
from folium.plugins import FeatureGroupSubGroup
import requests
from tqdm import tqdm

from api import landmark_to_coords

app = Flask(__name__)

START_ZOOM = 4
MIN_ZOOM = 2
MAX_ZOOM = 20
MIN_LON = -360
MAX_LON = 360
MIN_LAT = -180
MAX_LAT = 1800

data = ["hungary", "Strait of Gibraltar", "Alaska", "caribbean sea", "Mississippi Plains", "Volga", "Panama-canal",
        "Kamchatka Peninsula", "North Europe", "Vienna Basin", "Iberian Peninsula", "Mátra",
        "Pécsi ókeresztény sírkamrák",
        "Early Christian tombs of Pécs", "Szabolcs-Szatmár-Bereg megye", "Dunántúl", "Kis-Balaton", "Soproni-hegység",
        "Salgótarján", "Duna", "Aggteleki Nemzeti Park", "Middle East Asia"]

landmarks = []
# for i in data:
# landmarks.append([i, landmark_to_coords(i)])

titles = {"A földrész részei": "Parts of the continent", "Tájak": "Landscapes", "Vízrajz": "Waterscape",
          "Országok": "Countries",
          "Városok": "Cities"}

markers = {"Parts of the continent": ["red", "cloud"], "Landscapes": ["green", "cloud"],
           "Waterscape": ["blue", "cloud"],
           "Countries": ["orange", "cloud"],
           "Cities": ["pink", "cloud"]}
asia = []
with open("asia.txt", "r", encoding="utf-8") as file:
    for i in file.read().split("*"):
        segment = []
        for j in i.split(", "):
            if j != "":
                segment.append(j.strip("\n").replace("\n", " "))
        if len(segment) != 0:
            asia.append(segment)
print(*asia, sep="\n")
print("\n")
asia_eng = []
with open("asia-eng.txt", "r", encoding="utf-8") as file:
    for i in file.read().split("*"):
        segment = []
        for j in i.split(", "):
            if j != "":
                segment.append(j.strip("\n").replace("\n", " "))
        if len(segment) != 0:
            asia_eng.append(segment)
# print(*asia_eng, sep="\n")
# print(list(titles.items()))
asia_dict = []
for i in range(len(asia)):
    for j in range(len(asia[i])):
        asia_dict.append([list(titles.items())[i][1], {asia[i][j]: asia_eng[i][j]}])

print(*asia_dict, sep="\n")
print(list(asia_dict[0][1].items())[0])

#for i in tqdm(asia_dict):
    #print(list(i[1].items())[0])
    #landmarks.append([i, landmark_to_coords(list(i[1].items())[0][0], list(i[1].items())[0][1])])

#with open("asia-save.txt", "w", encoding="utf-8") as file:
    #file.write(str(landmarks))

with open("asia-save.txt", "r", encoding="utf-8") as file:
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
        print(i)
        folium.Marker(
            location=[float(i[1][0]), float(i[1][1])],
            tooltip=str(landmark_name_touple[0]),
            popup=str(landmark_name_touple[0]),
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

    m.save("templates/map.html")
    m.save("map.html")

    @app.route("/")
    def home():
        return render_template("map.html")

    app.run()


if __name__ == "__main__":
    main()
