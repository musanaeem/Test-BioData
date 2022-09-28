import datetime
import jwt
from profiles.models import *
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .serializers import *
from .permissions import IsJWTAuthenticated, IsUsersObject
from django.shortcuts import get_object_or_404


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = Account.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
        }

        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success',
        }
        return response


class BioView(APIView):

    permission_classes = [IsJWTAuthenticated]

    def get(self, request):
        
        serializer = request.api_user
        bio = get_object_or_404(Bio, user_id=serializer.data['id'])
        bio_serializer = BioSerializer(bio)
        return Response(bio_serializer.data)
        


    def post(self, request):
        serializer = request.api_user

        if Bio.objects.filter(user_id=serializer.data['id']):
            return Response(
                    {'detail': 'Bio already exists!',
                    'status': '400'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        bio_serializer = BioSerializer(data=request.data)
        bio_serializer.initial_data['user'] = serializer.data['id']
        bio_serializer.is_valid(raise_exception=True)
        bio_serializer.save()

        return Response({
            'message': 'success',
            'record_entered': bio_serializer.data
        })


    def patch(self, request):

        
        serializer = request.api_user
        bio = get_object_or_404(Bio, user_id=serializer.data['id'])

        bio_serializer = BioSerializer(instance=bio, data=request.data, partial=True)

        if bio_serializer.is_valid():
            bio_serializer.save()
            return Response(bio_serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        


    def delete(self, request):

        
        serializer = request.api_user
        bio = get_object_or_404(Bio, user_id=serializer.data['id'])
        bio.delete()

        return Response({
            'message' : 'Deletion Successful!'
        })
        
   
class BlogViewSet(viewsets.ModelViewSet):

    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def get_permissions(self):
        action_list = ['list', 'get', 'post', 'retrieve']
        if self.action in action_list:
            permission_classes = [IsJWTAuthenticated]
        else:
            permission_classes = [IsUsersObject]
        return [permission() for permission in permission_classes]