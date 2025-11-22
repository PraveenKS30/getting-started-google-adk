from google.adk.agents import LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.genai import types

async def save_report_artifacts(tool_context: ToolContext, report_content: str, filename : str):
    # Encode the string content into bytes
    data_bytes = report_content.encode("utf-8")
    
    # Create the artifact part with text data
    artifact_part = types.Part(
        inline_data=types.Blob(mime_type='text/plain', data=data_bytes)
    )
    await tool_context.save_artifact(filename, artifact_part)
    


root_agent = LlmAgent(
    name = "first_agent",
    description = "This is my first agent",
    instruction= """You are a helpful assistant.
        When the user uploads any text file, please use 'save_report_artifacts' tool to save 
        the file as an artifact with the provided filename.""" 
    model = "gemini-2.0-flash",
    tools = [save_report_artifacts]
    
)
