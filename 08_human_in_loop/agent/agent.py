from google.adk.agents import LlmAgent
from dotenv import load_dotenv
import aiohttp

# load environment variables 
load_dotenv()

async def get_weather(city: str) -> str:
    """Fetches the weather information for a given city in Celsius.
    
    Args:
        city (str): Name of the city to get weather for
        
    Returns:
        str: Weather information with temperature in Celsius
    """
    endpoint = "https://wttr.in"

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{endpoint}/{city}?m") as response:
            return await response.text()
    


root_agent = LlmAgent(
    name="first_agent",
    description="This is my first agent",
    instruction="You are a helpful assistant.",
    model="gemini-2.0-flash",
    tools = [get_weather]
    
)


