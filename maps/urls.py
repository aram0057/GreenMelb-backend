from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WasteViewSet, CentreViewSet

router = DefaultRouter()
router.register(r'wastes', WasteViewSet)
router.register(r'centres', CentreViewSet)  # Register the CentreViewSet

urlpatterns = [
    path('', include(router.urls)),
]
