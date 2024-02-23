import os
import datetime
from dotenv import load_dotenv
from newsapi import NewsApiClient
import re
import requests
from wolframalpha import Client

load_dotenv(dotenv_path='C:\\Users\\VAISHNAVI\\Desktop\\vaishnavi\\project\\data.env')

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
WOLFRAMALPHA_API_KEY = os.getenv('WOLFRAMALPHA_API_KEY')
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
news = NewsApiClient(api_key=NEWS_API_KEY)

def get_ip(_return=False):
    try:
        response = requests.get(f'http://ip-api.com/json/').json()
        if _return:
            return response
        else:
            return f'Your IP address is {response["query"]}'
    except Exception as e:
        print("Error fetching IP:", e)
        return None

def get_news():
    try:
        top_news = ""
        top_headlines = news.get_top_headlines(language="en", country="in")
        for article in top_headlines.get("articles", []):
            title = article.get("title", "")
            if isinstance(title, str):
                title = re.sub(r'[|-] [A-Za-z0-9 |:.]*', '', title).replace("’", "'")
                top_news += title + '\n'
        return top_news
    except Exception as e:
        print("Error fetching news:", e)
        return None

def get_weather(city=''):
    try:
        if city:
            response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric').json()
        else:
            response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={get_ip(True)["city"]}&appid={OPENWEATHERMAP_API_KEY}&units=metric').json()
        if 'main' in response and 'weather' in response:
            weather = f'It\'s {response["main"]["temp"]}° Celsius and {response["weather"][0]["main"]}\n' \
                    f'But feels like {response["main"]["feels_like"]}° Celsius\n' \
                    f'Wind is blowing at {round(response["wind"]["speed"] * 3.6, 2)}km/h\n' \
                    f'Visibility is {int(response["visibility"] / 1000)}km'
            return weather
        else:
            return "Weather data not available."
    except Exception as e:
        print("Error fetching weather:", e)
        return None

def get_general_response(query):
    client = Client(app_id=WOLFRAMALPHA_API_KEY)
    try:
        response = client.query(query)
        return next(response.results).text
    except (StopIteration, AttributeError) as e:
        print("Error fetching general response:", e)
        return None

# Example usage:
print("Fetching news...")
news_content = get_news()
if news_content:
    print(news_content)

print("Fetching weather...")
weather_info = get_weather()
if weather_info:
    print(weather_info)

print("Fetching general response...")
query = "What is the capital of France?"
response = get_general_response(query)
if response:
    print(response)
