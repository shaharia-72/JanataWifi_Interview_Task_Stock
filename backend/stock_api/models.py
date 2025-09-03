from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
  created_at = models.DateTimeField(auto_now_add=True, db_index=True)
  updated_at = models.DateTimeField(auto_now=True, db_index=True)

  class Meta:
    abstract = True



class stockModel(TimestampedModel):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    trade_code = models.CharField(max_length=10)
    high_trade = models.DecimalField(max_digits=10, decimal_places=2)
    low_trade = models.DecimalField(max_digits=10, decimal_places=2)
    open_trade = models.DecimalField(max_digits=10, decimal_places=2)
    close_trade = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    class Meta:
      ordering = ['-date', 'trade_code']
      verbose_name = 'Stock'
      verbose_name_plural = 'Stocks'
      db_table = 'stock_data'
      indexes = [
          models.Index(fields=['trade_code']),
          models.Index(fields=['date']),
          models.Index(fields=['trade_code', 'date']),
          ]

    constraints = [
        models.CheckConstraint(
            check=models.Q(high_trade__gte=models.F('low_trade')),
            name='high_greater_low'
        ),
        models.CheckConstraint(
            check=models.Q(open_trade__gte=0) & models.Q(close_trade__gte=0),
            name='price_positive'
        )
    ]

    unique_together = [['date', 'trade_code']]

    def __str__(self):
      return f"{self.trade_code} - {self.date}"
