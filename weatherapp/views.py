from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=402dd1f6a516a443a97ec6d8eabd1d8f'
    PARAMS = {'units': 'metric'}
    API_KEY = 'AIzaSyCkZPY0yMGjVD3VKyqIU_XfhrvZyNHvMw8'
    SEARCH_ENGINE_ID = '8418bff11a3a541dc'

    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    data = requests.get(city_url).json()
    print(data)  # TEMP: check your terminal — look for an "error" key and its message

    search_items = data.get("items")
    if search_items:
        image_url = search_items[0]['link']
    else:
        image_url = None  # fall back gracefully instead of crashing

    try:
        data = requests.get(url, params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except Exception:
        exception_occurred = True
        messages.error(request, 'Entered data is not available to API')
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occurred': exception_occurred
        })