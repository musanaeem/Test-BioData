import jwt
from profiles.models import Account
from .serializers import LoginSerializer

def authenticate_user(request):
    token = request.COOKIES.get('jwt')
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = Account.objects.filter(id=payload['id']).first()
    
        if user:
            serializer = LoginSerializer(user)    
            return serializer
    except:
        pass
    return None