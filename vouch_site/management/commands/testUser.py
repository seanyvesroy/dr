from django.core.management.base import BaseCommand
from vouch_site.models import Doctor, User, Condition, Endorsement
import random

class Command(BaseCommand):
    help = "Assign conditions to users and populate endorsements based on doctors and matching conditions"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        doctors = Doctor.objects.prefetch_related("conditions_treated").all()
        all_conditions = list(Condition.objects.all())

        # Step 1: Assign 1-3 random conditions to each user
        for user in users:
            if user.conditions.count() == 0:
                assigned = random.sample(all_conditions, k=random.randint(1, min(3, len(all_conditions))))
                user.conditions.set(assigned)
                self.stdout.write(f"Assigned {len(assigned)} condition(s) to {user.username}")

        # Step 2: Create endorsements for doctors treating those conditions
        count = 0
        for user in users:
            for condition in user.conditions.all():
                eligible_doctors = [doc for doc in doctors if condition in doc.conditions_treated.all()]
                if not eligible_doctors:
                    continue

                doctor = random.choice(eligible_doctors)
                if not Endorsement.objects.filter(user=user, doctor=doctor, condition=condition).exists():
                    Endorsement.objects.create(
                        user=user,
                        doctor=doctor,
                        condition=condition,
                        comment=f"Dr. {doctor.name} helped me with {condition.name.lower()}."
                    )
                    count += 1

        self.stdout.write(self.style.SUCCESS(f"Created {count} endorsements."))
