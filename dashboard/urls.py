from django.urls import path
from .views import get_losers_data_api, get_gainers_data_api, get_money_rankings_api, get_bitcoin_price_api, get_future_rankings_api, get_historical_data_api, get_24h_data_api

urlpatterns = [
    path('api/usa_losers/', get_losers_data_api, name="usa_losers"),
    path('api/usa_gainers/', get_gainers_data_api, name="usa_gainers"),
    path('api/bitcoin_price/', get_bitcoin_price_api, name="bitcoin_price"),
    path('api/rankings/', get_future_rankings_api, name="rankings"),
    path('api/historical_data/', get_historical_data_api, name="historical_data"),
    path('api/24h_data/', get_24h_data_api, name="24h_data"),
    path('api/money_rankings/', get_money_rankings_api, name="money_rankings"),
]

# http://127.0.0.1:8000/api/usa_losers/
# http://127.0.0.1:8000/api/money_rankings/