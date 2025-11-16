# -*- coding: utf-8 -*-
"""
チャットAPI ルート
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    persona: str = "code"
    vibration_mode: str = "auto"
    workspace_mode: str = "chat"
    max_length: int = 256

class ChatResponse(BaseModel):
    response: str
    persona: str
    vibration_mode: str
    timestamp: str

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """チャット処理"""
    # ペルソナ別応答
    persona_responses = {
        "code": f"🔧 Code-chan♫です！「{request.message}」について技術的な観点から回答しますね！",
        "yurika": f"🎨 Yurikaです！「{request.message}」をデザイン的な視点で考えてみましょう！",
        "ana": f"📊 Anaです！「{request.message}」のデータを分析してみますね！",
        "haruka": f"🎵 Harukaです！「{request.message}」について音楽的にお答えします♪",
        "misaki": f"✅ Misakiです！「{request.message}」の品質を確認しましょう！",
        "ren": f"⚙️ Renです！「{request.message}」の運用面を考えてみます！"
    }
    
    # 振動モード別調整
    vibration_suffix = {
        "goonro": " 🌸温かくサポートします！",
        "structure": " 🔧論理的に整理しますね。", 
        "musumekko": " 💫一緒に頑張りましょう！",
        "auto": " 🔄最適な方法を見つけます。"
    }
    
    response_text = persona_responses.get(request.persona, f"{request.persona}です。")
    response_text += vibration_suffix.get(request.vibration_mode, "")
    
    return ChatResponse(
        response=response_text,
        persona=request.persona,
        vibration_mode=request.vibration_mode,
        timestamp="2025-11-16T18:30:00"
    )

@router.get("/history")
async def get_chat_history():
    """チャット履歴取得"""
    return {"history": [], "total": 0}