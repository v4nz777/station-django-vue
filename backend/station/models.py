
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save, pre_save
from datetime import timedelta, datetime
from datetimerange import DateTimeRange


class User(AbstractUser):
    gender = models.CharField(max_length=20, null=False, blank=False)
    position = models.ForeignKey('Position', on_delete=models.CASCADE, blank=True, null=True, related_name="pos")
    designation = models.ManyToManyField('Department', blank=True, related_name="departments_assigned")
    address = models.CharField(max_length=100, blank=True)
    mobile = models.CharField(max_length=20, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    facebook = models.CharField(max_length=50, blank=True)
    is_in_charge = models.BooleanField(default=False)
    in_charge_of = models.ManyToManyField('Department', blank=True, related_name="departments_headed")
    is_logged = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars")
    position_str = models.CharField(max_length=256,blank=True,null=True)
 

    def save(self, *args, **kwargs):
        if self.pk != None:
            if self.in_charge_of.all().count() >= 1:
                self.is_in_charge = True
            else:
                self.is_in_charge = False
        if self.position != None:
            self.position_str = Position.objects.get(id=self.position.id).title
        super(User, self).save(*args, **kwargs)


def make_default_dict():
    return {"type": ""}
class Activity(models.Model):
    class Meta:
        verbose_name_plural = "Activities"
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name="author")
    username = models.CharField(max_length=50, blank=True, null=True)
    userpic = models.ImageField(blank=True, null=True)
    sub_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="sub_user")
    sub_username = models.CharField(max_length=50, blank=True, null=True)
    sub_userpic = models.ImageField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=False, auto_now=False)
    subject = models.TextField(max_length=300, blank=False, null=False)
    other = models.JSONField(blank=True, null=True, default=make_default_dict)

    def __str__(self):
        return f"{self.user} {self.subject}"
    
    def new_activity(self, username, subject, **kwargs):
        now = datetime.now().replace(tzinfo=None)
        self.created = now
        self.user = User.objects.get(username=username)
        self.subject = subject
        self.other = kwargs
        self.save()

    def save(self, *args, **kwargs):
        self.username = self.user.username
        self.userpic = self.user.avatar
        if self.sub_user:
            self.sub_username = self.sub_user.username
            self.sub_userpic = self.sub_user.avatar
        return super(Activity,self).save(*args, **kwargs)

  



