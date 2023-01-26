import pip
import requests
from datetime import *
import os
import config
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = config.my_stock_api
NEWS_API_KEY = config.my_news_api

twilio_account_sid = config.twilio_account_sid
twilio_auth_token = config.twilio_auth_token
client = Client(twilio_account_sid, twilio_auth_token)
twilio_phone_number = config.twilio_phone_num
my_phone_number = config.my_phone_num

date = datetime.today() - timedelta(days=5)
print(date)
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

news_params = {
    "q": COMPANY_NAME,
    "from": str(date),
    "sortBy": "popularity",
    "language": "en",
    "apiKey": NEWS_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
stock_data = response.json()

stock_info = [key for (key, value) in stock_data.items()]
a = stock_info[1]

stock_closing = [value for (key, value) in stock_data[a].items()]


stock_close_yesterday = float(stock_closing[0]['4. close'])
stock_close_before = float(stock_closing[1]['4. close'])

closing_difference = stock_close_yesterday - stock_close_before

closing_difference_percentage = round(((closing_difference / stock_close_before) * 100), 2)

print(closing_difference_percentage)

if closing_difference_percentage > 3 or closing_difference_percentage < 3:
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    print(news_data)

for _ in range(1, 4):
    top_3_news = [news_data["articles"][_]]
    print(top_3_news)
    message = client.messages.create(body=f"{STOCK_NAME}: 🔺{closing_difference_percentage}%\n"
                                          f"Headline: {top_3_news[0]['title']}\n"
                                          f"Brief: {top_3_news[0]['content']}\n",
                                     from_=twilio_phone_number,
                                     to=my_phone_number)

