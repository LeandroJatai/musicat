from django.contrib import admin
from musicat.utils import register_all_models_in_admin

# Register your models here.

register_all_models_in_admin(__name__)