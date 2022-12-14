from django .urls import path
from . import views

urlpatterns = [
    path("search_advertiser/<str:keyword>", views.searchAdvertisers, name="searchAdvertisers"),
    path("advertiser/<int:id>", views.getAdvertiser, name="getAdvertiser"),
    path("audiofile/<int:id>", views.getAudioFile, name="getAudioFile"),
    path("ads/<str:filter>", views.getAds, name="getAds"),
    path("ad/<str:contract>/<str:version>",views.getAdVersion, name="getAdVersion"),
    path("new_ads", views.submitAd, name="submitAd"),
    path("invoices/<str:contract>", views.getInvoiceList, name="getInvoiceList"),
    path("add_invoice", views.createInvoice, name="createInvoice"),
    path("invoice_exists/<str:invoice>", views.checkIfInvoiceExists, name="checkIfInvoiceExists"),
    path("pay_invoice", views.payInvoice, name="payInvoice"),
    path("change_ad_avatar", views.changeAdAvatar, name="changeAdAvatar"),
    path("compare/<str:contract>/<int:x>/<int:y>", views.compareVersions, name="compareVersions"),
    path("change_version", views.changeVersion, name="changeVersion"),

]
