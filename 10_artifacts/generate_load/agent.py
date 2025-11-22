from google.adk import Agent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools import load_artifacts
from google.genai import types


async def save_report_artifacts(tool_context: ToolContext, report_content : str):
   # Encode the string content into bytes
    data_bytes = report_content.encode("utf-8")
    
    # Create the artifact part with text data
    artifact_part = types.Part(
        inline_data=types.Blob(mime_type='text/plain', data= data_bytes)
    )
    await tool_context.save_artifact("reports.txt", artifact_part)
    



root_agent = Agent(
    name='artifact_agent',  # Added required name parameter
    model='gemini-2.0-flash',
    instruction="""
        You are a helpful assistant.
        1.  When the user asks you to create any report or document, you MUST then call the 
            'save_report_artifacts' tool immediately with the full content to save it as an artifact.
        2.  In case of any questions about previously saved artifacts, you can use the 'load_artifacts' 
            tool to retrieve them.
    """,
    tools=[save_report_artifacts, load_artifacts]
    )