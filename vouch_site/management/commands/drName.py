from vouch_site.models import Doctor
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Updates the first Doctor with a name and suffix for testing purposes.'

    def handle(self, *args, **options):
        doc = Doctor.objects.first()
        if doc:
            doc.name = "John Doe"
            doc.first_name = "John"
            doc.last_name = "Doe"
            doc.suffix = "MD"
            doc.save()
            self.stdout.write(self.style.SUCCESS('Successfully updated doctor'))
        else:
            self.stdout.write(self.style.ERROR('No doctors found to update'))
