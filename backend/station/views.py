from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.decorators import api_view
from .models import User, History, Activity, Position
from .serializers import (
    UserSerializer,
    HistorySerializer,
    ActivitySerializer,
    MonthlyDTRSerializer,
    PositionSerializer
    )
import json
from .dtr import generate_workbook
from datetime import datetime, tzinfo, date
from django.core.exceptions import ObjectDoesNotExist


""" ::::::::::::::::::::::::::::::::::::::::
    Function: user registration.
    API route: "/register"
    """
@api_view(["POST"])
def createUser(request):
    data = json.loads(request.body)

    # Getting the details for new user in lower case.
    username = data["username"].lower()
    email = data["email"].lower()
    first_name = data["firstName"].lower()
    last_name = data["lastName"].lower()
    address = data["address"].lower()
    mobile = data["mobile"].lower()
    telephone = data["telephone"].lower()
    facebook = data["facebook"].lower()
    gender = data["gender"].lower()


    # Check if Password Matched
    password = data["password"]
    confirmation = data["confirmation"]

    if password != confirmation:
        message = "The password you entered wont match each other..."

        return Response({"message":message})

    # Save the Details to the Database
    print(data)
    try:
        # & making sure the USERNAME and EMAIL are in lowerCase
        registration = User.objects.create_user(
            username.lower(),
            email.lower(),
            password,
            first_name=first_name.lower(),
            last_name=last_name.lower(),
            gender=gender.lower(),
            address=address.lower(),
            mobile=mobile,
            telephone=telephone,
            facebook=facebook.lower(),
        )
        registration.save()
        activity = Activity()
        activity.new_activity(username.lower(), "joined the station", type="registration")

        message = "Registration succeeded!"
        print(message)
        return Response({"message":message})
        
    except IntegrityError:
        message = "Username already taken!"
        print(message)
        return Response({"message":message})



""" ::::::::::::::::::::::::::::::::::::::::
    Function: View list of users from database with all fields.
    API route: "/users"
    """
@api_view(["GET"])
def getListofUsers(request):
    data = User.objects.filter(is_superuser=False)
    serializer = UserSerializer(data, many=True)
    return Response(serializer.data)



""" ::::::::::::::::::::::::::::::::::::::::
    Function: View a user and his/her details.
    API route: "/user/sample-user"

    Can be used to access current user
    """
@api_view(["GET"])
def getCurrentUser(request, username):
    data = User.objects.get(username=username)
    serializer = UserSerializer(data)

    return Response(serializer.data)




""" ::::::::::::::::::::::::::::::::::::::::
    Function: Change is_logged status to true and write on DTR sheet
    API route: "/dtr_log"

    Can be used to access current user
    """
@api_view(["PUT"])
def inDTR(request):
    data = json.loads(request.body)
    username = data["username"].lower()

    user = User.objects.get(username=username)
    if not user.is_logged:
        user.is_logged = True
        user.save()

        # Create History instance
        # Date
        now = datetime.now().replace(tzinfo=None)

        month = now.strftime("%B")
        date = now.strftime("%d")
        year = now.strftime("%Y")

        # Time
        time = now.strftime("%X")
  
        try:
            _all = History.objects.filter(user=user, month=month, date=date, year=year)
            current = History.objects.get(user=user, month=month, date=date, year=year)
            if current in _all:
                activity = Activity()
                activity.new_activity(username.lower(), "relogged in", type="relogin")


        except ObjectDoesNotExist:
            create_instance = History(user=user, time_in_datetime=now)
            create_instance.save()
            activity = Activity()
            activity.new_activity(username.lower(), "logged in", type="login")
   
        
        return Response({"is_logged":user.is_logged})
    else:
        return Response({"is_logged":user.is_logged})




""" ::::::::::::::::::::::::::::::::::::::::
    Function: Change is_logged status to false and write on DTR sheet
    API route: "/dtr_out"

    Can be used to access current user
    """
@api_view(["PUT"])
def outDTR(request):
    data = json.loads(request.body)

    username = data["username"].lower()
    month = data["month"]
    date = data["date"]
    year = data["year"]

    user = User.objects.get(username=username)
    

    if user.is_logged:
        user.is_logged = False
        user.save()
        # Create History instance
        # Date

    
        # Time
        now = datetime.now()
        instance = History.objects.get(user=user, month=month, date=date, year=year)
 
        # instance.time_out = time
        instance.time_out_datetime = now
        instance.save()

        #record last active
        user.last_login = now
        user.save()

        activity = Activity()
        activity.new_activity(username.lower(), "logged out", type="logout")
        return Response({"is_logged": user.is_logged})
    else:
        return Response({"is_logged": user.is_logged})


