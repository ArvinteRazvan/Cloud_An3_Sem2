import google_geolocation_api as geo
import requests

API_KEY = "7428a01d3e0994050942425eefc0a7d5"


def get_weather():
    lat, lng = geo.get_coordonates()

    payload = {'lat': lat, 'lon': lng, 'appid': API_KEY}
    r = requests.get('http://api.openweathermap.org/data/2.5/weather', params=payload)
    print(lat,lng)
    print(r.url)
    print("Wheather API - success")
    return r.json()
