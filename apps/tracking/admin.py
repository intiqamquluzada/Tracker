from django.contrib import admin
from apps.tracking.models import (PriceHistory, Stock, Subscription, Alert)

admin.site.register(PriceHistory)
admin.site.register(Stock)
admin.site.register(Subscription)
admin.site.register(Alert)

