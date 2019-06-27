from django.shortcuts import render, redirect
from apps.parks.models import *
import requests
from django.contrib import messages

# Create your views here.


def index(request):
    context = {
        "all_parks": Park.objects.all(),
    }
    return render(request, 'parks/map.html', context)


def create(request):
    errors = Park.objects.address_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
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
        review_text = res2['result']['reviews'][0]['text']
        website = res2['result']['website']
        rating = res2['result']['rating']

        # # Get the photo
        # photo_id = res2['result']['photos'][0]['photo_reference']
        # params2 = {
        #     "place_id": place_id,
        #     "key": "AIzaSyDcuEo_YNfM-UN8VWL9IeXtfJHR30R4I_0",
        #     "photo_reference": photo_id,
        #     "maxwidth": 400
        # }
        # raw_image_data = requests.get(placesapi, params=params2)
        # print(raw_image_data)
        # print(photo_id)

        try:
            x = res2['result']['opening_hours']
        except:
            hours = "No hours listed"
        else:
            monday = res2['result']['opening_hours']['weekday_text'][0]
            tuesday = res2['result']['opening_hours']['weekday_text'][1]
            wednesday = res2['result']['opening_hours']['weekday_text'][2]
            thursday = res2['result']['opening_hours']['weekday_text'][3]
            friday = res2['result']['opening_hours']['weekday_text'][4]
            saturday = res2['result']['opening_hours']['weekday_text'][5]
            sunday = res2['result']['opening_hours']['weekday_text'][6]
            hours = [monday, tuesday, wednesday,
                thursday, friday, saturday, sunday]
        try:
            phone = res2['result']['formatted_phone_number']
        except:
            phone = "No Phone number available"
        # try:
        #     hours = res2['result']['opening_hours']['weekday_text']
        # except:
        #     hours = "No hours available"
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
    print(hours_str)
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




    # # Trying to get the photos from the places api
    # googlemapsapi = "https://maps.googleapis.com/maps/api/geocode/json"
    # params = {
    #         'address': park.address,
    #         'sensor': 'false',
    #         'region': 'us',
    #         'key': 'AIzaSyDcuEo_YNfM-UN8VWL9IeXtfJHR30R4I_0'
    #     }
    # req = requests.get(googlemapsapi, params=params)
    # res = req.json()
    # place_id = res['results'][0]['place_id']
    # print(place_id)


    # placesapi = "https://maps.googleapis.com/maps/api/place/details/json"
    # params = {
    #         "place_id": place_id,
    #         "key": "AIzaSyDcuEo_YNfM-UN8VWL9IeXtfJHR30R4I_0",
    #         # "fields" : "photo"
    #     }
    # req2 = requests.get(placesapi, params=params)
    # res2 = req2.json()
    # print(res2['result'])

    # # only get the 1st image, throwing a keyerror on 'photos'...works if this photo_id is hardcoded to any photo_reference
    # photo_id = res2['result']['photos'][0]['photo_reference'] 
    
    context = {
        "selected_park": park,
        "split_hours" : split_list,
        "formatted_hours" : left_bracket,
        "formatted_hours2" : right_bracket,
        "photo_reference" : "CmRaAAAAeJXXDzKtE0O7LMEL9kHnY7Y4zXnLthg1t4yALnjd9yH7uQLmhH_LdbU5-kavzEQML3tpexaquvsegJ0ZnSlOlhVvAqenKIK5ozan_yzq80EL0CKdF6HZgqv3Pgd0ScXPEhAPNr_rr8pKKHy-K5NmlL4fGhRGGsDKuDl05nFJNropoAvCbkbjdQ",
        # "key" :  "AIzaSyDcuEo_YNfM-UN8VWL9IeXtfJHR30R4I_0" # don't have to pass in, can hardcode in html
    }
    return render(request, "parks/parkinfo.html", context)
