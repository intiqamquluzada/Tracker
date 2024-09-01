from rest_framework import serializers
from apps.tracking.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'stock']
        read_only_fields = ['user']  #
