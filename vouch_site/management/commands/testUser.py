from django.core.management.base import BaseCommand
from vouch_site.models import User  # <--- use your custom User model!!

class Command(BaseCommand):
    help = 'Create a test user for login testing.'

    def handle(self, *args, **kwargs):
        username = "testuser"
        email = "testuser@example.com"
        password = "password123"

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Test user '{username}' created with password '{password}'"))
        else:
            self.stdout.write(self.style.WARNING(f"Test user '{username}' already exists."))
