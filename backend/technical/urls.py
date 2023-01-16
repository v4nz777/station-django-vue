from django .urls import path
from . import views

urlpatterns = [
    path("add_equipment",views.newEquipment, name="newEquipment"),
    path("new_group",views.addNewGroup, name="addNewGroup"),
    path("seach_brand/<str:keyword>",views.searchBrand, name="searchBrand"),
    path("seach_group/<str:keyword>",views.searchGroup, name="searchGroup"),
    path("check_name/<str:name>",views.checkName, name="checkName"),
    path("check_group/<str:group_name>",views.checkGroup, name="checkGroup"),
    path("equipment_groups/<str:filter>",views.filterGroups, name="filterGroups"),
    path("equipment/<int:id>",views.getEquipment, name="getEquipment"),
    path("brand/<int:id>",views.getBrand, name="getBrand"),
    path("group/<int:id>",views.getGroup, name="getGroup"),
    path("equipment_image/<int:id>",views.getImage, name="getImage"),
    path("eq_upload",views.savePictures, name="savePictures"),
    path("set_eq_avatar/<int:equipment_id>/<int:pic_id>",views.setEquipmentAvatar, name="setEquipmentAvatar"),
    path("group_to/<int:group_id>",views.groupEquipment, name="groupEquipment"),
    path("delete_items",views.deleteEquipments, name="deleteEquipments"),
    path("change_item_status",views.newStatus, name="newStatus"),
    path("new_power_interruption",views.newPowerInterruption, name="newPowerInterruption"),
    path("new_power_reading",views.newPowerConsumption, name="newPowerConsumption"),
    path("get_power_readings",views.getPowerConsumptions, name="getPowerConsumptions"),
    path("get_power_interruptions",views.getPowerInterruptions, name="getPowerInterruptions"),
]
