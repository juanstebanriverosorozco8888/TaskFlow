from django.shortcuts import render

from .services import (
    get_weather
)


def user_weather_view(request):

    city = request.GET.get(
        'city',
        'Bogotá'
    )

    data = get_weather(
        city
    )

    weather = None

    if data:

        weather = {

            'city':
            data['name'],

            'temp':
            data['main']['temp'],

            'description':
            data['weather'][0]['description'],

            'humidity':
            data['main']['humidity'],

            'wind':
            data['wind']['speed'],

            'icon':
            data['weather'][0]['icon']
        }

    return render(

        request,

        'weather/user_weather.html',

        {

            'weather':
            weather
        }
    )

def weather_view(request):

    city = request.GET.get(
        'city',
        'Bogotá'
    )

    data = get_weather(
        city
    )

    weather = None

    if data:

        weather = {

            'city':
            data['name'],

            'temp':
            data['main']['temp'],

            'description':
            data['weather'][0]['description'],

            'humidity':
            data['main']['humidity'],

            'wind':
            data['wind']['speed'],

            'icon':
            data['weather'][0]['icon']
        }

    return render(

        request,

        'weather/weather.html',

        {

            'weather':
            weather
        }
    )