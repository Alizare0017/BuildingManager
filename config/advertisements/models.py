from django.db import models

from buildings.models import UnitSpecification


class Advertisement(models.Model):
    RENT = "RENT"
    SALE = "SALE"
    choices = [
        (RENT, "rent"),
        (SALE, "sale")
    ]
    unit_specification = models.ForeignKey(UnitSpecification, on_delete=models.CASCADE)
    what_for = models.CharField(max_length=4, choices=choices)
    price = models.FloatField(null=True)
    mortgage = models.FloatField(null=True)
    rent = models.FloatField(null=True)
    exchangeable = models.BooleanField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)
