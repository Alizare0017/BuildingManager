from django.contrib import admin
from .models import Unit, Building, UnitSpecification
from django.contrib.auth.models import Group



admin.site.register(Building)
admin.site.register(Unit)
admin.site.register(UnitSpecification)

admin.site.unregister(Group)