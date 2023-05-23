from django.db import models
from django.conf import settings


class Building(models.Model):
    """
    an instance of this table will be generated after a manager create a new building
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    unit_count = models.IntegerField()
    address = models.TextField(null=True, blank=True)


class Unit(models.Model):
    """
    after creating a Building instance by Building Manager, units will be generated based on building manager input
    """
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name="units")
    resident = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    members = models.IntegerField(default=1)
    unit_number = models.IntegerField()


class UnitSpecification(models.Model):
    unit = models.OneToOneField(Unit, on_delete=models.CASCADE)
    area = models.FloatField()
    built_up_area = models.FloatField()
    bedroom = models.IntegerField()
    floor = models.IntegerField()
    year_of_construction = models.IntegerField()
    features = models.TextField(help_text="in a comma-seperated format", null=True)
    description = models.TextField(null=True)
