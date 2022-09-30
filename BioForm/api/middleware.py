import jwt
from profiles.models import Account
from django.utils.deprecation import MiddlewareMixin


class JTW_AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'COOKIES')

        token = request.COOKIES.get('jwt')
        
        if token:
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                user = Account.objects.filter(id=payload['id']).first()
                request.api_user = user
                return

            except Exception:
                pass
        
        request.api_user = None
