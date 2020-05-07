from django.db import models
from django.utils.timezone import now
from account.models import Account

# Create your models here.
#modelo para crear las denuncias

class Complaint(models.Model):
    user_complaint = models.ForeignKey(Account, related_name="User_complaint", on_delete=models.CASCADE, verbose_name='Denunciante')
    indicated_user = models.ForeignKey(Account, related_name="indicated_user", null=True, on_delete=models.CASCADE, verbose_name='Denunciado')
    problem = models.CharField(max_length=20,null=False, blank=False, verbose_name='Problema')
    comment = models.TextField(null=True, verbose_name='Comentario')
    published = models.DateTimeField(verbose_name="Fecha de publicacion", default=now)

    class Meta():
        verbose_name = "Denunciante"
        verbose_name_plural = "Denunciantes"


    def __str__(self): 
        return self.user_complaint.get_full_name()

    