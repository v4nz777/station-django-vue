from rest_framework import serializers
from .models import Equipment, EquipmentGroup, Brand, Image, PowerConsumption, PowerInterruption, InventoryExport

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"

class EquipmentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentGroup
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

class PowerConsumptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerConsumption
        fields = "__all__"

class PowerInterruptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerInterruption
        fields = "__all__"

class InventoryExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryExport
        fields = "__all__"