import json
from datetime import datetime, date
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from zoneinfo import ZoneInfo

from .dtr import generate_workbook
from .models import User, History, Position, Station, Activity
from .helpers import create_new_user
from .serializers import (
    UserSerializer,
    HistorySerializer,
    MonthlyDTRSerializer,
    PositionSerializer,
    StationSerializer,
    ActivitySerializer,
)

@api_view(["GET"])
def giveStationInfo(request):
    station = Station.objects.first()
    if not station:
        return Response({"message": "No station data found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(StationSerializer(station).data)


@api_view(["POST"])
def createUser(request):
    required_fields = ["username", "email", "password", "confirmation"]
    data = json.loads(request.body)

    if not all(field in data for field in required_fields):
        return Response({"message": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)
    
    if data["password"] != data["confirmation"]:
        return Response({"message": "Password and confirmation do not match."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = create_new_user(data)
    except IntegrityError:
        return Response({"message": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Registration succeeded.", "data":UserSerializer(user).data})



@api_view(["GET"])
def getListofUsers(request):
    data = User.objects.filter(is_superuser=False)
    serializer = UserSerializer(data, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getCurrentUser(request, username):
    username = username.lower()
    try:
        data = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"message": f"User: {username} does not exist in database"},status=status.HTTP_400_BAD_REQUEST)
    return Response(UserSerializer(data).data)


@api_view(["PUT"])
def logInToDTR(request):
    data = json.loads(request.body)
    username = data.get("username", "").lower()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if not user.is_logged:
        user.is_logged = True
        user.save()
        now = datetime.now(tz=ZoneInfo(settings.TIME_ZONE))
        history, created = History.objects.get_or_create(
            user=user, month=now.strftime("%B"), date=now.strftime("%d"), year=now.strftime("%Y"),
            defaults={"time_in_datetime": now, "time_out_datetime": None},
        )
        return Response({"is_logged": user.is_logged})
    else:
        return Response({"is_logged": user.is_logged})


@api_view(["PUT"])
def logOutToDTR(request):
    data = json.loads(request.body)

    username = data["username"].lower()
    month = data["month"]
    date = data["date"]
    year = data["year"]
    user = User.objects.get(username=username)
    if user.is_logged:
        user.is_logged = False
        user.save()
        now = datetime.now(tz=ZoneInfo(settings.TIME_ZONE))
       
        instance = History.objects.get(user=user, month=month, date=date, year=year)
 
        instance.time_out_datetime = now
        instance.save()

        user.last_login = now
        user.save()
        
    return Response({"is_logged": user.is_logged})
    

@api_view(["GET"])
def getAllUserHistory(request, username):
    user = User.objects.get(username=username)
    data = History.objects.filter(user=user)
    
    history_list = []
    for i in data:
        serializer = HistorySerializer(i)
        if serializer.data["time_in_datetime"] and serializer.data["time_out_datetime"]:
            history_list.append(serializer.data)
        
    context = {
        "history": sorted(history_list[:30], key=lambda x: x["id"], reverse=True)
    }
    return Response(context)


@api_view(["GET"])
def filterUserHistoryByMonth(request, username, year, month):
    
    user = User.objects.get(username=username)
    data = History.objects.filter(user=user, year=year, month=month)
    
    history_list = []
    for i in data:
        if i.time_out_datetime:
            serializer = HistorySerializer(i)
            history_list.append(serializer.data)
        
    context = {
        "history": sorted(history_list, key=lambda x: x["date"])
    }
    return Response(context)


@api_view(["GET"])
def filterUserHistoryByDate(request, username, year, month, date):
    try:
        user = User.objects.get(username=username)
        data = History.objects.get(user=user, year=year, month=month, date=date)
        
        serializer = HistorySerializer(data)
        return Response(serializer.data)
    except:
        return Response({"message": "History does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def changeAvatar(request, username):
    
    user = User.objects.get(username=username)
    image = request.data["avatar"]
    print(image)
    user.avatar = image
    user.save()

    response = {
        "message": "Avatar updated!",
        "new_avatar": user.avatar.url
    }
    return Response(response)


@api_view(["GET"])
def getUserActivity(request, username):
    user = User.objects.get(username = username)
    try:
        activity = Activity.objects.filter(user=user).order_by("-created")
        serializer = ActivitySerializer(activity, many=True)
        return Response(serializer.data)
        
    except ObjectDoesNotExist:
        return Response({"message":f"User: {username} has no activity yet"})


@api_view(["GET"])
def getFilteredActivity(request, filter):
    if filter.lower() == "general":
        general = Activity.objects.all().order_by("-created")
        serializer = ActivitySerializer(general, many=True)

        return Response(serializer.data)
    else:
        return Response({"message": f"no assigned filter: '{filter}' yet"})


@api_view(["POST"])
def generateDTR(request, username):
    data = request.data
    from_ = datetime.strptime(data["from"],"%Y-%m-%d")
    to_ = datetime.strptime(data["to"],"%Y-%m-%d")
    generate = generate_workbook(username,from_,to_)
    serializer = MonthlyDTRSerializer(generate)
    return Response(serializer.data)


@api_view(["GET"])
def positions(request,query:str):
    if query.lower() == 'all':
        positions = Position.objects.all()
    else:
        positions = Position.objects.filter(title__icontains=query.lower()).exclude(title__iexact=query.lower())

    serializer = PositionSerializer(positions,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def position(request,id:int):
    position = Position.objects.get(id=id)
    serializer = PositionSerializer(position)
    return Response(serializer.data)

@api_view(["POST"])
def addPosition(request):
    if request.method == "POST":
        data = request.data
        title = str(data["position_title"]).lower()
        try:
            Position.objects.get(title=title)
        except ObjectDoesNotExist:
            Position(title=title).save()
        positions = Position.objects.all()
        serializer = PositionSerializer(positions,many=True)
        return Response(serializer.data)

@api_view(["POST"])
def assignPos(request,username):
    data = request.data
    title = str(data["position_title"]).lower()
    try:
        position = Position.objects.get(title=title)
    except ObjectDoesNotExist:
        position = Position(title=title)
        position.save()

    user = User.objects.get(username=username)
    user.position = position
    user.regular = True if data["regular"]=="true" else False
    user.save()
    serializer = PositionSerializer(position)
    return Response(serializer.data)
    
