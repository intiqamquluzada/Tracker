from django.urls import path
from config import consumers

websocket_urlpatterns = [
    path('ws/stock-price/', consumers.StockPriceConsumer.as_asgi()),
]
