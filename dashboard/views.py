from django.shortcuts import (
    render,
    redirect
)

from config.firebase import db

def home_dashboard(request):

    role = request.jwt_user[
        'role'
    ]

    if role == 'admin':

        return admin_dashboard(
            request
        )

    return user_dashboard(
        request
    )

def admin_dashboard(request):

    uid = request.jwt_user[
        'uid'
    ]

    if not uid:

        return redirect(
            'login'
        )

    user_doc = db.collection(
        'users'
    ).document(uid).get()

    user = user_doc.to_dict()

    role = user.get(
        'role'
    )

    total_projects = len(
        list(
            db.collection(
                'projects'
            ).stream()
        )
    )

    total_tasks = len(
        list(
            db.collection(
                'tasks'
            ).stream()
        )
    )

    total_users = len(
        list(
            db.collection(
                'users'
            ).stream()
        )
    )

    # si es usuario luego hacemos otro dashboard
    if role == 'usuario':

        return redirect(
            'user_dashboard'
        )

    return render(

        request,

        'dashboard/home.html',

        {

            'user':
            user,

            'total_projects':
            total_projects,

            'total_tasks':
            total_tasks,

            'total_users':
            total_users
        }
    )

def user_dashboard(request):

    uid = request.jwt_user[
        'uid'
    ]

    tasks = []

    docs = db.collection(
        'tasks'
    ).where(
        'assigned_to',
        '==',
        uid
    ).stream()

    for doc in docs:

        tasks.append(
            doc.to_dict()
        )

    pending = len([

        t for t in tasks

        if t['status']
        == 'Pendiente'
    ])

    progress = len([

        t for t in tasks

        if t['status']
        == 'En progreso'
    ])

    completed = len([

        t for t in tasks

        if t['status']
        == 'Completada'
    ])

    return render(

        request,

        'dashboard/user_home.html',

        {

            'pending': pending,

            'progress': progress,

            'completed': completed
        }
    )