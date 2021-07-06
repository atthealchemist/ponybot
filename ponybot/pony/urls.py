from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import PonyViewSet

router = DefaultRouter()
router.register(r'ponies', PonyViewSet)
