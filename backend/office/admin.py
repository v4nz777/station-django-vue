from django.contrib import admin
from .models import AdVersion, Adcategory, Advertiser, Invoice, InvoiceTransmittal,AudioFile, Ad

# Register your models here.
admin.site.register(AdVersion)
admin.site.register(Ad)
admin.site.register(Adcategory)
admin.site.register(Advertiser)
admin.site.register(AudioFile)
admin.site.register(Invoice)
admin.site.register(InvoiceTransmittal)

