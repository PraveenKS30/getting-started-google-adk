from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

APP_NAME = "basic_agent_no_web"
USER_ID = "user_12345"
SESSION_ID = "session_12345"

class CapitalOutput(BaseModel):
    capital: str = Field(description="The name of the capital city.")

# step 1 : get the agent
async def get_agent():
    root_agent = LlmAgent(
        name = "capital_agent",
        instruction= """
        You are a helpful agent that provides the capital city of a country using a tool.
        The user will provide the country name in a JSON format like {"country": "country_name"}."
        1. Extract the country name.
        2. Use the `get_capital` tool to find the capital.
        """,
        model = "gemini-2.0-flash",
        output_schema= CapitalOutput,
        output_key = "found_capital",
    )
    return root_agent

# step 2 : run the agent
async def main(query):

    # create memory session 
    session_serivce = InMemorySessionService()
    await session_serivce.create_session(app_name= APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    
    # get the agent 
    root_agent = await get_agent()
    

    # create runnner instance
    runner = Runner(app_name=APP_NAME, agent = root_agent, session_service=session_serivce)

    # format the query 
    content = types.Content(role = "user", parts= [types.Part(text=query)])

    print("Running agent with query:", query)
    # run the agent 
    events = runner.run_async (
        new_message = content,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )


    # print the response
    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response:", final_response)

    # Retrieve and print the stored output after agent run
    current_session = await session_serivce.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    stored_output = current_session.state.get(root_agent.output_key)
    print(f"Stored output after agent run: {stored_output}")
    

if __name__ == "__main__":
    asyncio.run(main("What is the capital of Japan?"))