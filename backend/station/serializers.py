from rest_framework import serializers
from .models import User, History, Activity, MonthlyDTR, Position, Station

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)

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

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"

class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"