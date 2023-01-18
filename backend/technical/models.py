from django.db import models
from datetime import datetime, timedelta

class EquipmentGroup(models.Model):
    group_name = models.CharField(max_length=1000)
    equipments = models.ManyToManyField("Equipment", blank=True, related_name="equipments")
    def __str__(self):
        return self.group_name

class Set(models.Model):
    set_name = models.CharField(max_length=1000)
    equipments = models.ManyToManyField("Equipment", blank=True, related_name="equipments_in_set")
    def __str__(self):
        return self.set_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=1000, blank=False, null=False)
    models = models.ManyToManyField("Equipment", blank=True, related_name="models")
    def __str__(self):
        return self.brand_name

class Image(models.Model):
    file_name = models.CharField(max_length=1000, blank=False, null=False)
    file = models.FileField(upload_to="technical_gallery", null=True)
    uploader = models.ForeignKey("station.User",on_delete=models.SET_NULL, blank=True, null=True)
    uploaded = models.DateTimeField(auto_now_add=False, auto_now=False)
    

class Equipment(models.Model):
    name = models.CharField(max_length=1000, blank=False, null=False)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, related_name="brand", blank=True, null=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    serial_no = models.CharField(max_length=100, null=True, blank=True)
    property_no = models.CharField(max_length=100, null=True, blank=True)
    date_acquired = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    purchase_cost = models.IntegerField(null=True, blank=True)
    owner = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    group = models.ForeignKey(EquipmentGroup, on_delete=models.SET_NULL,null=True, blank=True)
    version = models.IntegerField(null=True, blank=True)
    gallery = models.ManyToManyField(Image, blank=True, related_name="gallery")
    avatar = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    set = models.ForeignKey(Set, on_delete=models.SET_NULL, null=True, blank=True, related_name="set")

    def get_brand_name(self):
        return self.brand.brand_name

    def get_group_name(self):
        return self.group.group_name

    def remove_from_current_group(self):
        try:
            self.group.equipments.remove(self)
            self.save()
        except:
            print("no group yet")

    def group_to(self, group):
        self.remove_from_current_group()
        group.equipments.add(self)
        group.save()
        print(self.name + " added to group " + group.group_name)
        self.group = group
        self.save()
        print(self.name + " saved")

    
    def __str__(self):
        return f"{self.name} {self.version}"

# MODELS FOR ENERGY/POWER 

class PowerInterruption(models.Model):
    interrupted = models.DateTimeField(null=False,blank=False)
    restored = models.DateTimeField(null=True,blank=True)
    duration_hours = models.IntegerField(null=True,blank=True)
    duration_minutes = models.IntegerField(null=True,blank=True)
    duration_seconds = models.IntegerField(null=True,blank=True)
    scheduled = models.BooleanField(default=False)
    def set_duration(self):
        if self.restored:
            r = self.restored
            i = self.interrupted
            interrupted = timedelta(days=i.day,hours=i.hour, minutes=i.minute, seconds=i.second)
            restored = timedelta(days=r.day, hours=r.hour, minutes=r.minute, seconds=r.second)
            duration = (restored - interrupted).total_seconds()   
            print("duration", duration)     

            hours,remainder = divmod(duration,3600)
            minutes,seconds = divmod(remainder, 60)
            self.duration_hours = hours
            self.duration_minutes = minutes
            self.duration_seconds = seconds
            self.save()
           
            return True
        else:
            return False
    
    




class PowerConsumption(models.Model):
    date_time = models.DateTimeField(blank=False, null=False)
    meter = models.IntegerField(blank=False, null=False)
    added = models.DateTimeField(auto_now_add=True)
    consumed = models.IntegerField(default=0)
    trend = models.CharField(max_length=20, blank=True, null=True)


    def get_consumption(self,_prev,_pres):
        self.consumed = _pres - _prev
        self.save()
        return self.consumed
        


