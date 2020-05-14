from django.shortcuts import render
from django.views.generic.base import TemplateView
from account.models import Account
from ad.models import Ad
from search.models import Search
import datetime

from django.contrib.auth.mixins import UserPassesTestMixin
# Create your views here.
class graphsTemplateView(UserPassesTestMixin ,TemplateView):
    template_name = "graphs/graphs.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        year=datetime.datetime.now().year
        context = super().get_context_data(**kwargs)
        context['active_users'] =  Account.objects.filter(is_active=True).count()
        context['inactive_users'] =  Account.objects.filter(is_active=False).count()
        context['active_ads'] = Ad.objects.filter(active= True).count()
        context['inactive_ads'] = Ad.objects.filter(active= False).count()


        all_join_dates = Account.objects.all().filter(date_joined__year=year)

        #Users*actualyear
        ene,feb,mar,abr,may,jun,jul,ago,sep,oc,nov,dic=0,0,0,0,0,0,0,0,0,0,0,0

        for date in all_join_dates:
            if date.date_joined.month == 1:
                en=en+1
            elif date.date_joined.month == 2:
                feb= feb+1
            elif date.date_joined.month == 3:
                mar= mar+1
            elif date.date_joined.month == 4:
                abr= abr+1
            elif date.date_joined.month == 5:
                may= may+1
            elif date.date_joined.month == 6:
                jun= jun+1
            elif date.date_joined.month == 7:
                jul= jul+1
            elif date.date_joined.month == 8:
                ago= ago+1
            elif date.date_joined.month == 9:
                sep= sep+1
            elif date.date_joined.month == 10:
                oc= oc+1
            elif date.date_joined.month == 11:
                nov= nov+1
            elif date.date_joined.month == 12:
                dic= dic+1   
       
        context['ene']=ene
        context['feb']=feb
        context['mar']=mar
        context['abr']=abr
        context['may']=may
        context['jun']=jun
        context['jul']=jul
        context['ago']=ago
        context['sep']=sep
        context['oc']=oc
        context['nov']=nov
        context['dic']=dic

        #Search Graphs Data 
        context["ad_search"] =Search.objects.filter(ad_search=True).count()
        context["user_search"] =Search.objects.filter(user_search=True).count()
        context["store_search"] =Search.objects.filter(store_search=True).count()
        context["custom_price_range"] =Search.objects.filter(custon_price_range=True).count()

        #Anuncios Eliminados*Categoria
        ads_query = Ad.objects.filter(active= False).all()
        active_categoryes = list()
        for ad in ads_query:
            if ad.id_category.category_name not in active_categoryes:
                active_categoryes.append(ad.id_category.category_name)

        active_categoryes_values=dict([(key, 0) for key in active_categoryes])

        for ad in ads_query:
            if ad.id_category.category_name in active_categoryes_values.keys():
                active_categoryes_values[ad.id_category.category_name] += 1

        context["disable"] = active_categoryes_values
        return context