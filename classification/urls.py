from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import ImageUploadView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='upload_file'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
