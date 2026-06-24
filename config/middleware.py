from django.shortcuts import redirect
import jwt

from django.conf import settings

from django.shortcuts import redirect

from firebase_admin import auth

class FirebaseAuthMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        public_urls = [

            '/',
            '/register/',
        ]

        if request.path in public_urls:

            return self.get_response(request)

        token = request.session.get(
            "firebase_token"
        )

        if not token:

            return redirect(
                "login"
            )

        try:

            decoded_token = auth.verify_id_token(
                token
            )

            
            request.firebase_user = (
                decoded_token
            )

        except Exception:

            request.session.flush()

            return redirect(
                "login"
            )

        return self.get_response(
            request
        )


class JWTAuthenticationMiddleware:

    def __init__(

        self,

        get_response

    ):

        self.get_response = get_response

    def __call__(

        self,

        request

    ):

        public_urls = [

            '/',

            '/register/'
        ]

        if request.path in public_urls:

            return self.get_response(
                request
            )

        token = request.session.get(
            'jwt'
        )

        if not token:

            return redirect(
                'login'
            )

        try:

            decoded = jwt.decode(

                token,

                settings.SECRET_KEY,

                algorithms=['HS256']
            )
            
            request.jwt_user = decoded

        except jwt.ExpiredSignatureError:

            request.session.flush()

            return redirect(
                'login'
            )

        except jwt.InvalidTokenError:

            request.session.flush()

            return redirect(
                'login'
            )

        response = self.get_response(
            request
        )

        response[
            'Cache-Control'
        ] = 'no-cache, no-store, must-revalidate'

        response[
            'Pragma'
        ] = 'no-cache'

        response[
            'Expires'
        ] = '0'

        return response
    


class NoCacheMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        response["Cache-Control"] = (
            "no-cache, no-store, must-revalidate"
        )

        response["Pragma"] = "no-cache"

        response["Expires"] = "0"

        return response