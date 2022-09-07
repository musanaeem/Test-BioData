from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from profiles.models import Account, AccountManager

# File not used 
""" class AccountBackend(ModelBackend):

    def authenticate(self, request, username = None, password = None, **kwargs):
        UserModel = get_user_model

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        
        try:
            case_insensitive_email = AccountManager.get_by_natural_key(email__iexact=username)

            user = Account.objects.get(email = case_insensitive_email)

        except:
            return
        else:
            if user.check_password(password):
                return user """
