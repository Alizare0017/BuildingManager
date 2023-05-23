from django.urls import path

from . import views

urlpatterns = [
    path("", views.TicketsView.as_view(), name="tickets"),
    path("<int:pk>/", views.RetrieveTicketView.as_view(), name="ticket"),
    path("buildings/<int:pk>/", views.ManagerTicketView.as_view(), name="buildings_tickets")
]
