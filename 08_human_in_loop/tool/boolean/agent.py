from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from dotenv import load_dotenv
import requests

# load environment variables 
load_dotenv()

def get_weather(city: str) -> str:
    """Fetches the weather information for a given city in Celsius.
    
    Args:
        city (str): Name of the city to get weather for
        
    Returns:
        str: Weather information with temperature in Celsius
    """
    endpoint = "https://wttr.in"
    # Adding m for metric units (Celsius)
    response = requests.get(f"{endpoint}/{city}?m")
    return response.text

def get_confirmation(city: str) -> bool:
    return city.lower() in ["new york", "san francisco", "los angeles", "chicago", "houston"]

root_agent = LlmAgent(
    name="first_agent",
    description="This is my first agent",
    instruction="You are a helpful assistant.",
    model="gemini-2.0-flash",
    tools = [FunctionTool(get_weather, require_confirmation=get_confirmation) ]
    
)
