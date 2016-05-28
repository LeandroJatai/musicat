from django.conf.urls import include, url
from core.views import ClasseListView

from .apps import AppConfig


app_name = AppConfig.name


urlpatterns = [
    url(r'^config/classe/$', ClasseListView.as_view(), name='classe_list'),
]
