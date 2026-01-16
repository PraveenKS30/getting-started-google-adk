from google.adk.agents import LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
import os
from pathlib import Path

async def save_report_artifacts(tool_context: ToolContext, file_path: str, filename: str = None):
    
    # Check if file_path is a directory
    if os.path.isdir(file_path):
        # Read all PDF files from the directory
        pdf_files = list(Path(file_path).glob('*.pdf'))
        
        if not pdf_files:
            raise ValueError(f"No PDF files found in directory: {file_path}")
        
        # Process each PDF file
        for pdf_file in pdf_files:
            with open(pdf_file, 'rb') as f:
                pdf_bytes = f.read()
            
            # Save as a PDF artifact
            artifact_part = types.Part(
                inline_data=types.Blob(mime_type='application/pdf', data=pdf_bytes)
            )
            await tool_context.save_artifact(pdf_file.name, artifact_part)
    else:
        # Read the single file if directory doesn't exist
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File or directory not found: {file_path}")
        
        with open(file_path, 'rb') as f:
            pdf_bytes = f.read()

        # Save as a PDF artifact
        artifact_part = types.Part(
            inline_data=types.Blob(mime_type='application/pdf', data=pdf_bytes)
        )
        await tool_context.save_artifact(filename, artifact_part)
    


root_agent = LlmAgent(
    name = "first_agent",
    description = "This is my first agent",
    instruction= """
        You are an assistant that manages artifacts.
        If the user asks to save a document, 
        call 'save_report_artifacts' to save the files as an artifacts.
        You don't need to ask for the filename from the user and please keep the 
        filename as the original file while saving.
        """ ,
    model = "gemini-2.0-flash",
    tools = [save_report_artifacts]
    
)
