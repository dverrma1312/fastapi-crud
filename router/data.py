from fastapi import FastAPI, APIRouter
from models import TravelData, TravelResponse
import asyncio

router = APIRouter(prefix="/data", tags=["DATA"])

@router.post("/")
async def get_data(travel_data: TravelData) -> TravelResponse:
    #implement the logic to validate teh start time should not be more than the end time and pass the data to the getweather data and the get currancy rate
    if travel_data.return_date < travel_data.travel_date:
        raise ValueError("Return date cannot be before travel date")
    weather_data, currency_rate = asyncio.gather(get_weather_data(travel_data.source, travel_data.destination, travel_data.travel_date, travel_data.return_date), get_currency_rate(travel_data.source, travel_data.destination))
    return TravelResponse(data=weather_data, hightemperature=weather_data["high_temperature"], lowtemperature=weather_data["low_temperature"], currencyrate=currency_rate)

