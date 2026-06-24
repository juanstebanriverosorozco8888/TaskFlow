import requests
import os


API_KEY = os.getenv(
    'WEATHER_API_KEY'
)


def get_weather(city):

    url = (
        'https://api.openweathermap.org/data/2.5/weather'
    )

    params = {

        'q':
        city,

        'appid':
        API_KEY,

        'units':
        'metric',

        'lang':
        'es'
    }

    response = requests.get(
        url,
        params=params
    )

    if response.status_code == 200:

        return response.json()

    return None