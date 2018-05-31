import googlemaps
from datetime import datetime
import requests


API_Key = "AIzaSyCfabPcy5jVLHr2ONeIB_ifaeLtXfvCvPE"

def get_coordonates():
    r = requests.post("https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCfabPcy5jVLHr2ONeIB_ifaeLtXfvCvPE")
    r = r.json()
    print("google location-success")
    return r['location']['lat'], r['location']['lng']


# Geolocation_Api_key="AIzaSyDu-3Df73MElHXZ9JWoA2XsmUrSY2dzItY"

# gmaps = googlemaps.Client(key=Geolocation_Api_key)

# print(gmaps)

# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((r['location']['lat'], r['location']['lng']))

# print(reverse_geocode_result['formatted_address'])

