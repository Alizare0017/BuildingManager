from django.contrib import admin
from django.urls import path, include


from rest_framework.urlpatterns import format_suffix_patterns
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/buildings/", include("buildings.urls")),
    path("api/announcements/", include("announcements.urls")),
    path("api/tickets/", include("tickets.urls")),
    path("api/financials/", include("financials.urls")),
    path("api/advertisement/", include("advertisements.urls")),
    path("api/polls/", include("poll.urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

format_suffix_patterns(urlpatterns)
