from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from datetime import datetime

from .serializers import (EquipmentSerializer,
                            EquipmentGroupSerializer,
                            BrandSerializer,
                            ImageSerializer,
                            PowerConsumptionSerializer,
                            PowerInterruptionSerializer)
from .models import (Equipment,
                    EquipmentGroup,
                    Brand,
                    Image,
                    PowerInterruption,
                    PowerConsumption)

from station.models import User
from station.models import Activity



"""
This function will recieve data from api: "add_equipment/".
Will save equipments info to the database
"""
@api_view(["POST"])
def newEquipment(request):
    data = request.data
    _name = data["name"].lower()
    _brand = data["brand"].lower()
    _model = data["model"]
    _serial_no = data["serial_no"]
    _property_no = data["property_no"]
    _purchase_cost = int(data["purchase_cost"])
    _owner = data["owner"]
    _status = data["status"]
    _date_acquired = datetime.strptime(data["date_acquired"],"%Y-%m-%d")
    _group = data["group"].lower()



    #Get Brand
    try:
        brand = Brand.objects.get(brand_name=_brand)
    except ObjectDoesNotExist:
        brand = Brand(brand_name=_brand)
        brand.save()

    
    #Get Group
    try:
        group = EquipmentGroup.objects.get(group_name=_group)
    except ObjectDoesNotExist:
        group = EquipmentGroup(group_name=_group)
        group.save()


    #Make equipment instance
    try:
        #add tailing number if already existed
        search_equipment = Equipment.objects.get(name = _name)
        # custom_name = _name + " " + str(search_equipment.version + 1)
        # equipment = Equipment(
        #     name=custom_name,
        #     brand=brand,
        #     model=_model,
        #     serial_no=_serial_no,
        #     property_no=_property_no,
        #     date_acquired=_date_acquired,
        #     purchase_cost=_purchase_cost,
        #     owner=_owner,
        #     status=_status,
        #     group=group
        # )
        # equipment.save()

    except ObjectDoesNotExist:
        equipment = Equipment(
            name=_name,
            brand=brand,
            model=_model,
            serial_no=_serial_no,
            property_no=_property_no,
            date_acquired=_date_acquired,
            purchase_cost=_purchase_cost,
            owner=_owner,
            status=_status,
            group=group
        )
        equipment.save()
    
    # list model to brand
    brand.models.add(equipment)
    brand.save()

    #list equipment to group
    group.equipments.add(equipment)
    group.save()

    #save activity
   
    activity = Activity()
    activity.new_activity(
        data["user"],
        f"added an equipment: {brand.brand_name} {_model} to inventory",
        type="inventory"
    )
    
   


    return Response({
        "message": "success!"
    })

"""
Upload pictures to database
api: "eq_upload"
"""
@api_view(["POST"])
def savePictures(request):
    data = request.data
    uploader = data["uploader"]
    equipment = Equipment.objects.get(id=int(data["equipment"]))

    for image in data.getlist("uploads"):
        img = Image(
            file_name=image.name,
            file = image,
            uploader = User.objects.get(username=uploader),
            uploaded=datetime.now()
        )
        img.save()
        equipment.gallery.add(img)
        equipment.save()

    return Response({"message":"posted"})

"""
set avatar
api: "set_eq_avatar/<int:equipmentID>/<int:picID>"
"""
@api_view(["PUT"])
def setEquipmentAvatar(request,equipment_id,pic_id):
    eq = Equipment.objects.get(id=equipment_id)
    pic = Image.objects.get(id=pic_id)

    eq.avatar = pic
    eq.save()
    return Response({"message":"success"})


"""
move to group
api: "group_to/<int:group_id>"
"""
@api_view(["PUT"])
def groupEquipment(request,group_id):
    group = EquipmentGroup.objects.get(id=group_id)
    data = request.data
    
    for equipment in data.getlist("equipments"):
        eq = Equipment.objects.get(id=int(equipment))
        eq.group_to(group)
    return Response({"message":"success"})
    
"""
delete item
api: "delete_items"
"""
@api_view(["POST"])
def deleteEquipments(request):
    data = request.data

    for i in data.getlist("delete_equipments"):
        item = Equipment.objects.get(id=int(i))
        item.delete()
    
    return Response({"message":"delete success"})



"""
change item status
api: "change_item_status"
"""
@api_view(["PUT"])
def newStatus(request):
    data = request.data

    for i in data.getlist("equipments"):
        item = Equipment.objects.get(id=int(i))
        item.status = data["status"]
        item.save()
    
    return Response({"message":f"new status applied"})


"""
add new group
api: "new_group"
"""
@api_view(["POST"])
def addNewGroup(request):
    data = request.data
    new_group = str(data["new_group"]).lower()
    EquipmentGroup(group_name=new_group).save()
    return Response({"message":"new group created"})



