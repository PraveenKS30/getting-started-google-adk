from google.adk.agents import LlmAgent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from dotenv import load_dotenv

load_dotenv()


def get_flight_search():
    """Search for flights with hardcoded source and destination."""
    flight_search_params = {
        "source": "NYC",
        "destination": "LAX",
        "departure_date": "2026-02-15",
        "return_date": "2026-02-22",
        "passengers": 2,
        "cabin_class": "economy",
        "airline_preference": "any"
    }
    
    # Mock flight results
    flight_results = [
        {
            "flight_id": "AA101",
            "airline": "American Airlines",
            "departure_time": "08:00 AM",
            "arrival_time": "11:30 AM",
            "duration": "5h 30m",
            "price": "$250",
            "stops": 0
        },
        {
            "flight_id": "UA202",
            "airline": "United Airlines",
            "departure_time": "10:15 AM",
            "arrival_time": "02:45 PM",
            "duration": "5h 30m",
            "price": "$220",
            "stops": 0
        },
        {
            "flight_id": "DL303",
            "airline": "Delta Airlines",
            "departure_time": "02:30 PM",
            "arrival_time": "06:00 PM",
            "duration": "5h 30m",
            "price": "$275",
            "stops": 1
        }
    ]
    
    return {
        "search_params": flight_search_params,
        "results": flight_results,
        "total_results": len(flight_results)
    }


def get_flight_booking():
    """Book a flight with hardcoded booking details."""
    booking_data = {
        "booking_id": "BK123456",
        "confirmation_number": "ABC123XYZ",
        "flight_id": "AA101",
        "airline": "American Airlines",
        "departure_date": "2026-02-15",
        "departure_time": "08:00 AM",
        "arrival_time": "11:30 AM",
        "departure_airport": "JFK",
        "arrival_airport": "LAX",
        "passengers": [
            {
                "passenger_id": "P001",
                "name": "John Doe",
                "email": "john.doe@email.com",
                "phone": "+1-555-0101",
                "seat": "12A",
                "meal_preference": "Vegetarian"
            },
            {
                "passenger_id": "P002",
                "name": "Jane Smith",
                "email": "jane.smith@email.com",
                "phone": "+1-555-0102",
                "seat": "12B",
                "meal_preference": "Non-Vegetarian"
            }
        ],
        "booking_status": "Confirmed",
        "total_price": "$500",
        "currency": "USD",
        "payment_method": "Credit Card",
        "booking_date": "2026-01-22",
        "baggage_allowance": "2 carry-on + 1 checked",
        "cancellation_policy": "Free cancellation until 24 hours before departure"
    }
    
    return booking_data

root_agent = LlmAgent(
    name = "travel_agent",
    description = "This is my travel agent",
    instruction= """
    You are a helpful travel assistant.
    Please use the get_flight_search function to search for flights.
    Use the get_flight_booking function to book a flight.
    """,
    model = "gemini-2.0-flash",
    tools = [get_flight_search, get_flight_booking]
    
)

a2a_app = to_a2a(root_agent, port=8081)
