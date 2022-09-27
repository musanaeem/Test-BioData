from rest_framework.permissions import BasePermission


class IsJWTAuthenticated(BasePermission):
    message = 'You must be logged in.'

    def has_permission(self, request, view):
        serializer = request.api_user
        if serializer:
            return True
        return False

class IsUsersObject(IsJWTAuthenticated):

    def has_object_permission(self, request, view, obj):
        serializer = request.api_user
        return obj.user.id == serializer.data['id']