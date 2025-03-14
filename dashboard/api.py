import requests
import datetime

def get_bitcoin_price():
  print("pobieram API...")
  url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
  try:
    response = requests.get(url,timeout=5)
    response.raise_for_status()
    data = response.json()
    price_str = data.get("price")
    price = float(price_str)
    formatted_price = f"{price:.2f}"
    return formatted_price
  except requests.RequestException as e:
    print("Błąd połaczenia z API BITCOIN PRICE",e)
    return None
  except (KeyError,ValueError) as e:
    print("Błąd podczas przetwarzania danych:",e)
    return None
  
def get_historical_data():
  url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=30"
  try:
    response = requests.get(url,timeout=5)
    response.raise_for_status()
    data = response.json()
    dates = []
    closes = []
    for candle in data:
      open_time = candle[0]
      dt = datetime.datetime.fromtimestamp(open_time / 1000)
      dates.append(dt)
      close_price = float(candle[4])
      closes.append(close_price)
    return dates,closes
  except Exception as e:
    print("Błąd podczas pobierania historycznych danych BTC:",e)
    return None, None

def get_24h_data():
  url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=24"
  try:
    response = requests.get(url,timeout=5)
    response.raise_for_status()
    data = response.json()
    dates = []
    closes = []
    for candle in data:
      open_time = candle[0]
      dt = datetime.datetime.fromtimestamp(open_time / 1000)
      dates.append(dt)
      close_price = float(candle[4])
      closes.append(close_price)
    return dates, closes
  except Exception as e:
    print("łąd pobierania danych 24h bitcoin:",e)
    return None, None