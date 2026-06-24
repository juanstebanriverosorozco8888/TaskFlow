from django.urls import path

from .views import (
    weather_view,
    user_weather_view
)

urlpatterns = [

    path(
        '',
        weather_view,
        name='weather'
    ),

    path(
        'user/',
        user_weather_view,
        name='user_weather'
    )
]