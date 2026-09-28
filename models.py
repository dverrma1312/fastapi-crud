from pydantic import BaseModel

class TravelData(BaseModel):
    source: str
    destination: str
    travel_date: str
    return_date: str

class TravelResponse(BaseModel):
    data: dict
    hightemperature: float
    lowtemperature: float
    currencyrate: float
    