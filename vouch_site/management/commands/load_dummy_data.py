from django.core.management.base import BaseCommand
from vouch_site.models import Doctor, Condition, City, State, ZipCode
import random

class Command(BaseCommand):
    help = 'Load dummy data into the database'

    def handle(self, *args, **kwargs):
        # Create some conditions
        conditions = ["Diabetes", "Hypertension", "Arthritis", "Asthma", "Epilepsy"]
        condition_objs = []
        for cond in conditions:
            obj, _ = Condition.objects.get_or_create(name=cond)
            condition_objs.append(obj)

        # Create a state and city
        state, _ = State.objects.get_or_create(name="California", code="CA")
        city, _ = City.objects.get_or_create(name="Cityville", state=state)
        zip_obj, _ = ZipCode.objects.get_or_create(code="90210", city=city, latitude=34.0901, longitude=-118.4065)

        # Create dummy doctors
        for i in range(5):
            doctor, created = Doctor.objects.get_or_create(
                name=f"Dr. Test {i}",
                specialty=random.choice(["Cardiology", "Neurology", "Orthopedics"]),
                address=f"{100 + i} Test St, Cityville, CA",
                phone="123-456-7890",
                city=city,
                zip_code=zip_obj,
                image=f"images/doctor{i % 2 + 1}.jpg"
            )
            doctor.conditions_treated.set(random.sample(condition_objs, 2))
            doctor.save()

        self.stdout.write(self.style.SUCCESS('Dummy data loaded successfully!'))
