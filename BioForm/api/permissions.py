from .utils import authenticate_or_get_user
from rest_framework.permissions import BasePermission


class IsJWTAuthenticated(BasePermission):
    message = 'You must be logged in.'

    

    def has_permission(self, request, view):
        
        serializer = authenticate_or_get_user(request)
        if serializer:
            return True
        return False

class IsUsersObject(IsJWTAuthenticated):

    def has_object_permission(self, request, view, obj):
        serializer = authenticate_or_get_user(request)
        return obj.user.id == serializer.data['id']