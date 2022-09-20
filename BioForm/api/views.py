import datetime
import jwt
from profiles.models import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *

def serialize_user(user):
    return {
        'username': user.username,
        'email': user.email,
        'date_of_birth': user.date_of_birth,
    }

@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def login(request):
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

    token = jwt.encode(payload, 'secret', algorithm='HS256')

    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'jwt': token
    }

    return response

@api_view(['POST'])
def logout(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'success'
    }
    return response

def authenticate_user(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated User!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated User!')

    user = Account.objects.filter(id=payload['id']).first()
    serializer = LoginSerializer(user)
    
    return serializer

@api_view(['GET'])
def get_user(request):
    user = request.user
    if user.is_authenticated:
        return Response({
            'user_data': serialize_user(user)
        })
    return Response({})

@api_view(['GET'])
def get_bio(request):
    try:
        serializer = authenticate_user(request)
        bio = Bio.objects.filter(user_id=serializer.data['id']).first()
        bio_serializer = BioSerializer(bio)
        return Response(bio_serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_bio(request):
    serializer = authenticate_user(request)

    if Bio.objects.filter(user_id=serializer.data['id']):
        raise Exception('Bio Already Exists! Cannot Add Another')

    bio_serializer = BioSerializer(data=request.data)
    bio_serializer.initial_data['user'] = serializer.data['id']
    bio_serializer.is_valid(raise_exception=True)
    bio_serializer.save()

    return Response({
        'message': 'success',
        'record_entered': bio_serializer.data
    })

@api_view(['PUT'])
def update_bio(request, id):

    try:
        bio = Bio.objects.get(id=id)
        bio_serializer = BioSerializer(instance=bio, data=request.data, partial=True)

        if bio_serializer.is_valid():
            bio_serializer.save()
            return Response(bio_serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_bio(request, id):

    try:
        bio = Bio.objects.get(id=id)
        bio.delete()

        return Response({
            'message' : 'Deletion Successful!'
        })
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_all_blogs(request):
    _ = authenticate_user(request)
    
    try:
        blogs = Blog.objects.all()
        blog_serializer = BlogSerializer(blogs, many=True)
        return Response(blog_serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_users_blogs(request):
    serializer = authenticate_user(request)

    try:
        blogs = Blog.objects.filter(user_id=serializer.data['id'])
        blog_serializer = BlogSerializer(blogs, many=True)
        return Response(blog_serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_blog(request):
    serializer = authenticate_user(request)

    blog_serializer = BlogSerializer(data=request.data)
    blog_serializer.initial_data['user'] = serializer.data['id']
    blog_serializer.is_valid(raise_exception=True)
    blog_serializer.save()

    return Response({
        'message': 'success',
        'record_entered': blog_serializer.data
    })

@api_view(['PUT'])
def update_blog(request, id):

    try:
        blog = Blog.objects.get(id=id)
        blog_serializer = BlogSerializer(instance=blog, data=request.data, partial=True)

        if blog_serializer.is_valid():
            blog_serializer.save()
            return Response(blog_serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_blog(request, id):

    try:
        blog = Blog.objects.get(id=id)
        blog.delete()

        return Response({
            'message' : 'Deletion Successful!'
        })
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

