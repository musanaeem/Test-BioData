from rest_framework.permissions import BasePermission


class IsJWTAuthenticated(BasePermission):
    message = 'You must be logged in.'

    def has_permission(self, request, view):
        return request.api_user is not None
        

class IsUsersObject(IsJWTAuthenticated):

    def has_object_permission(self, request, view, obj):
        if request.api_user:
            return getattr(obj, 'user_id') == getattr(request.api_user, 'id')
        return False