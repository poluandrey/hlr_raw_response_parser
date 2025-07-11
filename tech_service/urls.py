from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

from alaris.views import get_accounts_by_carrier

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('system_tools.urls')),
    path("mnp/get-accounts/", get_accounts_by_carrier, name="get_accounts_by_carrier"),

]
# DOCS
urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui',
         ),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

# API
urlpatterns += [
    path('api/', include('tech_service.api_router')),
]
