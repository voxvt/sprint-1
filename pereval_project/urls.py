from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

from pereval.views import UserViewset, CoordsViewset, LevelViewset, ImageViewset, PerevalViewset


router = routers.DefaultRouter()
router.register(r'users', UserViewset, basename='users')
router.register(r'coords', CoordsViewset, basename='coords')
router.register(r'levels', LevelViewset, basename='levels')
router.register(r'images', ImageViewset, basename='images')
router.register(r'perevals', PerevalViewset, basename='perevals')


schema_view = get_schema_view(
    openapi.Info(
        title="Pereval API",
        default_version='v1',
        description="API для приложения Pereval",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@pereval.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
