from django.contrib.auth import get_user_model
from profiles.models import *
from rest_framework import serializers, validators

Account = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('username', 'password', 'email', 'date_of_birth')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {
                'required': True,
                'allow_blank': False,
                'validators': [
                    validators.UniqueValidator(
                        Account.objects.all(), f'A user with that Email already exists.'
                    )
                ],
            },
        }

    def create(self, validated_data):

        user = Account.objects.atomic_create_user(username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            date_of_birth = validated_data['date_of_birth'])
        return user

class BioSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username')
    class Meta:
        model = Bio
        fields = ['name','user_username', 'user', 'address', 'description']

class BlogSerializer(serializers.ModelSerializer):
    user_username = serializers.SerializerMethodField('_get_account_username')
    #serializers.SerializerMethodField('_get_account_username')

    #serializers.CharField(source='user.username')

    def _get_account_username(self, blog_obect):
        user = getattr(blog_obect, 'user')
        username = getattr(user, 'username')
        return username

    class Meta:
        model = Blog
        fields = ['id', 'user', 'title', 'content', 'created', 'user_username']