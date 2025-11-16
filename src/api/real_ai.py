from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from real_ai_integration import real_ai

router = APIRouter()

class RealChatRequest(BaseModel):
    message: str
    personas: List[str]
    auto_implement: bool = False

class RealChatResponse(BaseModel):
    responses: List[dict]
    team_mode: bool
    implementation_ready: bool = False

@router.post("/real-chat", response_model=RealChatResponse)
async def real_ai_chat(request: RealChatRequest):
    """実際のAIペルソナとのチャット"""
    try:
        # 接続チェック
        if not await real_ai.test_connection():
            raise HTTPException(status_code=503, detail="AI service unavailable")
        
        if len(request.personas) == 1:
            # 単一ペルソナモード
            result = await real_ai.chat_with_persona(request.personas[0], request.message)
            return RealChatResponse(
                responses=[result],
                team_mode=False,
                implementation_ready=request.auto_implement and "コード" in request.message
            )
        else:
            # マルチペルソナモード
            results = await real_ai.multi_persona_chat(request.personas, request.message)
            return RealChatResponse(
                responses=results,
                team_mode=True,
                implementation_ready=request.auto_implement
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ai-status")
async def get_ai_status():
    """AI統合システムの状態"""
    connected = await real_ai.test_connection()
    info = real_ai.get_model_info()
    
    return {
        "connected": connected,
        "personas_available": len(info["available_personas"]),
        "models_count": info["total_models"],
        "persona_mapping": info["persona_mapping"]
    }