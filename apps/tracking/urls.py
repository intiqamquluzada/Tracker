from rest_framework.routers import DefaultRouter
from apps.tracking.views import SubscriptionViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
