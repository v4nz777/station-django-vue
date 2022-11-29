from django.contrib import admin
from .models import User, History,Department, Position, Activity, MonthlyDTR

# Register your models here.
admin.site.register(User)
admin.site.register(History)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Activity)
admin.site.register(MonthlyDTR)


