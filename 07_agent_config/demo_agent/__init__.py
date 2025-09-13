import requests

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
