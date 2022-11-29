from django.contrib import admin
from .models import Equipment,EquipmentGroup, Brand, Image, PowerInterruption, PowerConsumption

# Register your models here.
admin.site.register(Equipment)
admin.site.register(EquipmentGroup)
admin.site.register(Brand)
admin.site.register(Image)
admin.site.register(PowerInterruption)
admin.site.register(PowerConsumption)




