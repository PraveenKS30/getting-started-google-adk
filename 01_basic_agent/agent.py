from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name = "first_agent",
    description = "This is my first agent",
    instruction= "Youa are a helpful assistant.",
    model = "gemini-2.0-flash",
)