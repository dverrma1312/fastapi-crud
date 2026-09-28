import asyncio
from fastapi import APIRouter, HTTPException
from models import TravelData, TravelResponse
from services.getdata import get_weather_data, get_currency_rate

router = APIRouter(prefix="/data", tags=["DATA"])


@router.post("", response_model=TravelResponse)
@router.post("/", response_model=TravelResponse)
async def get_data(travel_data: TravelData) -> TravelResponse:
    # Validate that return_date is not before travel_date
    if travel_data.return_date < travel_data.travel_date:
        raise HTTPException(
            status_code=400,
            detail="Return date cannot be before travel date"
        )

    weather_data, currency_rate = await asyncio.gather(
        get_weather_data(
            travel_data.source,
            travel_data.destination,
            travel_data.travel_date,
            travel_data.return_date,
        ),
        get_currency_rate(travel_data.source, travel_data.destination),
    )

    return TravelResponse(
        data=weather_data,
        hightemperature=weather_data["high_temperature"],
        lowtemperature=weather_data["low_temperature"],
        currencyrate=currency_rate,
    )
