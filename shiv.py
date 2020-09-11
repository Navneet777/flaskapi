
import requests
import json

URL = "http://api.letgo.com/api/iplookup.json"
r = requests.get(url = URL)

data = r.json()
lat = data['latitude']
lon = data['longitude']

URL2 = "https://nominatim.openstreetmap.org/reverse"
params = {'lat': lat, 'lon': lon, 'format': 'json'}
r2 = requests.post(url = URL2,params=params)
data2 = r2.json()
display_name = data2['display_name']
city = data2['address']
print("display_name :" ,display_name)
city = city['city']
print("city :",city)
