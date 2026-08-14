from fastapi import FastAPI
from pydantic import BaseModel
from app.planner import run_agent
from app.system_status import router as system_status_router

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.include_router(system_status_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {
        "message": "HAMZA TEST 123"
    }
@app.post("/chat")
def chat(data: ChatRequest):
    reply = run_agent(data.message)

    return {
        "reply": reply
    }
    
