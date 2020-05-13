from ad.models import Ad, Disable_ads
from django.utils import timezone
from django.utils.timezone import timedelta

#JOBS
def delete_old_ads():
    valor= disable_days = Disable_ads.objects.filter(pk=1)
    days_to_disable=valor[0].time_to
    #old_ads = Ad.objects.filter(date_created__lte=(timezone.now() - timedelta(days=15)))
    for unique_element in disable_days:
        old_ads = Ad.objects.filter(date_created__lte=(timezone.now() - timedelta(days=days_to_disable)))
        
    for ad in old_ads:
        ad.active = False
        ad.reason = "automatic"
        ad.save()



