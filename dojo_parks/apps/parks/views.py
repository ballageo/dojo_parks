from django.shortcuts import render, redirect
from .models import *
import requests

# Create your views here.

def index(request):
    return render(request, 'parks/map.html')

def create(request):
    # Google Maps API
    googlemapsapi = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': request.POST['location'],
        'sensor': 'false',
        'region': 'us',
        'key': 'AIzaSyDcuEo_YNfM-UN8VWL9IeXtfJHR30R4I_0'
    }
    req = requests.get(googlemapsapi, params=params)
    res = req.json()
    print(res)
    latitude = res['results'][0]['geometry']['location']['lat']
    longitude = res['results'][0]['geometry']['location']['lng']
    place_id = res['results'][0]['place_id']
    address = request.POST['location']

    placesapi = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": "AIzaSyDcuEo_YNfM-UN8VWL9IeXtfJHR30R4I_0",
    }
    req2 = requests.get(placesapi, params=params)
    res2 = req2.json()
    title = res2['result']['name']
    rating = res2['result']['rating']
    print("*" * 100)
    print(res2)
    print("*" * 100)
    print(title)
    print("*" * 100)
    print(rating)



    return redirect("/")
