from buildings.models import Building, Unit
from users.models import User
from typing import List, Tuple

from django.db.models import Sum, QuerySet


def count_all_members(units: QuerySet[Unit]) -> dict:
    return units.aggregate(all_members=Sum("members"))


def get_all_residents(building: Building) -> Tuple[List[User], dict]:
    units = building.units.all()
    members_count = count_all_members(units)
    return [unit.resident for unit in units if unit.resident is not None], members_count
