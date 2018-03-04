from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Garden)
admin.site.register(GardenAddress)
admin.site.register(GardenAddressType)
