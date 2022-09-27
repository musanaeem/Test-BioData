import jwt
from profiles.models import Account
from .serializers import LoginSerializer
from django.utils.deprecation import MiddlewareMixin



class JTW_AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'COOKIES')

        token = request.COOKIES.get('jwt')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user = Account.objects.filter(id=payload['id']).first()

            if user:
                serializer = LoginSerializer(user)    
                request.api_user = serializer
                return
        except:
            pass
        request.api_user = None