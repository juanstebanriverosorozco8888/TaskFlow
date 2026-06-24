import os

import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

from dotenv import load_dotenv

load_dotenv()

if not firebase_admin._apps:

    private_key = os.getenv("FIREBASE_PRIVATE_KEY")

    if not private_key:
        raise Exception(
            "FIREBASE_PRIVATE_KEY no existe en el .env"
        )

    private_key = private_key.replace("\\n", "\n")

    cred = credentials.Certificate({

        "type": os.getenv("FIREBASE_TYPE"),

        "project_id": os.getenv("FIREBASE_PROJECT_ID"),

        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),

        "private_key": private_key,

        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),

        "client_id": os.getenv("FIREBASE_CLIENT_ID"),

        "auth_uri": os.getenv("FIREBASE_AUTH_URI"),

        "token_uri": os.getenv("FIREBASE_TOKEN_URI"),

        "auth_provider_x509_cert_url":
            os.getenv("FIREBASE_AUTH_PROVIDER_CERT_URL"),

        "client_x509_cert_url":
            os.getenv("FIREBASE_CLIENT_CERT_URL"),

        "universe_domain":
            os.getenv("FIREBASE_UNIVERSE_DOMAIN")

    })

    firebase_admin.initialize_app(cred)

db = firestore.client()


def verify_firebase_token(id_token):
    return auth.verify_id_token(id_token)