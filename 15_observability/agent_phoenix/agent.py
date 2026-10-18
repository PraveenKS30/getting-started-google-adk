"""Demo agent for Video 1: a tiny travel helper built with Google ADK.

It has one deliberate flaw: get_flight_price() returns an amount in INR
while its docstring (which the model reads) promises USD. Nothing crashes,
but the agent's answer is confidently wrong. A trace shows exactly why.
"""

# --- Tracing (added in Step 3 of the video; leave commented out for Step 2) ---
from phoenix.otel import register

register(
    project_name="travel-agent",  # shows up as a project in Phoenix
    auto_instrument=True,         # picks up openinference-instrumentation-google-adk
) 

from google.adk.agents import Agent


def get_weather(city: str) -> dict:
    """Returns the current weather for a city.

    Args:
        city: Name of the city, e.g. "Paris".
    """
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
    # BUG (on purpose): the number below is in Indian rupees, not dollars.
    prices_inr = {
        ("delhi", "paris"): 54000,
        ("delhi", "tokyo"): 48000,
        ("delhi", "goa"): 5400,
    }
    price = prices_inr.get((origin.lower(), destination.lower()))
    if price is None:
        return {"status": "error", "message": "Route not found"}
    return {"status": "ok", "origin": origin, "destination": destination,
            "price": price, "currency": "INR"}


def get_hotel_options(city: str) -> dict:
    """Returns a short list of hotels for a city with nightly price in USD.

    Args:
        city: Name of the city, e.g. "Tokyo".
    """
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
    tools=[get_weather, get_flight_price, get_hotel_options],
)
