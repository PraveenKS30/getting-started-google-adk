from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import vertexai
from vertexai import agent_engines


# Configuration
PROJECT_ID = <PROJECT_ID>
LOCATION = "us-central1"
RESOURCE_ID = <RESOURCE_ID>
AGENT_RESOURCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{RESOURCE_ID}"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Initialize FastAPI app
app = FastAPI(
    title="Vertex AI Agent API",
    description="REST API for interacting with Vertex AI agents",
    version="1.0.0"
)


# Store sessions in memory (for production, use a database)
sessions = {}


# Request/Response Models
class CreateSessionRequest(BaseModel):
    user_id: str


class CreateSessionResponse(BaseModel):
    session_id: str
    user_id: str


class QueryRequest(BaseModel):
    user_id: str
    session_id: str
    message: str


class QueryResponse(BaseModel):
    content: str
    session_id: str
    user_id: str


# Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/sessions", response_model=CreateSessionResponse)
async def create_session(request: CreateSessionRequest):
    """Create a new session for the user"""
    try:
        remote_app = agent_engines.get(AGENT_RESOURCE_NAME)
        remote_session = await remote_app.async_create_session(user_id=request.user_id)
        
        # Store session locally
        sessions[remote_session['id']] = {
            "user_id": request.user_id,
            "session_id": remote_session['id']
        }
        
        return CreateSessionResponse(
            session_id=remote_session['id'],
            user_id=request.user_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """Send a query to the agent and get a response"""
    try:
        # Verify session exists
        if request.session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")
        
        remote_app = agent_engines.get(AGENT_RESOURCE_NAME)
        
        # Stream and collect the response
        final_text = ""
        async for event in remote_app.async_stream_query(
            user_id=request.user_id,
            session_id=request.session_id,
            message=request.message,
        ):
            content = event.get("content")
            if content and content.get("role") == "model":
                for part in content.get("parts", []):
                    if "text" in part:
                        final_text += part["text"]
        
        return QueryResponse(
            content=final_text,
            session_id=request.session_id,
            user_id=request.user_id
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
