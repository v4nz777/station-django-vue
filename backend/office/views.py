from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import (
    AdVersion,
    Adcategory,
    Advertiser,
    AudioFile,
    Invoice,
    Ad,
    Package
    )
from station.models import Activity, User
from .serializers import (
    AdSerializer,
    AdVersionSerializer,
    AdvertiserSerializer,
    AudioFileSerializer,
    InvoiceSerializer,
    PackageSerializer,
    )
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
import json
from datetime import datetime,date
from .invoice import create_invoice
from django.core.files import File
from django.db.models import Q


"""
    :: Get all ads with filter
    :: api: "/ads/<str:filter>"
"""
@api_view(["GET"])
def getAds(request,filter):
    if filter.lower() == "all":
        data = Ad.objects.all().order_by("-id")
        serializer = AdSerializer(data, many=True)
        return Response(serializer.data)

@api_view(["GET"])
def getAdVersion(request,contract,version):
    ad = Ad.objects.get(contract=contract)
    version = ad.versions.get(version=version)

    serializer = AdVersionSerializer(version)
    return Response(serializer.data)

"""
    :: Create a new ad, or add new version  to an ad
"""
@api_view(["POST"])
def submitAd(request):
    data = request.data
    adtype = data["type"]
    adtitle = data["title"]
    advertiser = None
    revision = False
    package = None

    try:
        package = Package.objects.get(name=data["ad_package"])
    except ObjectDoesNotExist:
        package = None

    """ Make new advertiser if not yet existed """
    try:
        advertiser = Advertiser.objects.get(name=data["advertiser"])
    except ObjectDoesNotExist:
        new_advertiser = Advertiser(
            name = data["advertiser"]
        ).save()
        advertiser = Advertiser.objects.get(name=data["advertiser"])

    """ Query for existing Ad, else make a fresh Ad """
    try:
        ad = Ad.objects.get(contract=data["contract"])
        revision = True
    except ObjectDoesNotExist:
        new_ad = Ad(
            title = adtitle,
            contract = data["contract"],
            type = data["type"],
            bo_number = data["bo_number"],
            advertiser = advertiser,
        ).save()
        ad = Ad.objects.get(contract=data["contract"])

    """ Create new version """
    version = AdVersion(
        name = f"{adtitle} {ad.versions.count() + 1}",
        version = ad.versions.count() + 1,
        pricing = data["pricing"],
        ex_deal = data["ex_deal"][0],
        amount = float(data["amount"]),
        package = package,
        broadcast_start = data["broadcast_start"],
        broadcast_end = data["broadcast_end"],
        ad_spots = int(data["ad_spots"]),
        schedule = data["schedule"],
        has_tagline = data["has_tagline"][0],
        aob_spots = int(data["aob_spots"]),
        tc_spots = int(data["tc_spots"]),
        ss_spots = int(data["ss_spots"]),
        aob_sched = data["aob_sched"],
        tc_sched = data["tc_sched"],
        ss_sched = data["ss_sched"],
        account_executive = data["account_executive"],
        material_duration = data["material_duration"]
    )
    version.save()

    """Upload files then add to files(ManytoMany) field of this Ad"""
    audio_files = []

    if revision:
        print(data["existing_files"].split(","))
        for old_file_id in data["existing_files"].split(","):

            # if old_file_id not in data.getlist("files_remove") and old_file_id != "":
            if old_file_id not in data["files_remove"].split(",") and old_file_id != "":
                old_file = AudioFile.objects.get(id=old_file_id)
                audio_files.append(old_file)
                version.files.add(old_file)


    for file in data.getlist("files"):
        try:
            create_file = AudioFile(
                filename = file.name,
                from_ad = version,
                file = file
            ).save()
        except IntegrityError:
            pass # dont create if already existed // same filename
        
        # query the file and list to Ads
        this = AudioFile.objects.get(filename=file.name, from_ad = version)
        audio_files.append(this)
        version.files.add(this)
        version.save()
    
    """ add this version to Ad """
    ad.versions.add(version)

    """ set current version to use """
    ad.current_ver = version.version
    ad.save()

    """Add this ad to version"""
    if package:
        package.ads.add(ad)
        package.save()


    """Add to activities"""
    """ Activity types:
        ⭐ "ads"            -> if new ads
        ⭐ "ad_revisions"   -> if not new ads
    """
    activity = Activity()
    if not revision:
        activity.new_activity(
            data["uploader"],
            f"added a new {adtype} ad",
            type="ads",
            title=data["title"],
            contract=data["contract"],
            audio_files=[i.id for i in audio_files],
            duration=data["duration"]
            )
    else:
        _contract = data["contract"]
        
        activity.new_activity(
            data["uploader"],
            f"made changes to ad {_contract}",
            type="ad_revisions",
            title=data["title"],
            contract=data["contract"],
            duration=data["duration"]
            )
    return Response({"message":"Posted!"})

