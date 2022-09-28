from rest_framework.permissions import BasePermission


class IsJWTAuthenticated(BasePermission):
    message = 'You must be logged in.'

    def has_permission(self, request, view):
        return request.api_user
        

class IsUsersObject(IsJWTAuthenticated):

    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'user_id') == getattr(request.api_user, 'id')