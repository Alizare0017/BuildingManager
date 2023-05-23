from django.db import models

from buildings.models import Unit

from django.conf import settings
from django.utils import timezone


class Bill(models.Model):
    amount = models.FloatField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, related_name="Bills", on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField()
    description = models.TextField()
    is_paid = models.BooleanField(default=False)

    def is_overdue(self):
        return not self.is_paid and self.expire_date < timezone.now()
