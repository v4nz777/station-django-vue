from django .urls import path
from . import views

urlpatterns = [
    path("users/", views.getListofUsers, name="getListofUsers"),
    path("user/<str:username>/", views.getCurrentUser, name="getCurrentUser"),
    path("register/", views.createUser, name="createUser"),
    path("dtr_in/", views.inDTR, name="dtrIn"),
    path("dtr_out/", views.outDTR, name="dtrOut"),
    path("get_history/<str:username>/", views.getAllUserHistory, name="getAllUserHistory"),
    path("get_history/<str:username>/<str:year>/<str:month>/", views.filterUserHistoryByMonth, name="filterUserHistoryByMonth"),
    path("get_history/<str:username>/<str:year>/<str:month>/<str:date>/", views.filterUserHistoryByDate, name="filterUserHistoryByDate"),
    path("change/avatar/<str:username>/", views.changeAvatar, name="changeAvatar"),
    path("activity/<str:username>/", views.getUserActivity, name="getUserActivity"),
    path("activities/<str:filter>/", views.getFilteredActivity, name="generalActivity"),
    path("activities/add/brownout", views.postNewBrownOut, name="addNewBrownout"),
    path("generate/dtr/<str:username>", views.generateDTR, name="generateDTR"),
]
