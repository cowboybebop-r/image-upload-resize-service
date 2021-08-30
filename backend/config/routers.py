from django.urls import path
from rest_framework.routers import DefaultRouter

from api.viewsets import ImageViewSet

router = DefaultRouter()

router.register(r'images', ImageViewSet, basename='images-api')

urlpatterns = [
    path('images/<int:pk>/resize', ImageViewSet.as_view({'put': 'resize'}), name='resize-image')
] + router.urls
