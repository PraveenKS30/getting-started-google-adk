from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
import requests
from google.genai import types

def before_agent_call(callback_context: CallbackContext):

    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    state = callback_context.state.to_dict()
    user_content = callback_context.user_content

    print(f"Before Agent Call - Agent: {agent_name}, Invocation ID: {invocation_id}, State: {state}")

    if user_content and "weather" in callback_context.user_content.parts[-1].text :
        print("User is asking about weather.")
        return None
    else:
        return types.Content(
            parts=[types.Part(text=f"Agent {agent_name} skipped by before_agent_callback due to invalid query.")]
        )



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
    before_agent_callback= before_agent_call
    
)