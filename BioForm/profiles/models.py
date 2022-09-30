from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify

from django.db import models
import datetime

#User Manager Model
class AccountManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            **extra_fields
        )

        user.password = make_password(password)
        user.save(using = self.db)

        return user

    def create_superuser(self, email, username, password = None, **extra_fields):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            **extra_fields
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self.db)

        return user

    def atomic_create_user(self, email, username, password=None, **extra_fields):
        user = self.create_user(email, username, password, **extra_fields)
        return user
    
    def get_by_natural_key(self, email):
        return self.get(email__iexact=email)

# Custom User Model
class Account(AbstractBaseUser):

    email = models.EmailField(verbose_name = 'email', max_length = 60, unique = True)
    username = models.CharField(max_length = 30, unique = True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add = True)
    last_login = models.DateTimeField(verbose_name = 'last login', auto_now = True)
    date_of_birth = models.DateField(verbose_name = 'date of birth')
    age = models.IntegerField(null=True, blank= True)
    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'date_of_birth']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    # Over ride save function to do something before it is saved
    def save(self, *args, **kwargs):
        self.age = int((datetime.datetime.now().date() - self.date_of_birth).days / 365.25)
        super().save(*args, **kwargs)



class Bio(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)

class Blog(models.Model):
    title = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=400, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now= True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created']





# Create your models here.
