from rest_framework.routers import DefaultRouter
from apps.tracking.views import SubscriptionViewSet, AlertViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'alerts', AlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
