from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents import LlmAgent
import random

def book_hotel(location: str, nights: int) -> str:
    """
    Books a recommended hotel in the specified location for a set number of nights.
    Supported locations: NYC, LAX.
    """
    # Mapping of dummy hotels to specific locations
    inventory = {
        "NYC": ["The Empire Stay", "Central Park Suites", "Gotham Grand"],
        "LAX": ["Sunset Boulevard Inn", "Pacific View Resort", "Hollywood Hills Hotel"]
    }

    # Normalize input
    loc = location.upper().strip()
    
    if loc not in inventory:
        return f"Error: Location '{location}' is not supported. Please choose NYC or LAX."

    # Logic: The system automatically selects the first available hotel for the user
    selected_hotel = inventory[loc][0] 
    
    # Generate a dummy confirmation
    confirmation_id = f"RES-{loc}-{random.randint(1000, 9999)}"
    
    return (f"Success! I have booked your stay at **{selected_hotel}** in {loc} "
            f"for {nights} nights. Confirmation ID: {confirmation_id}.")


hotel_agent = LlmAgent(
    name="HotelBookingAgent",
    description="An agent that can search and book hotels using a remote hotel booking service.",
    model = "gemini-2.5-flash",
    tools = [book_hotel]
)



travel_agent = RemoteA2aAgent(
    name ="FlightBookingAgent",
    description = "An agent that can search and book flights using a remote flight booking service.",
    agent_card = f"http://localhost:8081/a2a/travel{AGENT_CARD_WELL_KNOWN_PATH}"

)

root_agent = LlmAgent(
    name = "OchestratorAgent",
    description = "This agent orchestrates between the flight booking agent and hotel booking agent to plan a complete trip for the user.",
    model = "gemini-2.5-flash",
    instruction= """
    You are a helpful travel assistant. 
    You can help users plan their trips by booking flights and hotels for them.
    """,
    sub_agents=[travel_agent, hotel_agent]
)