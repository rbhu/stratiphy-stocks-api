from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Generate tokens for existing users'

    def handle(self, *args, **options):
        for user in User.objects.all():
            token, created = Token.objects.get_or_create(user=user)
            print(user.username, ' ', token.key)
        self.stdout.write(self.style.SUCCESS('Tokens generated successfully!'))
