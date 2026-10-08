"""
URL configuration for healthcare_backend project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView
)


def root_api_overview(request):
    """Root endpoint providing quick API overview and documentation links."""
    return JsonResponse({
        'name': 'Healthcare Backend API',
        'version': '1.0.0',
        'status': 'healthy',
        'documentation': {
            'swagger': '/api/docs/',
            'redoc': '/api/redoc/',
            'schema': '/api/schema/',
        },
        'endpoints': {
            'authentication': {
                'register': 'POST /api/auth/register/',
                'login': 'POST /api/auth/login/',
                'current_user': 'GET /api/auth/me/',
                'token_refresh': 'POST /api/auth/token/refresh/',
            },
            'patients': {
                'list_and_create': 'GET / POST /api/patients/',
                'detail_update_delete': 'GET / PUT / PATCH / DELETE /api/patients/<id>/',
            },
            'doctors': {
                'list_and_create': 'GET / POST /api/doctors/',
                'detail_update_delete': 'GET / PUT / PATCH / DELETE /api/doctors/<id>/',
            },
            'mappings': {
                'assign_or_list_all': 'POST / GET /api/mappings/',
                'get_patient_doctors': 'GET /api/mappings/<patient_id>/',
                'remove_mapping': 'DELETE /api/mappings/<id>/',
            }
        }
    })


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Health / Overview
    path('', root_api_overview, name='root-overview'),
    path('api/', root_api_overview, name='api-overview'),

    # Application APIs
    path('api/auth/', include('authentication.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/doctors/', include('doctors.urls')),
    path('api/mappings/', include('mappings.urls')),

    # API Documentation (Swagger & ReDoc)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
