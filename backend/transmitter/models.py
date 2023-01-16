from django.db import models

class TXLog(models.Model):
    date = models.DateField()
    time = models.TimeField()
    hour = models.IntegerField(null=True)
    line_voltage = models.FloatField(blank=False, null=False)
    exciter = models.FloatField(blank=False, null=False)
    driver_current = models.FloatField(blank=False, null=False)
    driver_voltage = models.FloatField(blank=False, null=False)
    driver_forward = models.FloatField(blank=False, null=False)
    driver_rf = models.FloatField(blank=False, null=False)
    final_current = models.FloatField(blank=False, null=False)
    final_voltage = models.FloatField(blank=False, null=False)
    final_forward = models.FloatField(blank=False, null=False)
    final_rf = models.FloatField(blank=False, null=False)
    author = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:

        return str(self.date) + "--" + str(self.hour)
    
    def save(self, *args, **kwargs) -> None:
        if self.time:
            self.hour = int(self.time.strftime("%H"))
            
        return super().save(*args, **kwargs)