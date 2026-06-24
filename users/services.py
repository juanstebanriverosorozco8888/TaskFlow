from config.firebase import db
from firebase_admin import firestore


def create_user_collection(
        uid,
        name,
        email,
        role
):

    db.collection(
        'users'
    ).document(uid).set({

        'uid': uid,

        'name': name,

        'email': email,

        'role': role,

        'created_at':
        firestore.SERVER_TIMESTAMP,

        'last_login':
        None

    })