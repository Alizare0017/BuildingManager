from django.urls import path

from . import views

urlpatterns = [
    path("<int:pk>/", views.RetrieveDestroyView.as_view(), name="bill"),
    path("<int:pk>/paid/", views.PaidView.as_view(), name="paid"),
    path("buildings/<int:pk>/", views.BillView.as_view(), name="bills"),
    path("my_bills/", views.ResidentBillsView.as_view(), name="my_bills"),
]
