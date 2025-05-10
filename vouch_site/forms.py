from django import forms
from .models import Specialty, Condition, ZipCode, User
from django_select2.forms import Select2MultipleWidget

# Assuming Condition is your model

class DoctorSearchForm(forms.Form):
    fName = forms.CharField(max_length=100, required=False, label="First Name")
    lName = forms.CharField(max_length=100, required=False, label="Last Name")
    
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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'zip_code', 'conditions']
        widgets = {
            'conditions': Select2MultipleWidget,
        }
        labels = {
            'username': 'Username',
            'email': 'Email',
            'zip_code': 'Zip Code',
            'conditions': 'Conditions',
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']