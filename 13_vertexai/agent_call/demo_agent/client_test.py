import asyncio
from vertexai import agent_engines
import vertexai

PROJECT_ID =<PROJECT_ID>
LOCATION = "us-central1"
RESOURCE_ID =<RESOURCE_ID>

AGENT_RESOURCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{RESOURCE_ID}"

vertexai.init(project=PROJECT_ID, location=LOCATION)

async def query_agent(message: str):
    remote_app = agent_engines.get(AGENT_RESOURCE_NAME)

    # Get a session
    print("Creating session...")
    remote_session = await remote_app.async_create_session(user_id="test_user_123")
    print(f"Session Created: {remote_session['id']}")

    # Send a query to the agent
    print("Querying agent...")
    final_text = ""
    async for event in remote_app.async_stream_query(
        user_id="test_user_123",
        session_id=remote_session['id'],
        message=message,
    ):
        
    # Extract text parts from the model's response
        content = event.get("content")
        if content and content.get("role") == "model":
            for part in content.get("parts", []):
                if "text" in part:
                    final_text += part["text"]
    
    print(f"\nAgent Response: {final_text}")

# Run the async function
if __name__ == "__main__":
    asyncio.run(query_agent("What's the weather in new york?"))
