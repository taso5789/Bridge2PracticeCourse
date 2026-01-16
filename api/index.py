from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# FastAPIアプリケーションの初期化
app = FastAPI(title="AI Chatbot API")

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエストモデル
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []
    language: Optional[str] = "en"

# レスポンスモデル
class ChatResponse(BaseModel):
    response: str

# Gemini AIの初期化
try:
    import google.generativeai as genai

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set")

    genai.configure(api_key=api_key)
    # Use gemini-pro for stable performance
    model = genai.GenerativeModel('gemini-pro')

    print("✅ Gemini AI initialized successfully")
except Exception as e:
    print(f"❌ Error initializing Gemini AI: {e}")
    model = None

@app.get("/")
async def root():
    return {
        "message": "AI Chatbot API is running",
        "status": "ok",
        "ai_model": "Gemini Pro" if model else "Not configured"
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_configured": model is not None
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not model:
        raise HTTPException(
            status_code=500,
            detail="AI model is not configured. Please set GEMINI_API_KEY environment variable."
        )

    try:
        print(f"Received message: {request.message}")
        print(f"History length: {len(request.history)}")

        # 会話履歴を構築（Gemini API形式に変換）
        history = []
        if request.history:
            for msg in request.history[-10:]:  # 最新10件まで
                if msg.role == "user":
                    history.append({"role": "user", "parts": [msg.content]})
                elif msg.role == "assistant":
                    history.append({"role": "model", "parts": [msg.content]})

        print(f"Formatted history: {len(history)} messages")

        # チャットセッションを開始
        chat_session = model.start_chat(history=history)
        print("Chat session started")

        # 新しいメッセージを送信
        response = chat_session.send_message(request.message)
        print(f"Response received: {len(response.text)} characters")

        return ChatResponse(response=response.text)

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )
