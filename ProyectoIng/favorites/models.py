from django.db import models
from account.models import Account
# Create your models here.
class Favorites(models.Model):
    id_user= models.ForeignKey(Account, on_delete=models.CASCADE)
    id_favorite_user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name = "favoritos" )

