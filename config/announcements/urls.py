from django.urls import path
from . import views
urlpatterns = [
    path("building/<int:pk>/", views.AnnouncementsView.as_view(), name="building_announcements"),
    path("<int:pk>/", views.RetrieveDestroyAnnouncementsView.as_view(), name="announcement")
]