import jwt
from profiles.models import Account
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed


class JTW_AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'COOKIES')

        token = request.COOKIES.get('jwt')
        
        if token:
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                user = Account.objects.filter(id=payload['id']).first()
                request.api_user = user

            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated! Signature has expired')
        
        request.api_user = None
