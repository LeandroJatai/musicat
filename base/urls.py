

from .apps import AppConfig


app_name = AppConfig.name


urlpatterns = [
]

# Fix a static asset finding error on Django 1.9 + gunicorn:
# http://stackoverflow.com/questions/35510373/
# urlpatterns += staticfiles_urlpatterns()
