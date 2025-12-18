from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
import requests
from google.genai import types

def after_agent_call(callback_context: CallbackContext) -> types.Content:
    final_output = callback_context.state.get("weather_info")
    if final_output and "sunny" in final_output:
        return None 
    else : 
        return types.Content(
            parts=[types.Part(text=f"Agent {callback_context.agent_name} output modified by after_agent_callback: Weather is not sunny.")]
        )



def get_weather(city: str) -> str:
    """Fetches the weather information for a given city with hardcoded values.
    
    Args:
        city (str): Name of the city to get weather for
        
    Returns:
        str: Weather information with temperature in Celsius and condition
    """
    # Hardcoded weather data for different cities
    weather_data = {
        "london": {"temperature": 12, "condition": "rainy", "description": "Light rain with occasional showers"},
        "new york": {"temperature": 15, "condition": "sunny", "description": "Clear skies with bright sunshine"},
        "sydney": {"temperature": 28, "condition": "sunny", "description": "Warm and sunny with blue skies"},
        "tokyo": {"temperature": 18, "condition": "windy", "description": "Strong winds with partly cloudy skies"},
        "dubai": {"temperature": 35, "condition": "sunny", "description": "Hot and sunny with clear conditions"},
        "moscow": {"temperature": 5, "condition": "rainy", "description": "Cold and rainy with overcast skies"},
        "paris": {"temperature": 14, "condition": "windy", "description": "Breezy conditions with scattered clouds"},
        "toronto": {"temperature": 10, "condition": "rainy", "description": "Wet and rainy weather throughout the day"},
        "bangalore": {"temperature": 26, "condition": "sunny", "description": "Warm and sunny with gentle breeze"},
        "seattle": {"temperature": 8, "condition": "rainy", "description": "Drizzly and rainy with dark clouds"}
    }
    
    # Normalize city name to lowercase for lookup
    city_lower = city.lower().strip()
    
    # Check if city exists in our data, otherwise return a default response
    if city_lower in weather_data:
        data = weather_data[city_lower]
        return f"Weather for {city.title()}:\nTemperature: {data['temperature']}°C\nCondition: {data['condition'].capitalize()}\nDetails: {data['description']}"
    else:
        return f"Weather data for {city.title()} is not available in the system. Available cities: {', '.join(weather_data.keys())}"


root_agent = LlmAgent(
    name="first_agent",
    description="This is my first agent",
    instruction="""
        You are a helpful weather assistant. 
        Your ONLY purpose is to provide weather information using the provided tools. 
        IMPORTANT: If you see previous user queries in the conversation history that 
        were skipped, ignored, or not about weather, you must STRICTLY IGNORE them. 
        Focus ONLY on addressing the very last user message.
""",
    model="gemini-2.0-flash",
    tools = [get_weather],
    output_key ="weather_info",
    after_agent_callback=after_agent_call
    
)