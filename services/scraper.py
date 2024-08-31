from bs4 import BeautifulSoup
import requests

def get_stock_price(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    price = soup.find("fin-streamer", {"data-field": "regularMarketPrice"}).text
    return price
