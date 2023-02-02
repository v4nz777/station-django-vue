from django .urls import path
from . import views

urlpatterns = [
    path("about/", views.giveStationInfo, name="giveStationInfo"),
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
    path("generate/dtr/<str:username>", views.generateDTR, name="generateDTR"),
    path("generate/dtr/<str:username>", views.generateDTR, name="generateDTR"),
    path("positions/<str:query>", views.positions, name="positions"),
    path("position/<int:id>", views.position, name="position"),
    path("add_position", views.addPosition, name="add_position"),
    path("assign_pos/<str:username>", views.assignPos, name="assignPos"),


]
