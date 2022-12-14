from django .urls import path
from . import views

urlpatterns = [
    path("tx_log", views.log, name="transmitter log"),
    path("tx_logs/<str:filter>", views.getTXLogs, name="getTXLogs"),
]