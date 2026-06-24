from django.urls import path

from .views import (
    project_list,
    create_project_view,
    edit_project_view,
    delete_project
)

urlpatterns = [

    path(
        '',
        project_list,
        name='project_list'
    ),

    path(
        'create/',
        create_project_view,
        name='create_project'
    ),

    path(
        'edit/<str:project_id>/',
        edit_project_view,
        name='edit_project'
    ),

    path(
        'delete/<str:project_id>/',
        delete_project,
        name='delete_project'
    ),
]