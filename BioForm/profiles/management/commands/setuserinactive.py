from django.core.management.base import BaseCommand
from profiles.models import Account
from datetime import datetime, timedelta

class Command(BaseCommand):

    def handle(self, *args, **options):
        days_offline = 10

        inactive_users = Account.objects.filter(last_login__lte=datetime.now()-timedelta(days=days_offline))

        if inactive_users:
            for user in inactive_users:
                
                count += 1
                user.is_active = False

                user.save()
        
        print(f"{count} user(s) were set to inactive")