""" ::::::::::::::::::::::::::::::::::::::::
    Function: Returns all recent logs from user
    API route: "/get_history/sample-user"
    Output: List
    Can be used to access current user
    """
@api_view(["GET"])
def getAllUserHistory(request, username):
    user = User.objects.get(username=username)
    data = History.objects.filter(user=user)
    
    history_list = []
    for i in data:
        serializer = HistorySerializer(i)
        print(serializer.data)
        if serializer.data["time_in_datetime"] and serializer.data["time_out_datetime"]:
            history_list.append(serializer.data)
        
    context = {
        "history": sorted(history_list[:30], key=lambda x: x["id"], reverse=True)
    }
    return Response(context)


""" ::::::::::::::::::::::::::::::::::::::::
    Function: Returns all logs from user
    API route: "/get_history/sample-user"
    Output: List
    Can be used to access current user
    """
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


""" ::::::::::::::::::::::::::::::::::::::::
    Function: Returns filtered logs from user
    API route: "/get_history/sample-user/year/month/date"
    Output: Single object
    Can be used to access current user
    """
@api_view(["GET"])
def filterUserHistoryByDate(request, username, year, month, date):
    user = User.objects.get(username=username)
    
    data = History.objects.get(user=user, year=year, month=month, date=date)
    serializer = HistorySerializer(data)
    return Response(serializer.data)

""" ::::::::::::::::::::::::::::::::::::::::
    Function: Returns new avatar for user
    API route: "/change/avatar/sample-user/"
    Output: Single object
    Can be used to access current user
    """
@api_view(["POST"])
def changeAvatar(request, username):
    
    user = User.objects.get(username=username)
    image = request.data["avatar"]
    # Optimize image
    size = (244,244)
    print(image)
    user.avatar = image
    user.save()

    pronoun = "his" if user.gender == "male" else "her"
    activity = Activity()
    activity.new_activity(username.lower(), f"changed {pronoun} avatar", type="profile_modify")
    response = {
        "message": "Avatar updated!",
        "new_avatar": user.avatar.url
    }
    return Response(response)


""" ::::::::::::::::::::::::::::::::::::::::
    Function: Returns new activity for user
    API route: "/activity/sample-user/"
    Output: Single object
    Can be used to access current user
    """
@api_view(["GET"])
def getUserActivity(request, username):
    user = User.objects.get(username = username)
    try:
        activity = Activity.objects.filter(user=user).order_by("-created")
        serializer = ActivitySerializer(activity, many=True)
        return Response(serializer.data)
        
    except ObjectDoesNotExist:
        return Response({"message":f"User: {username} has no activity yet"})



""" ::::::::::::::::::::::::::::::::::::::::
    Function: Returns filtered activity
    API route: "/activities/filterkey/"
    Output: Single object
    Can be used to access current user

    :: Available Filters:
        > general
    """
@api_view(["GET"])
def getFilteredActivity(request, filter):
    if filter.lower() == "general":
        general = Activity.objects.all().order_by("-created")
        serializer = ActivitySerializer(general, many=True)

        return Response(serializer.data)
    else:
        return Response({"message": f"no assigned filter: '{filter}' yet"})
    #TODO elifs new filter

""" ::::::::::::::::::::::::::::::::::::::::
    Function: Add new activity called Brownouts
    API route: "/activities/add/"
    Output: Single object response

    """
@api_view(["POST"])
def postNewBrownOut(request):
    data = request.data
    activity = Activity()
    activity.new_activity(
        data["author"].lower(),
        "reported a brownout incident",
        type="brownout",
        interrupted=data["interrupted"],
        restored=data["restored"],
        duration=data["duration"]
        )
    return Response({"message": "success"})


""" ::::::::::::::::::::::::::::::::::::::::
    Function: Generate new DTR excel
    API route: "/generate/dtr/<sampleuser>"
    Output: Single object response

    """
@api_view(["POST"])
def generateDTR(request, username):
    data = request.data
    from_ = datetime.strptime(data["from"],"%Y-%m-%d")
    to_ = datetime.strptime(data["to"],"%Y-%m-%d")
    generate = generate_workbook(username,from_,to_)
    serializer = MonthlyDTRSerializer(generate)
    return Response(serializer.data)


"""Handles Positions"""

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
    user.save()
    serializer = PositionSerializer(position)
    return Response(serializer.data)
    
