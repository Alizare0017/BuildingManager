from django.urls import path

from . import views
urlpatterns = [
    path("", views.BuildingView.as_view(), name="buildings"),
    path("<int:pk>/", views.RetrieveUpdateDestroyBuildingView.as_view(), name="building"),
    path("<int:pk>/units/", views.BuildingsUnitsView.as_view(), name="buildings_units"),
    path("<int:pk>/residents/", views.GetAllResidentsView.as_view(), name="buildings_residents"),
    path("units/<int:pk>/", views.RetrieveUnitView.as_view(), name="unit"),
    path("units/<int:pk>/resident/", views.UnitsResidentView.as_view(), name="units_resident"),
    path("unit/specification/", views.UnitSpecificationView.as_view(), name="create_unit_specification"),
    path("unit/specification/<int:pk>/", views.RetrieveUpdateUnitSpecificationView.as_view(),
         name="unit_specification"),
    path("my_buildings/", views.ManagerBuildingListView.as_view(), name="manager_buildings"),
]

