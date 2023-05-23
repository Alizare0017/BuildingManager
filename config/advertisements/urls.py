from django.urls import path

from . import views

urlpatterns = [
    path("", views.AdvertisementView.as_view(), name="advertisements"),
    path("<int:pk>/", views.DestroyAddView.as_view(), name="delete_ad")
]
