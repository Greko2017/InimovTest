from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Partner(models.Model):     
    revenue_sale = models.CharField(max_length=120)
 
    class Meta:
        verbose_name = _("pl_budget")
        verbose_name_plural = _("pl_budgets")
        ordering = ("revenue_sale",)

    def __str__(self):
        return str(self.revenue_sale)