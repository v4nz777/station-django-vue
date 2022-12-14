from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from datetime import datetime

from .models import TXLog
from .serializers import TXLogSerializer

"""
Log an instance to database
"""

@api_view(["POST"])
def log(request):
    
    data = request.data
    print(data)
    date = datetime.strptime(data["date"],"%Y-%m-%d")
    time = datetime.strptime(data["time"],"%H:%M:%S")
    line_voltage = float(data["line_voltage"])
    exciter = float(data["exciter"])
    driver_voltage = float(data["driver_voltage"])
    driver_current = float(data["driver_current"])
    driver_forward = float(data["driver_forward"])
    driver_rf = float(data["driver_rf"])
    final_current = float(data["final_current"])
    final_voltage = float(data["final_voltage"])
    final_forward = float(data["final_forward"])
    final_rf = float(data["final_rf"])
    author = str(data["author"])
    remarks = str(data["remarks"])


    try:
        instance = TXLog.objects.get(date=date, hour=int(time.hour))
        #prepare for edit
        instance.line_voltage = line_voltage
        instance.exciter = exciter
        instance.driver_voltage = driver_voltage
        instance.driver_current = driver_current
        instance.driver_forward = driver_forward
        instance.driver_rf = driver_rf
        instance.final_current = final_current
        instance.final_voltage = final_voltage
        instance.final_forward = final_forward
        instance.final_rf = final_rf
        instance.author = author
        instance.remarks = remarks
        instance.save()

    except ObjectDoesNotExist:
        instance = TXLog(
            date = date,
            time = time,
            line_voltage = line_voltage,
            exciter = exciter,
            driver_voltage = driver_voltage,
            driver_current = driver_current,
            driver_forward = driver_forward,
            driver_rf = driver_rf,
            final_current = final_current,
            final_voltage = final_voltage,
            final_forward = final_forward,
            final_rf = final_rf,
            author = author,
            remarks = remarks
        )
        instance.save()
    return Response({"message": "success"})



"""GET ALL LOGS"""
@api_view(["GET"])
def getTXLogs(request, filter):
    print(filter)
    query = None
    many = False
    if filter == "all":
        query = TXLog.objects.all()
        many = True
    elif filter == "last":
        query = TXLog.objects.last()
        many = False
    else:
        date = datetime.strptime(filter,"%Y-%m-%d")
        query = TXLog.objects.filter(date=date.date())
        many = True

    serializer = TXLogSerializer(query, many=many)
    return Response(serializer.data)


