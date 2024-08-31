import logging
from datetime import datetime
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests
from bs4 import BeautifulSoup
from apps.tracking.models import Stock, PriceHistory, Alert, Subscription
from django.db import transaction

# Set up logging
logger = logging.getLogger(__name__)

@shared_task
def fetch_and_broadcast_stock_prices():
    channel_layer = get_channel_layer()
    if not channel_layer:
        logger.error("Channel layer is None. Ensure it is properly initialized.")
        return

    stocks = Stock.objects.all()

    for stock in stocks:
        try:
            price = get_stock_price(stock.symbol)
            if price is not None:
                date_today = datetime.now().date()

                # Store price history in a transaction
                with transaction.atomic():
                    # Check if price history record already exists
                    price_history, created = PriceHistory.objects.get_or_create(
                        stock=stock,
                        date=date_today,
                        defaults={'price': price}
                    )

                    if not created:
                        # If record already exists, update the price
                        price_history.price = price
                        price_history.save()

                # Broadcast the price update
                async_to_sync(channel_layer.group_send)(
                    'stock_price_group',
                    {
                        'type': 'stock_price_update',
                        'symbol': stock.symbol,
                        'price': price
                    }
                )

                # Check and trigger alerts
                check_and_trigger_alerts(stock, price)

                logger.info(f"Successfully broadcasted and saved price for {stock.symbol}: {price}")
            else:
                logger.warning(f"No price returned for {stock.symbol}")
        except Exception as e:
            logger.error(f"Failed to fetch or broadcast price for {stock.symbol}: {e}")

def get_stock_price(symbol):
    # URL for scraping stock price from Yahoo Finance
    api_url = f"https://finance.yahoo.com/quote/{symbol}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example of extracting price from Yahoo Finance
        price_element = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
        if price_element:
            return float(price_element.get_text().replace(',', ''))  # Convert to float
        else:
            logger.warning(f"Price element not found for {symbol}")
            return None
    except requests.RequestException as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        return None  # Return None or a default value if the API request fails

def check_and_trigger_alerts(stock, price):
    # Check and trigger alerts for the given stock
    alerts = Alert.objects.filter(stock=stock, triggered=False)
    for alert in alerts:
        if price >= alert.threshold_price:
            alert.triggered = True
            alert.save()
            notify_user(alert.user, stock.symbol, price)

def notify_user(user, symbol, price):
    # Implement the logic to notify the user (e.g., send an email, push notification, etc.)
    logger.info(f"Notification sent to {user.full_name} for stock {symbol} at price {price}")
    # Add actual notification logic here (e.g., send an email)
