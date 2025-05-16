from django.contrib import admin
from .models import CustomUser, Profile, Bus, Schedule, Booking
# Register your models here.

admin.site.register([CustomUser, Profile, Bus, Schedule, Booking])
