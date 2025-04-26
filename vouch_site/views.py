from django.shortcuts import render
from .models import Doctor
from .forms import DoctorSearchForm

def index(request):
    return render(request, "vouch/index.html")
def search(request):
    doctors = Doctor.objects.all()
    if request.method == "POST":
        form = DoctorSearchForm(request.POST)
        if form.is_valid():
            specialty = form.specialty
            condition = form.conditions
            distance = form.distance
        if specialty:
            doctors = doctors.filter(specialty__iexact=specialty)
        if condition:
            doctors = doctors.filter(conditions__name__iexact=condition)  # adjust if M2M
        if distance:
        # You need to handle location filtering separately (see note below)
            pass
    else:
            
        form = DoctorSearchForm()
    return render(request, "vouch/search.html",{'form':form})
def login(request):
    return render(request, "vouch/login.html")
