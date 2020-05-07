from ad.models import Ad, Disable_ads
from django.utils import timezone
from django.utils.timezone import timedelta

#JOBS
def delete_old_ads():
    disable_days = Disable_ads.objects.filter(pk=1)
    #old_ads = Ad.objects.filter(date_created__lte=(timezone.now() - timedelta(days=15)))
    for unique_element in disable_days:
        old_ads = Ad.objects.filter(date_created__lte=(timezone.now() - timedelta(days=unique_element["time_to"])))
        
    for ad in old_ads:
        ad.active = False
        ad.save()



