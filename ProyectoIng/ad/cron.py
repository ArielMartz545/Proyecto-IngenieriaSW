from ad.models import Ad
from django.utils import timezone
from django.utils.timezone import timedelta

#JOBS
def delete_old_ads():
    old_ads = Ad.objects.filter(date_created__gte=timezone.now()-timedelta(days=15))
        for ad in old_ads:
            ad.active = False
            ad.save()

def test():
    return True
