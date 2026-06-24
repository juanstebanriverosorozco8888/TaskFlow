from django.urls import path

from .views import (
    login_view,
    register_view,
    logout_view,
    user_list,
    edit_user,
    delete_user
)

urlpatterns = [

    path(
        '',
        login_view,
        name='login'
    ),

    path(
        'register/',
        register_view,
        name='register'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),

    path(
        'users/',
        user_list,
        name='user_list'
    ),

    path(
        'users/edit/<str:user_uid>/',
        edit_user,
        name='edit_user'
    ),

    path(
        'users/delete/<str:user_uid>/',
        delete_user,
        name='delete_user'
    ),
]