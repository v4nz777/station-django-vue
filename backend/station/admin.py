from django.contrib import admin
from .models import User, History,Department, Position, Activity, MonthlyDTR, Station

# Register your models here.
admin.site.register(User)
admin.site.register(History)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Activity)
admin.site.register(MonthlyDTR)
admin.site.register(Station)



