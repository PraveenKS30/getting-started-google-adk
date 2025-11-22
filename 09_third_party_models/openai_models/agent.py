from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

root_agent = LlmAgent(
    name = "first_agent",
    description = "This is my first agent",
    instruction= "You are a helpful assistant.",
    model = LiteLlm(model= "openai/gpt-4o-mini"),
    
)