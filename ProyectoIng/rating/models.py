from django.db import models
from account.models import Account
from store.models import Store

# Create your models here.

#modelo para crear la evaluacion de usuarios

class Rating(models.Model):
    evaluated_user = models.ForeignKey(Account, related_name="evaluated_user", null=True, on_delete=models.CASCADE, verbose_name='Evaluado')
    evaluator_user = models.ForeignKey(Account, related_name="evaluator_user", on_delete=models.CASCADE, verbose_name='Evaluador')
    evaluated_store = models.ForeignKey(Store, null=True, on_delete=models.CASCADE, verbose_name='Tienda Evaluada')
    points = models.IntegerField( verbose_name='Puntos')
    comment = models.TextField( null=True, verbose_name='Comentario')


    def __str__(self):

#muestra los usuarios que fueron evaluados 

        if self.evaluated_user is None:
            return self.evaluator_user.get_full_name()
        else:
            return self.evaluator_user.get_full_name()+' gave '+ str (self.points ) +' to '+ self.evaluated_user.get_full_name()

    class Meta():
        verbose_name= "Evaluación"
        verbose_name_plural= "Evaluaciones"

class RatingStore(models.Model):
    evaluated_store = models.ForeignKey(Store, related_name="evaluated_store", null=True, on_delete=models.CASCADE, verbose_name='Tienda Evaluada')
    evaluator_user_store = models.ForeignKey(Account, related_name="evaluator_user_store", on_delete=models.CASCADE, verbose_name='Evaluador')
    points = models.IntegerField( verbose_name='Puntos')
    comment = models.TextField( null=True, verbose_name='Comentario')

    def __str__(self):

#muestra los usuarios que fueron evaluados 

        if self.evaluated_store is None:
            return self.evaluator_user_store.get_full_name()
        else:
            return self.evaluator_user_store.get_full_name()+' gave '+ str (self.points ) +' to '+ self.evaluated_store.store_name

    class Meta():
        verbose_name= "Evaluación Tiendas"
        verbose_name_plural= "Evaluaciónes de Tiendas"