from router import data
from models import TravelData, TravelResponse
from services.cache import get_cache, set_cache
import httpx

async def get_weather_data(source: str, destination: str, travel_date: str, return_date: str) -> dict:
    # Implement the logic to fetch weather data from an external API
    #check if the data is already in cache, if yes return the cached data, if not fetch from the API and store it in cache
    cachhe_key = f"{source}_{destination}_{travel_date}_{return_date}"
    data = get_cache(cachhe_key)
    if data is not None:
        return data 
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weatherapi.com/v1/forecast.json?key=YOUR_API_KEY&q={destination}&dt={travel_date}&end_dt={return_date}")
        response.raise_for_status()
        data =  response.json()
        forecast = []
        for day in data["forecast"]["forecastday"]:
            forecast.append({
                "date": day["date"],
                "high_temperature": day["day"]["maxtemp_c"],
                "low_temperature": day["day"]["mintemp_c"]
            })
        set_cache(cachhe_key, {"forecast": forecast}, 3600)  # Cache for 1 hour
        return {"forecast": forecast}