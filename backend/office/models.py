from django.db import models

class Ad(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=False)
    contract = models.CharField(max_length=50, unique=True, blank=False)
    type = models.CharField(max_length=50, unique=False, blank=False)
    bo_number = models.CharField(max_length=50, unique=False, blank=True)
    advertiser = models.ForeignKey('Advertiser', on_delete=models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey('Adcategory', on_delete=models.SET_NULL, blank=True, null=True)
    versions = models.ManyToManyField("AdVersion", related_name="ads")
    ad_avatar = models.ImageField(upload_to="ads_avatars", blank=True, null=True)
    # current_ver = models.CharField(max_length=50, blank=False)
    current_ver = models.IntegerField(blank=False, null=True)
    
    def __str__(self):
        return f"{self.title} #{self.contract}"


class AdVersion(models.Model):
    # title = models.CharField(max_length=50, unique=True, blank=False)
    # contract = models.CharField(max_length=50, unique=True, blank=False)
    # type = models.CharField(max_length=50, unique=False, blank=False)
    # bo_number = models.CharField(max_length=50, unique=False, blank=True)
    # advertiser = models.ForeignKey('Advertiser', on_delete=models.SET_NULL, blank=True, null=True)
    # category = models.ForeignKey('Adcategory', on_delete=models.SET_NULL, blank=True, null=True)
    # ad_avatar = models.ImageField(upload_to="ads_avatars", blank=True, null=True)
    
    name = models.CharField(max_length=50, blank=False)
    # version = models.CharField(max_length=50, blank=False)
    version = models.IntegerField(blank=False)
    running = models.BooleanField(default=True)
    amount = models.FloatField(blank=False)
    account_executive = models.CharField(max_length=200)
    pricing = models.CharField(max_length=20)
    ex_deal = models.BooleanField(default=False)
    package = models.ForeignKey('Package',on_delete=models.SET_NULL, null=True, blank=True)
    broadcast_start = models.DateField(null=True, blank=True)
    broadcast_end = models.DateField(null=True, blank=True)

    ad_spots = models.IntegerField(blank=False)
    schedule = models.TextField(max_length=500, blank=True)

    files = models.ManyToManyField("AudioFile",related_name="files")
    material_duration = models.IntegerField(blank=True, null=True)

    has_tagline = models.BooleanField(default=False)

    aob_spots = models.IntegerField(null=True)
    tc_spots = models.IntegerField(null=True)
    ss_spots = models.IntegerField(null=True)

    aob_sched = models.CharField(max_length=1000,blank=True, null=True)
    tc_sched = models.CharField(max_length=1000,blank=True, null=True)
    ss_sched = models.CharField(max_length=1000,blank=True, null=True)
    
    remarks = models.TextField(max_length=500, blank=True)

    added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class AudioFile(models.Model):
    from_ad = models.ForeignKey(AdVersion, on_delete=models.CASCADE, related_name="file")
    filename = models.CharField(max_length=500,blank=False, null=False)
    file = models.FileField(upload_to="ads_materials", null=True)
    duration = models.IntegerField(blank=True, null=True)

class Advertiser(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    address = models.CharField(max_length=100, blank=True)
    ads = models.ManyToManyField(AdVersion, blank=True, related_name="ads_owned")
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Adcategory(models.Model):
    title = models.CharField(max_length=50, unique=True)
    ads = models.ManyToManyField(AdVersion, blank=True, related_name="ads_under")

    def __str__(self):
        return self.title

class Invoice(models.Model):
    advertiser = models.ForeignKey(Advertiser, on_delete=models.SET_NULL, null=True)
    from_contract = models.CharField(max_length=100, blank=False)
    # account_executive = models.ForeignKey('station.User', on_delete=models.SET_NULL, null=True)
    account_executive = models.CharField(max_length=200)
    for_ads = models.ManyToManyField(AdVersion, blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    invoice_no = models.CharField(max_length=50, blank=False)
    
    paid = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    amount = models.FloatField(blank=True, null=True)
    amount_received = models.FloatField(blank=True, null=True)

    or_date = models.DateField(null=True, blank=True)
    or_number = models.CharField(max_length=50, blank=True, null=True)
    applicable_month_from = models.DateField(null=True, blank=True)
    applicable_month_to = models.DateField(null=True, blank=True)

    file = models.FileField(upload_to="invoices", blank=True, null=True)

    deposited = models.BooleanField(default=False)
    deposit_slip = models.ImageField(upload_to="bank_deposits", blank=True, null=True)

    def __str__(self):
        return f'{self.invoice_date}|{self.from_contract}'




class InvoiceTransmittal(models.Model):
    month = models.CharField(max_length=100, blank=False)
    year = models.CharField(max_length=5, blank=False)
    invoices = models.ManyToManyField(Invoice, blank=True)

    def __str__(self):
        return self.month


class Package(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    description = models.CharField(max_length=1512, null=True, blank=True)
    price = models.FloatField(blank=False, null=False)
    pricing = models.CharField(max_length=256, null=False, blank=False)
    duration_of_pricing = models.IntegerField(blank=False,null=False)
    spots_per_day = models.IntegerField(blank=False,null=False)
    aob_per_day = models.IntegerField(blank=True,null=True)
    tc_per_day = models.IntegerField(blank=True,null=True)
    ss_per_day = models.IntegerField(blank=True,null=True)
    material_duration = models.FloatField(blank=False,null=False)
    author = models.CharField(max_length=256, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    ads = models.ManyToManyField(Ad, blank=True)
    theme = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    def verify(self, name, description, price, pricing, duration_of_pricing, spots_per_day, aob_per_day, tc_per_day, ss_per_day,material_duration):
        _name = name == self.name
        _description = description == self.description
        _price = price == self.price
        _pricing = pricing == self.pricing
        _duration_of_pricing = duration_of_pricing == self.duration_of_pricing
        _spots_per_day = spots_per_day == self.spots_per_day
        _aob_per_day = aob_per_day == self.aob_per_day
        _tc_per_day = tc_per_day == self.tc_per_day
        _ss_per_day = ss_per_day == self.ss_per_day
        _material_duration = material_duration == self.material_duration

        return _name and _description and _price and _pricing and _duration_of_pricing and _spots_per_day and _aob_per_day and _tc_per_day and _ss_per_day and _material_duration
    
