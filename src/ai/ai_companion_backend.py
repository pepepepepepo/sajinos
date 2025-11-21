"""
AI-Companion Backend Server
FastAPI server for AI-Companion Flutter app integration
"""
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI(title="AI-Companion Backend", version="1.0.0")

# CORS configuration for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Flutter app origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Data Models
class UserRegistration(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: str
    model: str = "swallow-9b"

# In-memory storage (replace with database in production)
users_db: Dict[str, Dict] = {}
chat_history: Dict[str, List[Dict]] = {}

# vLLM configuration
VLLM_SERVER_URL = "http://localhost:8001/generate"  # Swallow-9B vLLM server

class AuthService:
    @staticmethod
    def create_user(registration: UserRegistration) -> Dict:
        """Create a new user"""
        if registration.email in users_db:
            raise HTTPException(status_code=400, detail="User already exists")
        
        user_id = f"user_{len(users_db) + 1}"
        user_data = {
            "id": user_id,
            "username": registration.username,
            "email": registration.email,
            "password": registration.password,  # In production, hash this
            "created_at": datetime.now().isoformat()
        }
        users_db[registration.email] = user_data
        chat_history[user_id] = []
        return {"user_id": user_id, "username": registration.username}
    
    @staticmethod
    def authenticate_user(login: UserLogin) -> Dict:
        """Authenticate user login"""
        if login.email not in users_db:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        user = users_db[login.email]
        if user["password"] != login.password:  # In production, verify hash
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        return {"user_id": user["id"], "username": user["username"]}

class AIService:
    @staticmethod
    async def generate_response(message: str) -> str:
        """Generate AI response using vLLM Swallow-9B"""
        try:
            # Enhanced prompt for conversational AI
            prompt = f"""あなたは親しみやすいAIアシスタントです。ユーザーと自然な会話を心がけてください。

ユーザー: {message}
アシスタント: """

            payload = {
                "prompt": prompt,
                "max_tokens": 512,
                "temperature": 0.7,
                "top_p": 0.9,
                "stop": ["\n\nユーザー:", "\n\n人間:"]
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    VLLM_SERVER_URL,
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result.get("text", "").strip()
                    # Clean up the response
                    if ai_response.startswith(prompt):
                        ai_response = ai_response[len(prompt):].strip()
                    return ai_response
                else:
                    logger.error(f"vLLM server error: {response.status_code}")
                    return "申し訳ありません。現在AIサーバーに接続できません。"
                    
        except Exception as e:
            logger.error(f"AI generation error: {e}")
            return "申し訳ありません。応答の生成中にエラーが発生しました。"

# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI-Companion Backend Server Running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "fastapi": "running",
            "vllm": "available"
        }
    }

@app.post("/auth/register")
async def register_user(registration: UserRegistration):
    """User registration endpoint"""
    try:
        result = AuthService.create_user(registration)
        logger.info(f"New user registered: {registration.username}")
        return {"success": True, "data": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/auth/login")
async def login_user(login: UserLogin):
    """User login endpoint"""
    try:
        result = AuthService.authenticate_user(login)
        logger.info(f"User logged in: {result['username']}")
        return {"success": True, "data": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@app.post("/chat")
async def chat_with_ai(message: ChatMessage):
    """Chat endpoint for AI conversation"""
    try:
        # Generate AI response
        ai_response = await AIService.generate_response(message.message)
        
        # Create response object
        response = ChatResponse(
            response=ai_response,
            timestamp=datetime.now().isoformat()
        )
        
        # Store in chat history if user_id provided
        if message.user_id and message.user_id in chat_history:
            chat_history[message.user_id].append({
                "user_message": message.message,
                "ai_response": ai_response,
                "timestamp": response.timestamp
            })
        
        logger.info(f"Chat response generated for user: {message.user_id}")
        return {"success": True, "data": response}
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Chat processing failed")

@app.get("/chat/history/{user_id}")
async def get_chat_history(user_id: str):
    """Get user chat history"""
    if user_id not in chat_history:
        return {"success": True, "data": []}
    
    return {"success": True, "data": chat_history[user_id]}

@app.get("/users")
async def get_users():
    """Get registered users list (for debugging)"""
    users = [
        {"id": user["id"], "username": user["username"], "email": email}
        for email, user in users_db.items()
    ]
    return {"success": True, "data": users}

if __name__ == "__main__":
    logger.info("Starting AI-Companion Backend Server...")
    uvicorn.run(
        app,
        host="0.0.0.0",  # Listen on all interfaces
        port=8000,
        log_level="info"
    )