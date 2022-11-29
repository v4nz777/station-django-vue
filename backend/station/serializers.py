from rest_framework import serializers
from .models import User, History, Activity, MonthlyDTR

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = "__all__"

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"

class MonthlyDTRSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyDTR
        fields = "__all__"