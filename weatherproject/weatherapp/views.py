from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import requests
import datetime

@csrf_exempt
def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Erode'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=fd135b932bf8794d26e07723d663ac63'
    PARAMS = {'units': 'metric'}
    try:
        data = requests.get(url, params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp_celsius = data['main']['temp']
        temp_fahrenheit = round((temp_celsius * 9/5) + 32,2)
        weather_class = get_weather_class(description)

        day = datetime.date.today()

        return render(
            request, 
            'index.html', 
            {
                'description': description, 
                'icon': icon, 
                'temp_celsius': temp_celsius, 
                'temp_fahrenheit': temp_fahrenheit, 
                'day': day, 
                'city': city, 
                'exception_occurred': False, 
                'weather_class': weather_class
            }
        )

    except:
        exception_occurred = True
        messages.error(request, "City weather is not available")
        day = datetime.date.today()
        return render(
            request, 
            'index.html', 
            {
                'icon': '01d', 
                'day': day, 
                'city': 'City weather not available', 
                'exception_occurred': True, 
                'weather_class': 'default-weather'
            }
        )


def get_weather_class(description):
    if 'clear' in description.lower():
        return 'sunny'
    elif 'cloud' in description.lower():
        return 'cloudy'
    elif 'rain' in description.lower():
        return 'rainy'
    elif 'snow' in description.lower():
        return 'snowy'
    elif 'haze' in description.lower() or 'smoke' in description.lower():
        return 'hazy'
    return 'default-weather'
