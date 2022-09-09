from django.core.management.base import BaseCommand
from profiles.models import Account
from datetime import date

class Command(BaseCommand):

    def handle(self, *args, **options):
        count = 0
        active_users = Account.objects.filter(is_active=True)

        if active_users:
            for user in active_users:
                date_difference = date.today() - user.last_login.date()

                if date_difference.days >=10 and user.is_admin == False:
                    count += 1
                    user.is_active = False

                    user.save()
        
        print(f"{count} user(s) were set to inactive")