class History(models.Model):
    class Meta:
        verbose_name_plural = "Histories"
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name="on_duty")
    month = models.CharField(max_length=20, blank=True)
    date = models.CharField(max_length=9, blank=True)
    year = models.CharField(max_length=9, blank=True)
    time_in = models.CharField(max_length=9, blank=True)
    time_in_datetime = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    time_in_day = models.CharField(max_length=20, blank=True)
    time_out = models.CharField(max_length=9, blank=True)
    time_out_datetime = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    time_out_day = models.CharField(max_length=20, blank=True)

    total = models.CharField(max_length=50, blank=True)
    total_in_hr = models.CharField(max_length=50, blank=True)
    total_in_mn = models.CharField(max_length=50, blank=True)

    overtime = models.CharField(max_length=50, blank=True)
    ot_in_hr = models.CharField(max_length=50, blank=True)
    ot_in_mn = models.CharField(max_length=50, blank=True)

    night_diff = models.CharField(max_length=50, blank=True)
    nd_in_hr = models.CharField(max_length=50, blank=True)
    nd_in_mn = models.CharField(max_length=50, blank=True)

    completed = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        
        if self.time_in_datetime and self.time_out_datetime:
            self.completed = True
            t_in = self.time_in_datetime.replace(tzinfo=None)
            t_out = self.time_out_datetime.replace(tzinfo=None)
            self.month = t_in.strftime("%B")
            self.year = t_in.strftime("%Y")
            self.date = t_in.strftime("%d")
            self.time_in_day = t_in.strftime("%A")
            self.time_out_day = t_out.strftime("%A")
            total = t_out - t_in

            # Convert to human readable
            s = total.total_seconds()
            hours, remainder = divmod(s, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.total_in_hr = int(hours)
            self.total_in_mn = int(minutes)

            sfx_mn = "" if minutes <= 1 else "s"
            sfx_hr = "" if hours <= 1 else "s"
            self.total = (f"{int(hours)}hr{sfx_hr}, {int(minutes)}min{sfx_mn}")

            self.in_as_twelve_hr_format(t_in)
            self.out_as_twelve_hr_format(t_out)
            self.calculate_overtime(total)
            self.calculate_night_diff(t_in,t_out)
        else:
            t_in = self.time_in_datetime.replace(tzinfo=None)
            self.month = t_in.strftime("%B")
            self.year = t_in.strftime("%Y")
            self.date = t_in.strftime("%d")
            self.time_in_day = t_in.strftime("%A")
        return super(History,self).save(*args, **kwargs)

    def in_as_twelve_hr_format(self, t_in):
        self.time_in = t_in.strftime('%I:%M %p')

    def out_as_twelve_hr_format(self, t_out):
        self.time_out = t_out.strftime('%I:%M %p')

    def calculate_overtime(self, total):
        # if total time exceeds 8 hours // 28800 seconds
            # for overtime
        if total.total_seconds() > 28800:
            t = datetime.strptime("08:00:00", "%H:%M:%S")
            eight_hours = timedelta(hours=t.hour, minutes=t.minute)
            overtime = total - eight_hours

            # Convert to human readable
            s = overtime.total_seconds()
            hours, remainder = divmod(s, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.ot_in_hr = int(hours)
            self.ot_in_mn = int(minutes)

            sfx_mn = "" if minutes <= 1 else "s"
            sfx_hr = "" if hours <= 1 else "s"
            self.overtime = (f"{int(hours)}hr{sfx_hr}, {int(minutes)}min{sfx_mn}")
    
    def calculate_night_diff(self,t_in,t_out):

        # if has worked between 10pm to 6am
        # for night differential
        night = [22,23,0,1,2,3,4,5,6]
        valid_night_shifts = []
        in_out_range = DateTimeRange(t_in, t_out).range(timedelta(hours=1))
        for inx,i in enumerate(in_out_range):
            if i.hour in night:
                # 6am oclocks
                if i.hour == 6:
                    if i.hour == t_in.hour:
                        valid_night_shifts.append({
                            "datetime": i,
                            "time": timedelta(hours=i.hour, minutes=0),
                            "duration": timedelta(hours=0, minutes=0)
                        })
                    elif i.hour == t_out.hour:
                        valid_night_shifts.append({
                            "datetime": t_out,
                            "time": timedelta(hours=t_out.hour, minutes=0),
                            "duration": timedelta(hours=0, minutes=(60-t_in.minute))
                        })
                    else:
                        valid_night_shifts.append({
                            "datetime": i,
                            "time": timedelta(hours=i.hour, minutes=0),
                            "duration": timedelta(hours=0, minutes=(60-t_in.minute))
                        })
                # 10pm oclocks
                elif i.hour == 22:
                    if i.hour == t_in.hour:
                        valid_night_shifts.append({
                        "datetime": i,
                        "time": timedelta(hours=i.hour, minutes=t_in.minute),
                        "duration": timedelta(hours=0, minutes=t_in.minute)
                        })
                    elif i.hour == t_out.hour:
                        valid_night_shifts.append({
                        "datetime": i,
                        "time": timedelta(hours=i.hour, minutes=t_out.minute),
                        "duration": timedelta(hours=0, minutes=(t_out.minute-t_in.minute))
                        })
                    else:
                        valid_night_shifts.append({
                            "datetime": i,
                            "time": timedelta(hours=i.hour, minutes=0),
                            "duration": timedelta(hours=0, minutes=i.minute)
                        })
                
                # other oclocks
                else:
                    if i.hour == t_in.hour:
                            valid_night_shifts.append({
                            "datetime": i,
                            "time": timedelta(hours=i.hour, minutes=i.minute),
                            "duration": timedelta(hours=0, minutes=0)
                        })
                    elif i.hour == t_out.hour:
                        valid_night_shifts.append({
                            "datetime": i,
                            "time": timedelta(hours=t_out.hour, minutes=t_out.minute),
                            "duration": timedelta(hours=1, minutes=(t_out.minute-t_in.minute))
                        })
                    else:
                        valid_night_shifts.append({
                            "datetime": i,
                            "time": timedelta(hours=i.hour, minutes=i.minute),
                            "duration": timedelta(hours=1, minutes=0)
                        })

        # Append the timeout time even if its less than an hour...
        # Fix for datetimerange not included the tiemout if its less than 60 minutes.
        if t_out.minute < t_in.minute:
            if t_out.hour in night:
                if t_out.hour == 6:
                    valid_night_shifts.append({
                        "datetime": t_out,
                        "time": timedelta(hours=t_out.hour, minutes=0),
                        "duration": timedelta(hours=0, minutes=(60-t_in.minute))
                    })
                else:
                    valid_night_shifts.append({
                        "datetime": t_out,
                        "time": timedelta(hours=t_out.hour, minutes=t_out.minute),
                        "duration": timedelta(hours=0, minutes=60-(t_in.minute-t_out.minute))
                    })


        sum_of_night_shifts = sum([d["duration"] for d in valid_night_shifts],timedelta())
        # Convert to human readable
        # then save to database
        s = sum_of_night_shifts.total_seconds()
        hours, remainder = divmod(s, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.nd_in_hr = int(hours)
        self.nd_in_mn = int(minutes)

        sfx_mn = "" if minutes <= 1 else "s"
        sfx_hr = "" if hours <= 1 else "s"
        if int(s) > 60:
            self.night_diff = (f"{int(hours)}hr{sfx_hr}, {int(minutes)}min{sfx_mn}")
        else:
            pass

    def __str__(self):
        return f"{self.user.username} @ {self.time_in_datetime.hour}:{self.time_in_datetime.minute}//{self.month}-{self.date}-{self.year}"

class MonthlyDTR(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    range_start = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    range_end = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    file = models.FileField(upload_to="dtr")
    def save(self,*args, **kwargs):
        month = self.range_start.strftime("%B")
        start = self.range_start.strftime("%d")
        end = self.range_end.strftime("%d")
        year = self.range_end.strftime("%Y")
        self.title = f"{self.username}'s {month} {start}-{end} {year}"
        return super(MonthlyDTR,self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Department(models.Model):
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(max_length=300, blank=True)
    head = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="in_charge")
    users = models.ManyToManyField(User, blank=True)
    def __str__(self):
        return self.title

class Position(models.Model):
    title = models.CharField(max_length=30, blank=False, unique=True)
    salary_1 = models.IntegerField(blank=True, null=True)
    salary_2 = models.IntegerField(blank=True, null=True)
    salary_3 = models.IntegerField(blank=True, null=True)
    salary_4 = models.IntegerField(blank=True, null=True)
    salary_5 = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.title







# IF DEPARTMENT IS DESIGNATED TO USER, ADD USER TO THE DEPARTMENT
# IF DEPARTMENT IS UNDESIGNATED TO USER, REMOVE USER TO THE DEPARTMENT

@receiver(m2m_changed, sender=User.designation.through)
def department_designate(sender, instance, action, **kwargs):
    if action == 'post_add':
        _department = instance.designation.all()
        for i in _department:
            i.users.add(instance)

    if action == 'pre_remove':
        _department = instance.designation.all()
        for i in _department:
            i.users.remove(instance)

   