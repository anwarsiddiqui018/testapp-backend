from django.db import models
from django.utils import timezone

class StockFuturesModel(models.Model):
    SYMBOL = models.CharField(max_length=120,default=None)
    OPEN = models.FloatField(default=0.0)
    HIGH = models.FloatField(default=0.0)
    LOW = models.FloatField(default=0.0)
    CLOSE = models.FloatField(default=0.0)
    VOLUME = models.FloatField(default=0.0)
    OPEN_INT = models.FloatField(max_length=120,default=None)
    CHG_IN_OI = models.FloatField(default=0.0)
    TIMESTAMP = models.DateTimeField(default=timezone.now)


    def __str__(self) -> str:
        return self.SYMBOL + ' | '+ str(self.TIMESTAMP)