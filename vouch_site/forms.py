from django import forms
from .models import Doctor, Condition, ZipCode

class DoctorSearchForm(forms.Form):
    specialty = forms.ChoiceField(
        choices=[(spec, spec) for spec in Doctor.objects.values_list('specialty', flat=True).distinct()],
        required=False
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
