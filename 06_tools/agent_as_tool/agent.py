from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from dotenv import load_dotenv


# load environment variables 
load_dotenv()

summary_agent = LlmAgent(
    name = "summary_agent",
    model = "gemini-2.0-flash",
    description = "This agent summarizes text.",
    instruction = "You are a helpful assistant that summarizes text."
)

root_agent = LlmAgent(
    name="root_agent",
    instruction="""You are helpful agent in summarizing the given text.
    Please use the given summarize tool to get the summary of the text.
    """,
    model="gemini-2.0-flash",
    tools = [AgentTool(summary_agent)]
    
)

