from django.db import models
from account.models import Account
from store.models import Store

# Create your models here.

#modelo para crear la evaluacion de usuarios

class Rating(models.Model):
    evaluated_user = models.ForeignKey(Account, related_name="evaluated_user", null=True, on_delete=models.CASCADE)
    evaluator_user = models.ForeignKey(Account, related_name="evaluator_user", on_delete=models.CASCADE)
    evaluated_store = models.ForeignKey(Store, null=True, on_delete=models.CASCADE)
    points = models.IntegerField()
    comment = models.TextField( null=True)


    def __str__(self):

#muestra los usuarios que fueron evaluados 

        if self.evaluated_user is None:
            return self.evaluator_user.get_full_name()
        else:
            return self.evaluator_user.get_full_name()+' gave '+ str (self.points ) +' to '+ self.evaluated_user.get_full_name()

    class Meta():
        verbose_name= "Evaluación"
        verbose_name_plural= "Evaluaciones"
