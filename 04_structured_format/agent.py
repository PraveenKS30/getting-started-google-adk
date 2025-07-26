from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field

class Country(BaseModel):
    country : str = Field(description="The name of the country for which the capital is requested.")


# This function would give the capital city of a country along with some examples
def get_capital(country: str) :
    """
    Returns the capital city of the given country.
    
    Args:
        country (str): The name of the country.
        
    Returns:
        Capital: A model containing the capital city.
    """
    # This is a placeholder implementation. In a real scenario, you would query a database or an API.
    capitals = {
        "France": "Paris",
        "Germany": "Berlin",
        "Italy": "Rome",
        "Spain": "Madrid",
        "United Kingdom": "London"
    }
    
    capital_city = capitals.get(country, "Unknown")
    return capital_city


# initialize the agent 
root_agent = LlmAgent(
    name = "capital_agent",
    instruction= """
        You are a helpful agent that provides the capital city of a country using a tool.
        The user will provide the country name in a JSON format like {"country": "country_name"}."
        1. Extract the country name.
        2. Use the `get_capital` tool to find the capital..
    """,
    model = "gemini-2.0-flash",
    input_schema=Country,
    tools =[get_capital]

    
) 