@api_view(["PUT"])
def changeVersion(request):
    data = request.data
    new_version = int(data["new_version"])
    ad = Ad.objects.get(contract=data["contract"])
    ad.current_ver = new_version
    ad.save()

    return Response({"message": "changeVersion succeed!"})

@api_view(["GET"])
def compareVersions(request, contract, x ,y):
    ad = Ad.objects.get(contract=contract)
    verX = ad.versions.get(version=x)
    verY = ad.versions.get(version=y)

    x_serializer = AdVersionSerializer(verX)
    y_serializer = AdVersionSerializer(verY)


    return Response({
        "x": x_serializer.data,
        "y": y_serializer.data
    })

@api_view(["POST"])
def changeAdAvatar(request):
    data = request.data
    ad = Ad.objects.get(contract=data["contract"])
    ad.ad_avatar = data["ad_avatar"]
    ad.save()
    
    serializer = AdSerializer(ad)
    return Response(serializer.data)

@api_view(["GET"])
def searchAdvertisers(request,keyword):
    if keyword == "all":
        data = Advertiser.objects.all()
    else:
        data = Advertiser.objects.filter(name__icontains=keyword)
    
    serializer = AdvertiserSerializer(data,many=True)
    return Response(serializer.data)

@api_view(["GET"])
def getAdvertiser(request,id):
    data = Advertiser.objects.get(id=id)
    serializer = AdvertiserSerializer(data)
    return Response(serializer.data)

@api_view(["GET"])
def getAudioFile(request,id):
    data = AudioFile.objects.get(id=id)
    serializer = AudioFileSerializer(data)
    return Response(serializer.data)

@api_view(["GET"])
def getInvoiceList(request, contract):
    if request.method == "GET":
        data = Invoice.objects.filter(from_contract=contract).order_by("-id")
        serializer = InvoiceSerializer(data, many=True)
        return Response(serializer.data)

@api_view(["GET"])
def checkIfInvoiceExists(request,invoice):
    try:
        data = Invoice.objects.get(invoice_no=invoice)
        return Response({"message": "Invoice exists", "exists":True})
    except ObjectDoesNotExist:
        return Response({"message": "Invoice doesnt exist", "exists":False})


@api_view(["POST"])
def createInvoice(request):
    if request.method == "POST":
        data = request.data
        contract = data["from_contract"]
        advertiser = Advertiser.objects.get(id=data["advertiser"])
        from_ = datetime.strptime(data["applicable_month_from"],"%Y-%m-%d")
        to_ = datetime.strptime(data["applicable_month_to"],"%Y-%m-%d")
        invoice_date = datetime.strptime(data["invoice_date"],"%Y-%m-%d")

        try:
            new = Invoice(
                advertiser=advertiser,
                from_contract=contract,
                account_executive=data["account_executive"],
                invoice_no = data["invoice_no"],
                invoice_date = invoice_date,
                amount = data["amount"],
                applicable_month_from = from_,
                applicable_month_to = to_,
                paid=False
            )
            new.save()
            invoice = Invoice.objects.get(invoice_no=data["invoice_no"])

            invoice_file = create_invoice(data["invoice_no"])
            with open(invoice_file, "rb") as f:
                invoice.file.save(invoice_file,File(f), save=True)
            invoice.save()

            return Response({"contract":contract})
        except IntegrityError:
            return Response({"error": "IntegrityError"})

@api_view(["POST"])
def payInvoice(request):
    if request.method == "POST":
        data = request.data
        invoice_no = data["invoice_no"]
        amount_received = data["amount_received"]
        or_date = datetime.strptime(data["or_date"],"%Y-%m-%d").date()
        or_number = data["or_number"]
        print(data)

        try:
            get = Invoice.objects.get(invoice_no=invoice_no)
            get.amount_received = amount_received
            get.or_date = or_date
            get.or_number = or_number
            get.paid = True
            get.save()
            serializer = InvoiceSerializer(get)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"failed":"failed"})

