import os
import time
from google.adk.agents import Agent

USD_PER_INR = 0.012


def get_weather(city: str) -> dict:
    """Returns the current weather for a city.

    Args:
        city: Name of the city, e.g. "Paris".
    """
    if os.environ.get("SLOW_WEATHER") == "1":
        time.sleep(8)  # simulates a slow upstream API
    fake_weather = {
        "paris": {"temp_c": 18, "condition": "cloudy"},
        "tokyo": {"temp_c": 24, "condition": "sunny"},
        "goa": {"temp_c": 31, "condition": "humid"},
    }
    data = fake_weather.get(city.lower())
    if data is None:
        return {"status": "error", "message": f"No weather data for {city}"}
    return {"status": "ok", "city": city, **data}


def get_flight_price(origin: str, destination: str) -> dict:
    """Returns the cheapest one-way flight price in US dollars (USD).

    Args:
        origin: Departure city, e.g. "Delhi".
        destination: Arrival city, e.g. "Paris".
    """
    prices_inr = {
        ("delhi", "paris"): 54000,
        ("delhi", "tokyo"): 48000,
        ("delhi", "goa"): 5400,
    }
    price_inr = prices_inr.get((origin.lower(), destination.lower()))
    if price_inr is None:
        return {"status": "error", "message": "Route not found"}
    # Fixed since Video 1: convert to USD so the docstring is true.
    return {"status": "ok", "origin": origin, "destination": destination,
            "price": round(price_inr * USD_PER_INR), "currency": "USD"}


def get_hotel_options(city: str) -> dict:
    """Returns a short list of hotels for a city with nightly price in USD.

    Args:
        city: Name of the city, e.g. "Tokyo".
    """
    if os.environ.get("FAIL_HOTELS") == "1":
        raise RuntimeError("Hotel provider timed out")
    hotels = {
        "paris": [{"name": "Hotel Lumiere", "usd_per_night": 140}],
        "tokyo": [{"name": "Sakura Stay", "usd_per_night": 95}],
        "goa": [{"name": "Beachside Inn", "usd_per_night": 60}],
    }
    options = hotels.get(city.lower())
    if options is None:
        return {"status": "error", "message": f"No hotels for {city}"}
    return {"status": "ok", "city": city, "hotels": options}




root_agent = Agent(
    name="travel_agent",
    model="gemini-flash-latest",
    description="A friendly travel helper.",
    instruction=(
        "You are a helpful travel assistant. Use your tools to answer questions "
        "about weather, flights and hotels. Always answer briefly and mention prices."
    ),
    tools=[get_weather, get_flight_price, get_hotel_options]
)
