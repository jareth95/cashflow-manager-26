from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User



class Investment(models.Model):

    name = models.CharField(max_length=30)
    amount = models.FloatField()
    exchange = models.CharField(max_length=30)
    buy_price = models.FloatField()
    buy_date = models.DateField(default=now)
    sell_price = models.FloatField(null=True, blank=True)
    sell_date = models.DateField(null=True, blank=True)
    pnl = models.FloatField(null=True, blank=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

