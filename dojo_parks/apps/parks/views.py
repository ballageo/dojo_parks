from django.shortcuts import render, redirect
from apps.parks.models import *
import requests
from django.contrib import messages

# Create your views here.


def index(request):
    context = {
        "user" : User.objects.get(id=request.session["user_id"]),
        "all_parks": Park.objects.all(),
        "sidebar_parks": Park.objects.all().order_by("-id")[:10],
        "last_park": Park.objects.last(),
    }
    return render(request, 'parks/map.html', context)


def create(request):
    errors = Park.objects.address_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect("/")
    else:
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

        # Google Places API
        placesapi = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            "place_id": place_id,
            "key": "AIzaSyDcuEo_YNfM-UN8VWL9IeXtfJHR30R4I_0",
        }
        req2 = requests.get(placesapi, params=params)
        res2 = req2.json()
        title = res2['result']['name']
        formatted_address = res2['result']['formatted_address']
        try:
            review_text = res2['result']['reviews'][0]['text']
        except:
            review_text = "No reviews yet"
        try:
            website = res2['result']['website']
        except:
            website = "Sorry, no website available"
        try:
            rating = res2['result']['rating']
        except:
            rating = 0
        try:
            phone = res2['result']['formatted_phone_number']
        except:
            phone = "No Phone number available"
        try:
            hours = res2['result']['opening_hours']['weekday_text']
        except:
            hours = "No hours available"
        # Create the park 
        Park.objects.create(
            title=title,
            address=formatted_address,
            review=review_text,
            rating=rating,
            longitude=longitude,
            latitude=latitude,
            operating_hours=hours,
            website=website,
            phone_number=phone,
            created_by=User.objects.get(id=request.session["user_id"])
        )
        return redirect("/")

def parkinfo(request, parkid):
    park = Park.objects.get(id=parkid)
    context = {
        "selected_park": park,
    }
    return render(request, "parks/parkinfo.html", context)


def removePark(request, parkid):
    Park.objects.get(id = parkid).delete()
    return redirect('/')


def changeIcon(request, parkid):
    clicked_park = Park.objects.get(id=parkid)
    return redirect("/")