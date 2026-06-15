from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.llm.chatbot import chat

app = FastAPI(title="Medical Care Centre API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "Medical Care Centre Backend Running"}

@app.post("/chat")
def chatbot_response(request: ChatRequest):
    try:
        response = chat(request.message)
        return {"response": response}
    except Exception as e:
        return {"response": f"Backend error: {str(e)}"}