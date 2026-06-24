from django.urls import path

from .views import (
    task_list,
    create_task_view,
    edit_task_view,
    delete_task,
    update_status,
    user_task_list,
    user_update_status
)

urlpatterns = [

    path(
        '',
        task_list,
        name='task_list'
    ),
    
    path(
        'user/',
        user_task_list,
        name='user_task_list'
    ),

    path(
        'create/',
        create_task_view,
        name='create_task'
    ),

    path(
        'edit/<str:task_id>/',
        edit_task_view,
        name='edit_task'
    ),

    path(
        'delete/<str:task_id>/',
        delete_task,
        name='delete_task'
    ),

    path(
        'status/<str:task_id>/',
        update_status,
        name='update_status'
    ),

    path(
        'user/status/<str:task_id>/',
        user_update_status,
        name='user_update_status'
    ),
]