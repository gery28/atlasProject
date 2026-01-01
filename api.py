import requests
# from atlas import API_KEY
import os

error_offset = 0

API_KEY = os.getenv("GOOGLE-MAPS-KEY")


def landmark_to_coords_open(name, name_eng="Default"):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": name_eng,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "geo-lookup-script"
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if not data:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": name,
            "format": "json",
            "limit": 1
        }
        headers = {
            "User-Agent": "geo-lookup-script"
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        if not data:
            global error_offset
            error_offset += 1
            print(f"Error: {name} not found. Offset: {error_offset}")
            return 0, 0 + error_offset
    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon


def landmark_to_coords_google(landmark):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": landmark,
        "key": API_KEY
    }

    response = requests.get(url, params=params).json()
    print(response)
    if len(response["results"]) != 0:
        location = response["results"][0]["geometry"]["location"]
        lat, lon = location["lat"], location["lng"]
        return lat, lon

    global error_offset
    error_offset += 1
    print(f"Error: {landmark} not found. Offset: {error_offset}")
    return 0, 0 + error_offset
