from django.shortcuts import render, redirect
from apps.parks.models import *
import requests
from django.contrib import messages

# Create your views here.


def index(request):
    context = {
        "all_parks": Park.objects.all(),
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
            created_by=User.objects.get(id=1)
        )
        return redirect("/")

def parkinfo(request, parkid):

    park = Park.objects.get(id=parkid) #Get the park from the parkid
    hours_str = park.operating_hours #Get the string for park operating hours
    if hours_str == "No hours listed":
        left_bracket = "No hours listed"
        right_bracket= ""
        split_list = []
    else:
        split_list = hours_str.split(",") #Split the string into a list of strings, separated by commas

        #Replace [] and ' with empty string
        for word in split_list:
            if "[" in word:
                left_bracket = word.replace("[", "") #Only returns Monday without [
        for word in split_list:
            if "]" in word:
                right_bracket = word.replace("]", "") #Only returns Sunday without ]
        for word in split_list:
            if "'" in word:
                quotation = word.replace("'", "") #Not working
        
        split_list = split_list[1:-1]  # cutting off Monday and Sunday

    # 2 different ways trying to remove beginning and ending quotation
    # for i in range(len(split_list)):
    #     if split_list[i] == "'":
    #         quotation = split_list[i].replace("'","")
    #     print(quotation)

    # for hour in split_list:
    #     split_list[hour].replace("'","")
    # print(split_list)




    # Trying to get the photos from the places api
    googlemapsapi = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
            'address': park.address,
            'sensor': 'false',
            'region': 'us',
            'key': 'AIzaSyDcuEo_YNfM-UN8VWL9IeXtfJHR30R4I_0'
        }
    req = requests.get(googlemapsapi, params=params)
    res = req.json()
    place_id = res['results'][0]['place_id']
    print(place_id)


    placesapi = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
            "place_id": place_id,
            "key": "AIzaSyDcuEo_YNfM-UN8VWL9IeXtfJHR30R4I_0",
        }
    req2 = requests.get(placesapi, params=params)
    res2 = req2.json()

    # only get the 1st image, throwing a keyerror on 'photos'...works if this photo_id is hardcoded to any photo_reference
    try:
        photo_id = res2['result']['photos'][0]['photo_reference']
    except:
        photo_id = "No Photo"
    
    context = {
        "selected_park": park,
        "split_hours" : split_list,
        "formatted_hours" : left_bracket,
        "formatted_hours2" : right_bracket,
        "photo_reference" : photo_id,
        # "key" :  "AIzaSyDcuEo_YNfM-UN8VWL9IeXtfJHR30R4I_0" # don't have to pass in, can hardcode in html
    }
    return render(request, "parks/parkinfo.html", context)