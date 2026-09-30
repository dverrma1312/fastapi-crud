# Weather Vision API (Netravision)

A high-performance FastAPI service designed for travel planning. It aggregates weather forecasts and currency exchange rates concurrently using asynchronous Python, backed by an in-memory TTL caching layer.

---

## Features

- **Concurrent Data Fetching**: Utilizes `asyncio.gather` to query weather forecasts and currency conversion rates in parallel.
- **In-Memory TTL Caching**: Caches external API responses to minimize latency and avoid exceeding third-party rate limits.
- **Smart Currency & Location Resolution**: Automatically maps common city and country names to ISO currency codes, while supporting direct 3-letter currency codes.
- **Offline / Fallback Resilience**: Seamlessly falls back to baseline values if external APIs are unreachable or unconfigured.
- **Input Validation**: Enforces strict date checks (e.g., verifying that the return date is not prior to the departure date).

---

## Project Structure

```text
├── main.py              # FastAPI app initialization and route mounting
├── models.py            # Pydantic models for request and response validation
├── config.py            # Environment variable loading via python-dotenv
├── requirements.txt     # Python dependencies
├── router/
│   └── data.py          # API route definitions (/data endpoint)
└── services/
    ├── cache.py         # In-memory TTL cache implementation
    └── getdata.py       # Weather and currency fetching & fallback logic
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/dverrma1312/fastapi-crud.git
cd fastapi-crud
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)

Create a `.env` file in the root directory:

```env
WEATHER_API_KEY=your_weatherapi_key_here
GEMINI_API_KEY=your_gemini_api_key_here
EXCHANGE_RATE_API_KEY=your_exchange_rate_key_here
```

> **Note:** If no API keys are provided, the service runs in resilient fallback mode with simulated forecasts and standard baseline currency rates.

---

## Running the Application

Start the development server using `uvicorn`:

```bash
uvicorn main:app --reload
```

The service will be available at:
- **API Base URL**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/docs`
- **Alternative ReDoc**: `http://127.0.0.1:8000/redoc`

---

## API Endpoints

### 1. Health Check / Root

- **Method**: `GET`
- **Path**: `/`
- **Response**:
  ```json
  {
    "message": "Welcome to Weather API!"
  }
  ```

---

### 2. Travel Weather & Currency Data

- **Method**: `POST`
- **Path**: `/data` (or `/data/`)
- **Request Body**:

  ```json
  {
    "source": "New York",
    "destination": "London",
    "travel_date": "2026-10-01",
    "return_date": "2026-10-05"
  }
  ```

- **Success Response (`200 OK`)**:

  ```json
  {
    "data": {
      "source": "New York",
      "destination": "London",
      "travel_date": "2026-10-01",
      "return_date": "2026-10-05",
      "high_temperature": 26.5,
      "low_temperature": 18.0,
      "forecast": [
        {
          "date": "2026-10-01",
          "high_temperature": 26.5,
          "low_temperature": 18.0
        },
        {
          "date": "2026-10-02",
          "high_temperature": 26.5,
          "low_temperature": 18.0
        }
      ]
    },
    "hightemperature": 26.5,
    "lowtemperature": 18.0,
    "currencyrate": 0.78
  }
  ```

- **Validation Error (`400 Bad Request`)**:
  Returned when `return_date` precedes `travel_date`:

  ```json
  {
    "detail": "Return date cannot be before travel date"
  }
  ```

---

## Running Tests

Run the endpoint test script using the virtual environment:

```bash
./venv/bin/python -c "
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
res = client.get('/')
assert res.status_code == 200
print('Tests passed successfully!')
"
```
