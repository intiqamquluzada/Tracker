import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

# Set up logging
logger = logging.getLogger(__name__)


class StockPriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            # Add the WebSocket connection to the stock price group
            await self.channel_layer.group_add(
                'stock_price_group',
                self.channel_name
            )
            # Accept the WebSocket connection
            await self.accept()
            logger.info(f"WebSocket connection established: {self.channel_name}")
        except Exception as e:
            logger.error(f"Error in connect method: {e}")

    async def disconnect(self, close_code):
        try:
            # Remove the WebSocket connection from the stock price group
            await self.channel_layer.group_discard(
                'stock_price_group',
                self.channel_name
            )
            logger.info(f"WebSocket connection closed: {self.channel_name}")
        except Exception as e:
            logger.error(f"Error in disconnect method: {e}")

    async def stock_price_update(self, event):
        symbol = event['symbol']
        price = event['price']
        try:
            # Send the stock price update to the WebSocket client
            await self.send(text_data=json.dumps({
                'symbol': symbol,
                'price': price
            }))
        except Exception as e:
            logger.error(f"Error sending stock price update: {e}")
