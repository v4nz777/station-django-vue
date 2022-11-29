from dataclasses import field
from rest_framework import serializers
from .models import AdVersion, Ad, Adcategory, Advertiser,AudioFile, Invoice
class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"
class AdVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdVersion
        fields = "__all__"

class AdvertiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertiser
        fields = "__all__"
class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = "__all__"

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"