from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import httpx

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

# Gemini API設定
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

@app.get("/")
async def root():
    return {
        "message": "AI Chatbot API is running",
        "status": "ok",
        "ai_model": "Gemini 2.5 Flash" if GEMINI_API_KEY else "Not configured"
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_configured": GEMINI_API_KEY is not None
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="AI model is not configured. Please set GEMINI_API_KEY environment variable."
        )

    try:
        print(f"Received message: {request.message}")
        print(f"History length: {len(request.history)}")

        # 会話履歴を構築
        contents = []

        # 履歴を追加（最新10件まで）
        if request.history:
            for msg in request.history[-10:]:
                if msg.role == "user":
                    contents.append({
                        "role": "user",
                        "parts": [{"text": msg.content}]
                    })
                elif msg.role == "assistant":
                    contents.append({
                        "role": "model",
                        "parts": [{"text": msg.content}]
                    })

        # 新しいメッセージを追加
        contents.append({
            "role": "user",
            "parts": [{"text": request.message}]
        })

        print(f"Sending request with {len(contents)} messages")

        # Gemini APIにリクエスト送信
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                GEMINI_API_URL,
                headers={
                    "x-goog-api-key": GEMINI_API_KEY,
                    "Content-Type": "application/json"
                },
                json={
                    "contents": contents,
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 8192,
                        "topP": 0.95,
                        "topK": 40
                    },
                    "safetySettings": [
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
                    ]
                }
            )

            print(f"API response status: {response.status_code}")

            if response.status_code != 200:
                error_detail = response.text
                print(f"API error: {error_detail}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Gemini API error: {error_detail}"
                )

            result = response.json()
            print(f"Full API response: {result}")

            # レスポンスからテキストを抽出
            if "candidates" in result and len(result["candidates"]) > 0:
                candidate = result["candidates"][0]

                # finishReasonをチェック
                finish_reason = candidate.get("finishReason", "UNKNOWN")
                print(f"Finish reason: {finish_reason}")

                if finish_reason == "SAFETY":
                    print("Response blocked by safety filters")
                    raise HTTPException(
                        status_code=500,
                        detail="Response was blocked by safety filters. Please try rephrasing your question."
                    )

                if "content" in candidate and "parts" in candidate["content"]:
                    text = candidate["content"]["parts"][0]["text"]
                    print(f"Response received: {len(text)} characters")

                    if finish_reason == "MAX_TOKENS":
                        print("Warning: Response was truncated due to max tokens limit")

                    return ChatResponse(response=text)

            raise HTTPException(
                status_code=500,
                detail="Invalid response format from Gemini API"
            )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )
