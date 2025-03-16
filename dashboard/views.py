from django.http import JsonResponse
from . import api, future_rankings, usastock, WigMoney, usastock2
import logging
logger = logging.getLogger(__name__)

def get_losers_data_api(request):
    losers = usastock2.get_losers_data()
    return JsonResponse({
        "usa_losers": losers,
    })

def get_gainers_data_api(request):
    gainers = usastock.get_gainers_data()
    return JsonResponse({
        "usa_gainers": gainers,
    })

def get_money_rankings_api(request):
    # Uzyskaj top10 wzrostów i spadków
    gainers, losers = WigMoney.get_money_rankings()
    return JsonResponse({
        "gainers": gainers,
        "losers": losers,
    })

def get_bitcoin_price_api(request):
    logger.info("🔍 Wywołano `get_bitcoin_price_api`")
    print("🔍 Wywołano `get_bitcoin_price_api`")  
    price = api.get_bitcoin_price()
    print(f"✅ Pobieram cenę Bitcoina: {price}")
    if price is None:
        logger.error("❌ Błąd: Nie udało się pobrać ceny Bitcoina")
        return JsonResponse({"error": "Nie udało się pobrać ceny Bitcoina"}, status=500)
    return JsonResponse({"bitcoin_price": price})

def get_future_rankings_api(request):
    gainers_24h, losers_24h, gainers_1h, losers_1h = future_rankings.get_futures_rankings()
    return JsonResponse({
        "gainers_24h": gainers_24h,
        "losers_24h": losers_24h,
        "gainers_1h": gainers_1h,
        "losers_1h": losers_1h,
    })


def get_historical_data_api(request):
    dates, closes = api.get_historical_data()
    if dates is None or closes is None:
        return JsonResponse({"error": "Brak danych historycznych"}, status=500)
    
    return JsonResponse({"dates": [str(d) for d in dates], "closes": closes})

def get_24h_data_api(request):
    dates, closes = api.get_24h_data()
    if dates is None or closes is None:
        return JsonResponse({"error": "Brak danych 24h"}, status=500)
    
    return JsonResponse({"dates": [str(d) for d in dates], "closes": closes})