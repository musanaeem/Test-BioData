import datetime
import jwt
from profiles.models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .serializers import *
from .permissions import IsJWTAuthenticated

# from rest_framework.decorators import api_view

def serialize_user(user):
    return {
        'username': user.username,
        'email': user.email,
        'date_of_birth': user.date_of_birth,
    }

def get_authenticated_user(request):
    token = request.COOKIES.get('jwt')
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except:
        raise Exception('Not Authenticated')
    user = Account.objects.filter(id=payload['id']).first()
    serializer = LoginSerializer(user)

    return serializer

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
            'jwt': token
        }

        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class BioView(APIView):

    permission_classes = [IsJWTAuthenticated]

    def get(self, request):
        try:
            serializer = get_authenticated_user(request)
            bio = Bio.objects.filter(user_id=serializer.data['id']).first()
            bio_serializer = BioSerializer(bio)
            return Response(bio_serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        serializer = get_authenticated_user(request)

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


    def put(self, request):

        try:
            serializer = get_authenticated_user(request)
            bio = Bio.objects.filter(user_id=serializer.data['id']).first()

            bio_serializer = BioSerializer(instance=bio, data=request.data, partial=True)

            if bio_serializer.is_valid():
                bio_serializer.save()
                return Response(bio_serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def delete(self, request):

        try:
            serializer = get_authenticated_user(request)
            bio = Bio.objects.filter(user_id=serializer.data['id']).first()
            bio.delete()

            return Response({
                'message' : 'Deletion Successful!'
            })
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    

class BlogListView(APIView):

    permission_classes = [IsJWTAuthenticated]

    def get(self, request):
        try:
            blogs = Blog.objects.all()
            blog_serializer = BlogSerializer(blogs, many=True)
            return Response(blog_serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        serializer = get_authenticated_user(request)

        blog_serializer = BlogSerializer(data=request.data)
        blog_serializer.initial_data['user'] = serializer.data['id']
        blog_serializer.is_valid(raise_exception=True)
        blog_serializer.save()

        return Response({
            'message': 'success',
            'record_entered': blog_serializer.data
        })


class BlogUserView(APIView):
    def get(self, request):
        serializer = get_authenticated_user(request)

        try:
            blogs = Blog.objects.filter(user_id=serializer.data['id'])
            blog_serializer = BlogSerializer(blogs, many=True)
            return Response(blog_serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

class BlogDetailedView(APIView):

    def get(self, request, id):
        try:
            blog = Blog.objects.filter(id=id).first()
            blog_serializer = BlogSerializer(blog)
            return Response(blog_serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def put(self, request, id):

        serializer = get_authenticated_user(request)

        try:
            blogs = Blog.objects.filter(user_id=serializer.data['id'])

            blog = blogs.get(id=id)
            blog_serializer = BlogSerializer(instance=blog, data=request.data, partial=True)

            if blog_serializer.is_valid():
                blog_serializer.save()
                return Response(blog_serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, id):

        serializer = get_authenticated_user(request)
        try:
            blogs = Blog.objects.filter(user_id=serializer.data['id'])
            blog = blogs.get(id=id)
            blog.delete()

            return Response({
                'message' : 'Deletion Successful!'
            })
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


'''
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
def user_view(request):
    serializer = authenticate_user(request)
    return Response({
        'user_data': serializer.data
    })

@api_view(['GET'])
def bio_view(request):
    try:
        serializer = authenticate_user(request)
        bio = Bio.objects.filter(user_id=serializer.data['id']).first()
        bio_serializer = BioSerializer(bio)
        return Response(bio_serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def bio_create(request):
    serializer = authenticate_user(request)

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

@api_view(['PUT'])
def bio_update(request, id):

    try:
        serializer = authenticate_user(request)
        bio = Bio.objects.filter(user_id=serializer.data['id']).first()

        bio_serializer = BioSerializer(instance=bio, data=request.data, partial=True)

        if bio_serializer.is_valid():
            bio_serializer.save()
            return Response(bio_serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def bio_delete(request, id):

    try:
        serializer = authenticate_user(request)
        bio = Bio.objects.filter(user_id=serializer.data['id']).first()
        bio.delete()

        return Response({
            'message' : 'Deletion Successful!'
        })
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def user_view(request):
    serializer = authenticate_user(request)
    return Response({
        'user_data': serializer.data
    })


@api_view(['GET'])
def blog_list_view(request):
    _ = authenticate_user(request)
    
    try:
        blogs = Blog.objects.all()
        blog_serializer = BlogSerializer(blogs, many=True)
        return Response(blog_serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def blog_view_user(request):
    serializer = authenticate_user(request)

    try:
        blogs = Blog.objects.filter(user_id=serializer.data['id'])
        blog_serializer = BlogSerializer(blogs, many=True)
        return Response(blog_serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def blog_view(request, id):
    _ = authenticate_user(request)
    
    try:
        blog = Blog.objects.filter(id=id).first()
        blog_serializer = BlogSerializer(blog)
        return Response(blog_serializer.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def blog_create(request):
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
def blog_update(request, id):
    serializer = authenticate_user(request)

    try:
        blogs = Blog.objects.filter(user_id=serializer.data['id'])

        blog = blogs.get(id=id)
        blog_serializer = BlogSerializer(instance=blog, data=request.data, partial=True)

        if blog_serializer.is_valid():
            blog_serializer.save()
            return Response(blog_serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def blog_delete(request, id):
    serializer = authenticate_user(request)
    try:
        blogs = Blog.objects.filter(user_id=serializer.data['id'])
        blog = blogs.get(id=id)
        blog.delete()

        return Response({
            'message' : 'Deletion Successful!'
        })
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

'''