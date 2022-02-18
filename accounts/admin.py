from django.contrib import admin
from .models import *

my_models = (Paginas, Perfiles)

admin.site.register(my_models)
