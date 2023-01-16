from rest_framework import serializers
from .models import TXLog

class TXLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TXLog
        fields = "__all__"
