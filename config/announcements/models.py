from django.db import models
from django.conf import settings
from django.utils import timezone

from buildings.models import Building


class AnnouncementManager(models.Manager):
    def last_days_announcements(self, user, days):
        now = timezone.now()
        past_days = now - timezone.timedelta(days=days)
        self.filter(poster=user, pub_date__range=[past_days, now]).count()


class Announcement(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    description = models.TextField()
    pub_data = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(null=True, blank=True)
    seen_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="seen_announcements")

    objects = AnnouncementManager()


