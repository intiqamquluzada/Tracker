import logging
from django.db import transaction
from datetime import datetime, timedelta
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import requests
from bs4 import BeautifulSoup
from django.core.mail import send_mail
from django.urls import reverse
from apps.tracking.models import Stock, PriceHistory, Alert, Subscription
from config.predicter import predicter
from django.conf import settings
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

                with transaction.atomic():
                    price_history, created = PriceHistory.objects.get_or_create(
                        stock=stock,
                        date=date_today,
                        defaults={'price': price}
                    )
                    if not created:
                        price_history.price = price
                        price_history.save()

                async_to_sync(channel_layer.group_send)(
                    'stock_price_group',
                    {
                        'type': 'stock_price_update',
                        'symbol': stock.symbol,
                        'price': price
                    }
                )

                check_and_trigger_alerts(stock, price)

                end_date = date_today + timedelta(days=365)
                logger.info(f"BURA BAX--> {stock.symbol}, {str(date_today)}, {str(end_date)}")
                next_price = predicter(symbol=stock.symbol, start_date=str(date_today), end_date=str(end_date))

                if next_price is not None:
                    stock.expected_price = next_price
                    stock.save()

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
            logger.info(f"PRICEEE---{float(price_element.get_text().replace(',', ''))}")
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
    # Implementing of the logic to notify the user
    logger.info(f"Notification sent to {user.full_name} for stock {symbol} at price {price}")
    # Send an email
    send_mail(f"Dear, {user.full_name}"
,
              f"""You can visit page, and see changing price of item:
{symbol}={price}""",
              settings.EMAIL_HOST_USER,
              [user.email],
              fail_silently=False,

              )

