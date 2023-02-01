from django.core.exceptions import ObjectDoesNotExist
from .models import (
    AdVersion,
    Adcategory,
    Advertiser,
    AudioFile,
    Invoice,
    Ad,
    Package
    )
from .serializers import (
    AdSerializer,
    AdVersionSerializer,
    AdvertiserSerializer,
    AudioFileSerializer,
    InvoiceSerializer,
    PackageSerializer,
    )

def writeAdtoDatabase(data):
    print(data)
    adtype = data["type"]
    adtitle = data["title"]
    advertiser, fresh_ad, package = None, False, None

    try:
        package = Package.objects.get(name=data["ad_package"])
    except ObjectDoesNotExist:
        package = None

    """ Make new advertiser if not yet existed """
    advertiser,_ = Advertiser.objects.get_or_create(name=data["advertiser"])
    
    """ Query for existing Ad, else make a fresh Ad """
    ad,fresh_ad = Ad.objects.get_or_create(
        contract=data["contract"],
        defaults={
            "title": adtitle,
            "contract": data["contract"],
            "type": data["type"],
            "bo_number": data["bo_number"],
            "advertiser": advertiser,
        }
    )
    
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
    
    #   This will add any uploaded files to the current version of the Ad
    for file in data.getlist("files"):
        audio_file, _ = AudioFile.objects.get_or_create(filename=file.name, from_ad=version,defaults={"file": file})
        audio_files.append(audio_file)

    #   This will remove some materials from this Ad version, and keep other files
    if not fresh_ad:
        existing_files = data["existing_files"].split(",")  #   these are list of IDs(numbers)
        files_to_remove = data["files_remove"].split(",")   #   these are list of IDs(numbers)
        for old_file_id in existing_files:
            if old_file_id not in files_to_remove and old_file_id != "":
                old_file = AudioFile.objects.get(id=old_file_id)
                if old_file not in audio_files:
                    audio_files.append(old_file)

    version.files.set(audio_files)
    """ add this version to Ad """
    ad.versions.add(version)

    """ set current version to use """
    ad.current_ver = version.version
    ad.save()

    """Add this ad to version"""
    if package:
        package.ads.add(ad)
        package.save()

    serializer = AdSerializer(ad)
    return serializer.data