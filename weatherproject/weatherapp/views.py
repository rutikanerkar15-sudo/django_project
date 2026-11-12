from django.shortcuts import render
import requests
import datetime

def home(request):
    city = 'Pune'
    if request.method == 'POST':
        user_city = request.POST.get('city')
        if user_city and user_city.strip():
            city = user_city.strip()

    # OpenWeatherMap API
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=402dd1f6a516a443a97ec6d8eabd1d8f'
    PARAMS = {'units': 'metric'}

    # Google Custom Search API for background images (safe fallback if it fails)
    image_url = 'https://images.unsplash.com/photo-1534088568595-a066fa41088a'
    try:
        API_KEY = 'AIzaSyCkZPY0yMGjVD3VKyqIU_XfhrvZyNHvMw8'
        SEARCH_ENGINE_ID = '8418bff11a3a541dc'
        query = city + " 1920x1080"
        city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&searchType=image&imgSize=xlarge"
        
        search_data = requests.get(city_url).json()
        search_items = search_data.get("items")
        if search_items:
            image_url = search_items[0].get('link', image_url)
    except Exception:
        pass

    # Fetch weather data safely
    try:
        response = requests.get(url, params=PARAMS)
        data = response.json()
        
        if response.status_code != 200 or 'weather' not in data:
            raise Exception("Weather data not found")

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
        day = datetime.date.today()
        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': city,
            'exception_occurred': True,
            'image_url': image_url
        })