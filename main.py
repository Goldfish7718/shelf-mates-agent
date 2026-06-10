import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from agent import run_agent

app = FastAPI(
    title="Shelf-mates AI API",
    description="API for the Shelf-mates AI e-commerce grocery assistant agent",
    version="1.0.0"
)

# Enable CORS so other apps can consume this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production as required
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, Any]]] = None

class ChatResponse(BaseModel):
    response: str
    history: List[Dict[str, Any]]

@app.get("/")
def read_root():
    return {
        "name": "Shelf-mates AI API",
        "status": "healthy",
        "description": "Send POST requests to /chat to interact with the grocery assistant agent."
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = run_agent(message=request.message, history=request.history)
        return ChatResponse(
            response=result["response"],
            history=result["history"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Allow running the file directly with `python main.py`
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)