@api_view(["PUT"])
def bankDeposit(request,invoice):
    data = request.data
    image = data["deposit_slip"]
    print(data)
    invoice = Invoice.objects.get(invoice_no=invoice)

    invoice.deposit_slip = image
    invoice.deposited = True
    invoice.save()

    serializer = InvoiceSerializer(invoice)

    return Response(serializer.data)



@api_view(["POST"])
def newPackage(request):
    data = request.data
    print(data)
    name = str(data["name"]).lower()
    description = str(data["description"])
    price = float(data["price"])
    pricing = str(data["pricing"])
    duration_of_pricing = int(data["duration_of_pricing"])
    spots_per_day = int(data["spots_per_day"])
    aob_per_day = int(data["aob_per_day"])
    tc_per_day = int(data["tc_per_day"])
    ss_per_day = int(data["ss_per_day"])
    material_duration = float(data["material_duration"])
    author = str(data["author"])

    package = Package(
        name = name,
        description = description,
        price = price,
        pricing = pricing,
        duration_of_pricing = duration_of_pricing,
        spots_per_day = spots_per_day,
        aob_per_day = aob_per_day,
        tc_per_day = tc_per_day,
        ss_per_day = ss_per_day,
        material_duration = material_duration,
        author=author
    )
    package.save()
    serializer = PackageSerializer(package)
    return Response(serializer.data)

@api_view(["GET"])
def loadPackages(request, filter):
    if filter == "all":
        pkg = Package.objects.all()
    else:
        pkg = Package.objects.filter(
            Q(name__icontains=filter) | Q(description__icontains=filter)
        )
    serializer = PackageSerializer(pkg, many=True)
    return Response(serializer.data)

@api_view(["POST"])
def getPackage(request):
    data = request.data
    package_name = str(data["package"])
    pkg = Package.objects.get(name=package_name)
    serializer = PackageSerializer(pkg)
    return Response(serializer.data)

@api_view(["PUT"])
def changePackageColor(request,id):
    data = request.data
    pkg = Package.objects.get(id=id)
    pkg.theme = data["color"]
    pkg.save()

    #for refresh
    all_pkg = Package.objects.all()
    serializer = PackageSerializer(all_pkg, many=True)
    return Response(serializer.data)

@api_view(["DELETE"])
def deletePackage(request,id):
    pkg = Package.objects.get(id=id)
    pkg.delete()

    #for refresh
    all_pkg = Package.objects.all()
    serializer = PackageSerializer(all_pkg, many=True)
    return Response(serializer.data)

"""Get  and calculate total collections based on filter"""
@api_view(["GET"])
def totalCollection(request,filter):
    today = date.today()
    total = 0
    items = []
    if filter.lower() == "today":
        invoices = Invoice.objects.filter(
            paid=True,
            or_date__day__gte=today.day,
            or_date__month__gte=today.month,
            or_date__year__gte=today.year
        )
    elif filter.lower() == "month":
        invoices = Invoice.objects.filter(
            paid=True,
            or_date__month__gte=today.month,
            or_date__year__gte=today.year
        )
    elif filter.lower() == "year":
        invoices = Invoice.objects.filter(
            paid=True,
            or_date__year__gte=today.year
        )
    elif filter.lower() == "all":
        invoices = Invoice.objects.filter(paid=True)
    
    for i in invoices:
        items.append({
            "contract": i.from_contract,
            "invoice": i.invoice_no,
            "invoice_date": i.invoice_date,
            "or": i.or_number,
            "or_date": i.or_date,
            "amount_received":i.amount_received
        })
        total = total+i.amount_received
    
    return Response({
        "total":total,
        "items": items
    })

"""Get  and calculate total sales based on filter"""
@api_view(["GET"])
def totalSales(request,filter):
    today = date.today()
    total = 0
    items = []
    if filter.lower() == "today":
        invoices = Invoice.objects.filter(
            or_date__day__gte=today.day,
            or_date__month__gte=today.month,
            or_date__year__gte=today.year
        )
    elif filter.lower() == "month":
        invoices = Invoice.objects.filter(
            or_date__month__gte=today.month,
            or_date__year__gte=today.year
        )
    elif filter.lower() == "year":
        invoices = Invoice.objects.filter(
            or_date__year__gte=today.year
        )
    elif filter.lower() == "all":
        invoices = Invoice.objects.all()
    
    for i in invoices:
        items.append({
            "contract": i.from_contract,
            "invoice": i.invoice_no,
            "invoice_date": i.invoice_date,
            "amount":i.amount
        })
        total = total+i.amount
    
    return Response({
        "total":total,
        "items": items
    })