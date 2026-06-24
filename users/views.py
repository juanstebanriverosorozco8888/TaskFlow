from django.shortcuts import (
    render,
    redirect
)

import os
import requests
import jwt

from datetime import (
    datetime,
    timedelta
)

from django.conf import settings
from django.contrib import messages

from firebase_admin import auth as admin_auth, firestore

from django.http import JsonResponse

from config.firebase import db

from datetime import datetime

from .services import (
    create_user_collection
)


def login_view(request):


    if request.method == "POST":

        email = request.POST.get(
            "email"
        )

        password = request.POST.get(
            "password"
        )

        try:

            api_key = os.getenv("FIREBASE_API_KEY")

            url = (
                "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
            )


            payload = {

                "email":
                email,

                "password":
                password,

                "returnSecureToken":
                True
            }

            response = requests.post(

                f"{url}?key={api_key}",

                json=payload
            )

            data = response.json()

            if 'localId' not in data:

                print(data)

                messages.error(

                    request,

                    data.get(
                        'error',
                        {}
                    ).get(
                        'message',
                        'Error login'
                    )
                )

                return redirect(
                    'login'
                )

            uid = data['localId']

            request.session["firebase_token"] = data["idToken"]
            
            user_doc = db.collection(
                'users'
            ).document(
                uid
            ).get()

            if not user_doc.exists:

                messages.error(
                    request,
                    "Usuario no encontrado"
                )

                return redirect(
                    'login'
                )

            user_found = user_doc.to_dict()

            firebase_user = admin_auth.get_user(
                uid
            )

            timestamp = int(

                firebase_user
                .user_metadata
                .last_sign_in_timestamp

            ) / 1000

            formatted_date = datetime.fromtimestamp(
                timestamp
            ).strftime(
                '%d/%m/%Y %H:%M'
            )

            db.collection(
                'users'
            ).document(
                uid
            ).update({

                'last_login':
                formatted_date
            })


            token = jwt.encode(

            {

                "uid": uid,

                "email": user_found['email'],

                "role": user_found['role'],

                "exp": datetime.utcnow() + timedelta(hours=8)

            },

            settings.SECRET_KEY,

            algorithm="HS256"
            )
            
            
            request.session['jwt'] = token

            request.session[
                'uid'
            ] = uid

            request.session[
                'email'
            ] = user_found[
                'email'
            ]

            request.session[
                'role'
            ] = user_found[
                'role'
            ]

            if user_found['role'] == 'admin':

                return redirect(
                    'admin_dashboard'
                )

            return redirect(
                'user_dashboard'
            )

        except Exception as e:

            print(e)

            messages.error(

                request,

                "Error de autenticación"
            )

    return render(

        request,

        'users/login.html'
    )

def register_view(request):

    if request.method == 'POST':

        name = request.POST.get(
            'name'
        )

        email = request.POST.get(
            'email'
        )

        password = request.POST.get(
            'password'
        )

        role = request.POST.get(
            'role'
        )

        try:

            firebase_user = admin_auth.create_user(

                email=email,

                password=password
            )

            uid = firebase_user.uid

            db.collection(
                'users'
            ).document(
                uid
            ).set({

                'uid':
                uid,

                'name':
                name,

                'email':
                email,

                'role':
                role,

                'last_login':
                None
            })

            messages.success(

                request,

                'Usuario creado'
            )

            return redirect(
                'login'
            )

        except Exception as e:

            print(e)

            messages.error(

                request,

                'Error al registrar usuario'
            )

    return render(

        request,

        'users/register.html'
    )

def logout_view(request):

    request.session.clear()

    request.session.flush()

    return redirect("login")

def user_list(request):

    role = request.jwt_user[
        'role'
    ]

    if role != 'admin':

        return redirect(
            'home_dashboard'
        )

    users = []

    docs = db.collection(
        'users'
    ).stream()

    for doc in docs:

        user = doc.to_dict()

        users.append({

            'uid':
            user.get(
                'uid'
            ),

            'name':
            user.get(
                'name'
            ),

            'email':
            user.get(
                'email'
            ),

            'role':
            user.get(
                'role'
            ),

            'last_login':
            user.get(
                'last_login',
                'Nunca'
            )
        })

    return render(

        request,

        'users/list.html',

        {

            'users':
            users
        }
    )


def edit_user(
        request,
        user_uid
):

    user_doc = None

    docs = db.collection(
        'users'
    ).where(
        'uid',
        '==',
        user_uid
    ).stream()

    for doc in docs:

        user_doc = doc

    user = (
        user_doc.to_dict()
    )

    if request.method == 'POST':

        role = request.POST.get(
            'role'
        )

        db.collection(
            'users'
        ).document(
            user_doc.id
        ).update({

            'role':
            role
        })

        messages.success(

            request,

            'Rol actualizado'
        )

        return redirect(
            'user_list'
        )

    return render(

        request,

        'users/edit.html',

        {

            'user':
            user
        }
    )


def delete_user(
        request,
        user_uid
):

    docs = db.collection(
        'users'
    ).where(
        'uid',
        '==',
        user_uid
    ).stream()

    for doc in docs:

        db.collection(
            'users'
        ).document(
            doc.id
        ).delete()

    messages.success(

        request,

        'Usuario eliminado'
    )

    return redirect(
        'user_list'
    )


def home_dashboard(request):
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
        if t['status'] == 'Pendiente'
    ])

    progress = len([
        t for t in tasks
        if t['status'] == 'En progreso'
    ])

    completed = len([
        t for t in tasks
        if t['status'] == 'Completada'
    ])

    return render(

        requests.request,

        'dashboard/user_home.html',

        {

            'pending': pending,

            'progress': progress,

            'completed': completed
        }
    )
        