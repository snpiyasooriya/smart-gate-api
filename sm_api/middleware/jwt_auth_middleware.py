import jwt
from django.http import JsonResponse
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model

class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.COOKIES.get('access_token')
        if token:
            try:
                # Decode the token
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload.get('user_id')

                # Attach the user instance to the request
                if user_id:
                    User = get_user_model()
                    request.user = User.objects.get(id=user_id)
                else:
                    request.user = None
            except jwt.ExpiredSignatureError:
                request.user = None
                return JsonResponse({'error': 'Token has expired'}, status=401)
            except jwt.InvalidTokenError:
                request.user = None
                return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            request.user = None

        return None
