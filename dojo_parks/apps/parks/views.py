from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
<<<<<<< Updated upstream
    return render(request, "parks/index.html")
=======
    context = {
        "all_parks": Park.objects.all(),
    }
    return render(request, 'parks/map.html', context)


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

    # Google Places API

    placesapi = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "key": "AIzaSyDcuEo_YNfM-UN8VWL9IeXtfJHR30R4I_0",
    }
    req2 = requests.get(placesapi, params=params)
    res2 = req2.json()
    title = res2['result']['name']
    website = res2['result']['website']
    phone = res2['result']['formatted_phone_number']
    formatted_address = res2['result']['formatted_address']
    review_text = res2['result']['reviews'][0]['text'],

    try:
        rating = res2['result']['rating']
        hours = res2['result']['opening_hours']['weekday_text']
    except:
        rating = 0
        hours = "Sorry, no hours available"

    print("*" * 100)
    print(res2)
    print("*" * 100)
    print(title)
    print("*" * 100)
    print(rating)
    print("*" * 100)
    print(website)
    print("*" * 100)
    print(phone)
    print("*" * 100)
    print(formatted_address)
    print("*" * 100)
    print(review_text[0])

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

    park = Park.objects.get(id=parkid)
    print(park.operating_hours) # an array of 7 strings

    # The code below should loop through the array and print each string, but it's treating the whole park.operating_hours as 1 string, index 0 is the [....WTF???

    # for text in  enumerate(park.operating_hours):
    #     print(text)

    for text in park.operating_hours:
        print(text)
    # for  i in range(len(park.operating_hours)) :
    #     print(park.operating_hours[i]) 
    #     i += 1

    # [print(i) for i in park.operating_hours]

    print(park.operating_hours)

    

    context = {
        "selected_park": park,
    }
    return render(request, "parks/parkinfo.html", context)
>>>>>>> Stashed changes
