from django.core.management.base import BaseCommand
from profiles.models import Account
from datetime import datetime, timedelta

class Command(BaseCommand):

    def handle(self, *args, **options):
        days_offline = 10

        inactive_users_queryset = Account.objects.filter(last_login__lte=datetime.now()-timedelta(days=days_offline))
        inactive_users_count = inactive_users_queryset.count()
        inactive_users_queryset.update(is_active=False)
        
        print(f"{inactive_users_count} user(s) were set to inactive")