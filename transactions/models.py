from django.db import models

from users.models import User,Person

# Create your models here.
class Transactions(models.Model):

   user = models.ForeignKey(User, on_delete=models.CASCADE)
   amount = models.IntegerField()
   note = models.CharField(max_length=200,null=True)
   mode = models.BooleanField(null=False) # if mode 1 then to give or to recieve
   person = models.ForeignKey(Person, on_delete=models.CASCADE)
   status = models.BooleanField(default=False)

   class Meta:
      db_table="transactions"