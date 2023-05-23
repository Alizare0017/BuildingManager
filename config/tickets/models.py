from django.conf import settings
from django.db import models

from buildings.models import Building


class Ticket(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_tickets")
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=80)
    message = models.TextField()
    seen = models.BooleanField(default=False, null=True)

