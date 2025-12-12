import requests

error_offset=0
def landmark_to_coords(name, name_eng="Default"):
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
            return 0, 0+error_offset
    lat = float(data[0]["lat"])
    lon = float(data[0]["lon"])
    return lat, lon
