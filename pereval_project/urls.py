from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from pereval.views import UserViewset, CoordsViewset, LevelViewset, ImageViewset, PerevalViewset



router = routers.DefaultRouter()
router.register(r'users', UserViewset, basename='users')
router.register(r'coords', CoordsViewset, basename='coords')
router.register(r'levels', LevelViewset, basename='levels')
router.register(r'images', ImageViewset, basename='images')
router.register(r'perevals', PerevalViewset, basename='perevals')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    ]

