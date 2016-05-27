from django.conf.urls import url
from django.contrib.auth import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView

from .apps import AppConfig
from .forms import LoginForm

app_name = AppConfig.name


urlpatterns = [

]

# Fix a static asset finding error on Django 1.9 + gunicorn:
# http://stackoverflow.com/questions/35510373/
urlpatterns += staticfiles_urlpatterns()
