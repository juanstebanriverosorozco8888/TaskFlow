from django.urls import path

from .views import (
    admin_dashboard,
    user_dashboard,
    home_dashboard
)

urlpatterns = [

    path(
        '',
        home_dashboard,
        name='home_dashboard'
    ),

    path(
        'admin/',
        admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'user/',
        user_dashboard,
        name='user_dashboard'
    )
]