from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Fieldset, Layout
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from musicat.settings import MAX_IMAGE_UPLOAD_SIZE


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(
                                attrs={
                                 'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(
                                attrs={
                                 'class': 'form-control', 'name': 'password'}))
