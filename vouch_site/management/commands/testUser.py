import random
from django.core.management.base import BaseCommand
from vouch_site.models import Doctor, Endorsement,  User

class Command(BaseCommand):
    help = "Populate sample endorsements for doctors based on the conditions they treat"

    def handle(self, *args, **kwargs):
        doctors = Doctor.objects.prefetch_related('conditions_treated')
        users = list(User.objects.prefetch_related('conditions').all())

        count = 0

        for doctor in doctors:
            for condition in doctor.conditions_treated.all():
                # Find users who have this condition
                matching_users = [user for user in users if condition in user.conditions.all()]

                if not matching_users:
                    continue

                # Pick a random matching user
                user = random.choice(matching_users)

                # Only create endorsement if it doesn’t already exist
                endorsement, created = Endorsement.objects.get_or_create(
                    user=user,
                    doctor=doctor,
                    condition=condition,
                    defaults={'comment': f"{doctor.name} really helped me with {condition.name}!"}
                )
                if created:
                    count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Created {count} new endorsements.'))
