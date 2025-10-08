import os
import logging
import re
import wikipedia
from newsapi import NewsApiClient
from alpha_vantage.timeseries import TimeSeries
import openmeteo_requests
import requests_cache
from retry_requests import retry
import requests

# Set up logging
logger = logging.getLogger(__name__)

# --- Tool Functions ---

def calculator(expression: str) -> str:
    """Evaluates simple, safe math expressions."""
    try:
        if re.match(r'^[\d\s\+\-\*/\(\)\.]+$', expression):
            return str(eval(expression))
        else:
            return "Invalid math expression. Only numbers and basic operators are allowed."
    except Exception as e:
        logger.error(f"Calculator error: {e}")
        return "Calculation failed. Check the math expression."

def get_news(topic: str) -> str:
    """Fetches recent news articles about a specific topic."""
    try:
        newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))
        all_articles = newsapi.get_everything(q=topic, language='en', sort_by='relevancy', page_size=3)
        
        articles = all_articles.get('articles', [])
        if not articles:
            return f"No recent news found for '{topic}'."
        
        summary = f"Here are the top headlines for '{topic}':\n"
        for article in articles:
            summary += f"- {article['title']}: {article.get('description', 'No description available.')}\n"
        return summary
    except Exception as e:
        logger.error(f"News API error: {e}")
        return f"Error fetching news: {str(e)}"

def get_weather(city: str) -> str:
    """Provides the current weather conditions for a given city."""
    try:
        # --- STEP 1: Geocoding (Robust version) ---
        geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        geocoding_params = {"name": city, "count": 1, "language": "en", "format": "json"}
        
        geo_response = requests.get(geocoding_url, params=geocoding_params)
        geo_response.raise_for_status() 
        
        geo_data = geo_response.json()
        logger.info(f"Geocoding API response for '{city}': {geo_data}")

        results = geo_data.get("results")
        if not results:
            logger.warning(f"Geocoding failed for city '{city}'. No 'results' key in response.")
            return f"Could not find a location for '{city}'. Please provide a more specific name or check for typos."

        location_data = results[0]
        lat = location_data["latitude"]
        lon = location_data["longitude"]
        location_name = location_data.get("name", city)
        location_country = location_data.get("country", "")

        # --- STEP 2: Weather forecast (with Vercel-compatible caching) ---
        # --- THE FIX IS HERE ---
        # We tell requests_cache to store its database in the only writable directory on Vercel: /tmp
        cache_session = requests_cache.CachedSession('/tmp/weather_cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "apparent_temperature", "precipitation", "wind_speed_10m"]
        }
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        current = response.Current()
        
        return (f"Current weather in {location_name}, {location_country}: "
                f"Temperature: {current.Variables(0).Value():.2f}°C "
                f"Feels like: {current.Variables(1).Value():.2f}°C "
                f"Precipitation: {current.Variables(2).Value():.2f}mm "
                f"Wind Speed: {current.Variables(3).Value():.2f}km/h")

    except requests.exceptions.HTTPError as e:
        logger.error(f"Geocoding HTTP error for city '{city}': {e.response.text}")
        return f"There was a network problem finding the city '{city}'."
    except Exception as e:
        logger.error(f"Weather API error: {e}", exc_info=True)
        return f"An unexpected error occurred while fetching weather for '{city}'."

def get_stock_price(ticker_symbol: str) -> str:
    """Gets the latest stock price for a company using its stock ticker symbol."""
    try:
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            return "Error: ALPHA_VANTAGE_API_KEY is not set."

        ts = TimeSeries(key=api_key, output_format='json')
        data, meta_data = ts.get_quote_endpoint(symbol=ticker_symbol)
        
        logger.info(f"Alpha Vantage raw data for {ticker_symbol}: {data}")

        if not data:
            return f"No data returned from the stock API for '{ticker_symbol}'. This could be due to an invalid ticker or API rate limits."

        price = data.get('05. price')
        if not price:
            error_note = data.get('Note')
            if error_note:
                return f"Stock API error for '{ticker_symbol}': {error_note}"
            return f"Could not find the price in the API response for '{ticker_symbol}'."

        return f"The latest stock price for {ticker_symbol} is ${float(price):.2f}."
    
    except Exception as e:
        logger.error(f"Stock price error for {ticker_symbol}: {e}", exc_info=True)
        return f"Error fetching stock price: {str(e)}"

def get_wikipedia_summary(search_term: str) -> str:
    """Retrieves a concise summary of a topic from Wikipedia."""
    try:
        summary = wikipedia.summary(search_term, sentences=2, auto_suggest=False)
        return summary
    except wikipedia.exceptions.PageError:
        return f"Sorry, I couldn't find a Wikipedia page for '{search_term}'."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"'{search_term}' is ambiguous. Please be more specific. Options might include: {e.options[:3]}"
    except Exception as e:
        logger.error(f"Wikipedia error: {e}")
        return f"An error occurred while searching Wikipedia: {str(e)}"