""" 
🔎Search query for brands
🔑Use api: "seach_brand/<str:keyword>"
"""
@api_view(["GET"])
def searchBrand(request, keyword):
    try:
        query = Brand.objects.filter(brand_name__icontains=keyword)
        serializer = BrandSerializer(query, many=True)
        return Response(serializer.data, status=200)

    except ObjectDoesNotExist:
        return Response({"message":"search not found"}, status=404)



""" 
🔎Search query for groups
🔑Use api: "seach_group/<str:keyword>"
"""
@api_view(["GET"])
def searchGroup(request, keyword):
    try:
        query = EquipmentGroup.objects.filter(group_name__icontains=keyword)
        serializer = EquipmentGroupSerializer(query, many=True)
        return Response(serializer.data, status=200)

    except ObjectDoesNotExist:
        return Response({"message":"search not found"}, status=404)


"""
🔎For checking if the name already exist
🔑 Use api: "check_name"
"""
@api_view(["GET"])
def checkName(request, name):
    _name = name.lower()
    try:
        Equipment.objects.get(name=_name)
        return Response({"message": f"name: {_name} is taken", "taken": True})
    except ObjectDoesNotExist:
        return Response({"message": f"name: {_name} is avaialble", "taken": False})
"""
🔎For checking if the group already exist
🔑 Use api: "check_group/<str:group_name>"
"""
@api_view(["GET"])
def checkGroup(request, group_name):
    _name = group_name.lower()
    try:
        EquipmentGroup.objects.get(group_name=_name)
        return Response({"message": f"group: {_name} is taken", "taken": True})
    except ObjectDoesNotExist:
        return Response({"message": f"group: {_name} is avaialble", "taken": False})

"""
🔎Filter list of groups
🔑api: "equipment_groups/<str:filter>"
"""
@api_view(["GET"])
def filterGroups(request, filter):
    if filter == "all":
        groups = EquipmentGroup.objects.all()
        serializer = EquipmentGroupSerializer(groups, many=True)
        return Response(serializer.data)
   

"""
Get equipment by id
api: "equipment/<int:id>"
"""
@api_view(["GET"])
def getEquipment(request, id):
    equipment = Equipment.objects.get(id=id)
    serializer = EquipmentSerializer(equipment)
    return Response(serializer.data) 

"""
Get Brand
api: "brand/<int:id>"
"""
@api_view(["GET"])
def getBrand(request, id):
    brand = Brand.objects.get(id=id)
    serializer = BrandSerializer(brand)
    return Response(serializer.data) 
    
"""
Get Group
api: "group/<int:id>"
"""
@api_view(["GET"])
def getGroup(request, id):
    group = EquipmentGroup.objects.get(id=id)
    serializer = EquipmentGroupSerializer(group)
    return Response(serializer.data) 
    
"""
Get Image
api: "equipment_image/<int:id>"
"""
@api_view(["GET"])
def getImage(request, id):
    image = Image.objects.get(id=id)
    serializer = ImageSerializer(image)
    return Response(serializer.data) 


"""
POWER INTERRUPTIONS
"""

@api_view(["POST","PUT"])
def newPowerInterruption(request):
    data = request.data
    interrupted = datetime.strptime(data["interrupted"],"%Y-%m-%dT%H:%M")
    restored = datetime.strptime(data["restored"],"%Y-%m-%dT%H:%M")

    new = PowerInterruption(interrupted=interrupted, restored=restored, scheduled=data["scheduled"][0])
    new.save()
    new.set_duration()
    return Response({"message":"PI data encoding success"})


"""
POWER CONSUMPTIONS
"""
@api_view(["POST","PUT"])
def newPowerConsumption(request):
    data = request.data
    
    try:
        prev = PowerConsumption.objects.last()
        date_time = datetime.strptime(data["datetime"],"%Y-%m-%dT%H:%M")
        new = PowerConsumption(date_time=date_time, meter=int(data["meter"]))
        new.save()
        
        new.get_consumption(prev.meter,new.meter)

        if prev.consumed == new.consumed:
            new.trend = "same"
        elif prev.consumed > new.consumed:
            new.trend = "down"
        elif prev.consumed < new.consumed:
            new.trend = "up"
        new.save()

    except ObjectDoesNotExist:
        new = PowerConsumption(date_time=date_time, meter=int(data["meter"]))
        new.save()
        new.get_consumption(0,new.meter)
        new.trend = "up"
        new.save()

    
    return Response({"message":"PC data encoding success"})

@api_view(["GET"])
def getPowerConsumptions(request):
    power_consumptions = PowerConsumption.objects.all().order_by("-date_time")
    serializer = PowerConsumptionSerializer(power_consumptions, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getPowerInterruptions(request):
    power_interruptions = PowerInterruption.objects.all().order_by("-interrupted")
    serializer = PowerInterruptionSerializer(power_interruptions, many=True)
    return Response(serializer.data)