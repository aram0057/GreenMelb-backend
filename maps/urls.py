from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MelbourneSuburbsViewSet, WasteViewSet, CentreViewSet

router = DefaultRouter()
router.register(r'suburbs', MelbourneSuburbsViewSet, basename='suburb')
router.register(r'wastes', WasteViewSet, basename='waste')
router.register(r'centres', CentreViewSet, basename='centre')  # The viewset for 'centres'

urlpatterns = [
    path('', include(router.urls)),
]
