from django.urls import path
from system_tools.views import health_check


urlpatterns = [
    path('healthcheck', view=health_check),
]
