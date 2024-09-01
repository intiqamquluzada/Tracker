from rest_framework import serializers
from apps.tracking.models import Subscription, Alert


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('id', 'user', 'stock')
        read_only_fields = ('user',)


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ("threshold_price", "user", "stock", "triggered")
        read_only_fields = ('user',)