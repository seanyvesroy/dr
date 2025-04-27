from django import forms
from .models import Specialty, Condition, ZipCode, User

class DoctorSearchForm(forms.Form):
    specialty = forms.ModelChoiceField(
        queryset=Specialty.objects.all(),
        required=False,
        empty_label="Select a Specialty"
    )

    conditions_treated = forms.ModelChoiceField(
        queryset=Condition.objects.all(),
        required=False,
        empty_label="Select a Condition"
    )

    zip_code = forms.ModelChoiceField(
        queryset=ZipCode.objects.all(),
        required=False,
        empty_label="Select a Zip Code"
    )
