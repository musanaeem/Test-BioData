from django.core.management.base import BaseCommand
from profiles.models import Account
from datetime import date

class Command(BaseCommand):

    def handle(self, *args, **options):
        active_users = Account.objects.filter(is_active=True)

        if active_users:
            for user in active_users:
                date_difference = date.today() - user.last_login.date()
                print(date_difference.days)
                if date_difference.days >=10 and user.is_admin == False:
                    user.is_active = False
                    user.save()


