import requests
import concurrent.futures

# https://www.money.pl/gielda/indeksy_gpw/

def get_tradeable_symbols():
    """Pobiera tylko symbole, które są tradeable."""
    url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {s["symbol"] for s in data["symbols"] if s["status"] == "TRADING"}
    except Exception as e:
        print("Błąd pobierania exchangeInfo Futures:", e)
        return set()

def get_filtered_ticker_data():
    """Pobiera tickery, ale tylko dla tradeable symbols, redukując ilość pobieranych danych."""
    tradeable_symbols = get_tradeable_symbols()
    url = "https://api.binance.com/api/v3/ticker/24hr"
    
    if not tradeable_symbols:
        return []

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        all_tickers = response.json()
        return [ticker for ticker in all_tickers if ticker["symbol"] in tradeable_symbols]
    except Exception as e:
        print("Błąd pobierania danych 24h:", e)
        return []

def get_1h_change(symbol):
    """Pobiera zmianę procentową dla danej pary w ciągu 1h."""
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=2"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        if len(data) < 2:
            return None
        first_candle = data[0]
        second_candle = data[1]
        open_price = float(first_candle[1])
        close_price = float(second_candle[4])
        return round(((close_price - open_price) / open_price) * 100, 2)
    except Exception as e:
        print(f"Błąd pobierania danych 1h dla {symbol}:", e)
        return None

def get_binance_rankings():
    """Tworzy ranking kryptowalut według zmiany ceny w ciągu 24h i 1h."""
    tickers = get_filtered_ticker_data()
    results = []
    filtered_items = []

    for item in tickers:
        symbol = item.get("symbol")
        try:
            volume = float(item.get("volume", "0"))
            if volume <= 0:
                continue
            last_price = float(item.get("lastPrice"))
            change_24h = round(float(item.get("priceChangePercent")), 2)
        except Exception:
            continue
        filtered_items.append((symbol, last_price, change_24h))

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        future_to_symbol = {
            executor.submit(get_1h_change, symbol): (symbol, last_price, change_24h)
            for symbol, last_price, change_24h in filtered_items
        }
        for future in concurrent.futures.as_completed(future_to_symbol):
            symbol, last_price, change_24h = future_to_symbol[future]
            try:
                change_1h = future.result(timeout=5)
                if change_1h is None:
                    continue
                results.append({
                    "symbol": symbol,
                    "price": last_price,         # numeric for sorting
                    "change_24h": change_24h,      # numeric for sorting
                    "change_1h": round(change_1h, 2)
                })
            except Exception as exc:
                print(f"Symbol {symbol} wygenerował wyjątek: {exc}")
                continue

    return results

def format_result(item):
    """
    Formatuje wynik tak, aby cena była z trzema miejscami po przecinku,
    a zmiany procentowe zawsze z dwoma miejscami.
    """
    return {
        "symbol": item["symbol"],
        "price": f"{item['price']:.3f}",            # 3 decimal places
        "change_24h": f"{item['change_24h']:.2f}",     # 2 decimal places
        "change_1h": f"{item['change_1h']:.2f}"        # 2 decimal places
    }

def get_futures_rankings():
    """Zwraca top 5 rosnących i spadających kryptowalut w 24h i 1h."""
    data = get_binance_rankings()
    if not data:
        return None, None, None, None

    gainers_24h = sorted(data, key=lambda x: x["change_24h"], reverse=True)[:5]
    losers_24h = sorted(data, key=lambda x: x["change_24h"])[:5]
    gainers_1h = sorted(data, key=lambda x: x["change_1h"], reverse=True)[:5]
    losers_1h = sorted(data, key=lambda x: x["change_1h"])[:5]

    # Format results for display
    gainers_24h = [format_result(item) for item in gainers_24h]
    losers_24h = [format_result(item) for item in losers_24h]
    gainers_1h = [format_result(item) for item in gainers_1h]
    losers_1h = [format_result(item) for item in losers_1h]

    return gainers_24h, losers_24h, gainers_1h, losers_1h