from google.adk.agents import LlmAgent
from google.adk.tools.tool_context import ToolContext
from dotenv import load_dotenv
import requests

# load environment variables 
load_dotenv()

def get_weather(city: str, tool_context : ToolContext) -> str:
    """Fetches the weather information for a given city in Celsius.
    
    Args:
        city (str): Name of the city to get weather for
        
    Returns:
        str: Weather information with temperature in Celsius
    """
    tool_confirmation = tool_context.tool_confirmation
    if not tool_confirmation :
        tool_context.request_confirmation(
            hint=('Please approve or reject the weather request and specify the'
                ' temperature unit (celsius/fahrenheit). Respond with a'
                ' FunctionResponse containing a ToolConfirmation payload.'
            ),
            payload={'temperature_unit': 'celsius'}  # default to celsius

        )

        return {'status': 'Waiting for user confirmation for the temperature preference'}
    
    # Get confirmation details
    temp_unit = tool_confirmation.payload['temperature_unit']

    # Build URL based on temperature unit
    endpoint = "https://wttr.in"
    unit_param = '?m' if temp_unit == 'celsius' else '?u'  # m for metric (Celsius), u for US units (Fahrenheit)

    try:
        response = requests.get(f"{endpoint}/{city}{unit_param}")
        return {
            'status': 'success',
            'temperature_unit': temp_unit,
            'weather_data': response.text
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }   


root_agent = LlmAgent(
    name="first_agent",
    description="This is my first agent",
    instruction="You are a helpful assistant.",
    model="gemini-2.0-flash",
    tools = [get_weather]
    
)
