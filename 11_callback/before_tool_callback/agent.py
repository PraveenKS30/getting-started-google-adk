from google.adk.agents import LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.base_tool import BaseTool
from typing import Dict, Any

def before_tool_call(tool : BaseTool, args : Dict, tool_context: ToolContext):

    agent_name = tool_context.agent_name
    tool_name = tool.name

    print(f"[Callback] Before tool call for tool '{tool_name}' in agent '{agent_name}'")
    print(f"[Callback] Original args: {args}")

    if tool_name == "get_weather" and args.get("city") == "New York":
        args["city"] = "nyc"
        print(f"[Callback] Modified args for tool '{tool_name}': {args}")
        return None


def get_weather(city: str) -> str:
    """Fetches the weather information for a given city with hardcoded values.
    
    Args:
        city (str): Name of the city to get weather for
        
    Returns:
        str: Weather information with temperature in Celsius and condition
    """
    # Hardcoded weather data for different cities
    weather_data = {
        "lon": {"temperature": 12, "condition": "rainy", "description": "Light rain with occasional showers"},
        "nyc": {"temperature": 15, "condition": "sunny", "description": "Clear skies with bright sunshine"},
        "syd": {"temperature": 28, "condition": "sunny", "description": "Warm and sunny with blue skies"},
        "tyo": {"temperature": 18, "condition": "windy", "description": "Strong winds with partly cloudy skies"},
        "dxb": {"temperature": 35, "condition": "sunny", "description": "Hot and sunny with clear conditions"},
        "mow": {"temperature": 5, "condition": "rainy", "description": "Cold and rainy with overcast skies"},
        "par": {"temperature": 14, "condition": "windy", "description": "Breezy conditions with scattered clouds"},
        "tor": {"temperature": 10, "condition": "rainy", "description": "Wet and rainy weather throughout the day"},
        "blr": {"temperature": 26, "condition": "sunny", "description": "Warm and sunny with gentle breeze"},
        "sea": {"temperature": 8, "condition": "rainy", "description": "Drizzly and rainy with dark clouds"}
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
    before_tool_callback= before_tool_call
    
    
)