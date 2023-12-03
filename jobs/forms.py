from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',)


class WorkForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ('customer_name', 'print', 'height', 'width', 'unit_price', 'cost')


class CloseRecordForm(forms.ModelForm):
    class Meta:
        model = CloseRecord
        fields = ('name_record', 'total_jobs', 'total_sav', 'total_flex', 'total_cost')


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
