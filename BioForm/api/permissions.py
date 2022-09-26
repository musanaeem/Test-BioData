from email import message
import jwt

from rest_framework.permissions import BasePermission

class IsJWTAuthenticated(BasePermission):
    message = 'You must be logged in.'

    def has_permission(self, request, view):
        
        token = request.COOKIES.get('jwt')

        if token:
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
                if payload:
                    return True
            except jwt.ExpiredSignatureError:
                pass
        return False