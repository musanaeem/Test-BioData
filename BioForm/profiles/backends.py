from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

from profiles.models import Account, AccountManager
from django.contrib import messages


class AccountBackend(ModelBackend):

    def authenticate(self, request, username = None, password = None, **kwargs):
        UserModel = get_user_model

        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        
        try:
            case_sensitive_email = AccountManager.get_by_natural_key(email__iexact=username)

            user = Account.objects.get(email = case_sensitive_email)
            
        except:
            return
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
