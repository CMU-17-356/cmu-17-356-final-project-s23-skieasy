from django.contrib import admin

from .models import *


admin.site.register(Profile)
admin.site.register(Equipment)
admin.site.register(EquipmentListing)
admin.site.register(EquipmentReservation)
admin.site.register(EquipmentImages)
