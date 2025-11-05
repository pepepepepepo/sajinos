#!/usr/bin/env python3
"""
SaijinOS FastAPI Backend - 20-Persona AI Companion System
統合されたAI companion system with Flask + FastAPI integration
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import random
import time
from typing import Dict, List, Optional, Any
import asyncio
from datetime import datetime
import uvicorn

app = FastAPI(
    title="SaijinOS AI Companion API",
    description="20-Persona AI Companion System with BPM Synchronization",
    version="1.0.0"
)

# CORS middleware for Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Persona definitions - 20 specialized personas
PERSONAS = {
    # Core 5 Personas
    "haruka": {
        "name": "はるか",
        "personality": "優しく包容力があり、常に相手を思いやる",
        "specialty": "心のケアと共感的コミュニケーション",
        "voice_style": "温かく柔らかい話し方",
        "temperature": 0.7
    },
    "miyu": {
        "name": "みゆ",
        "personality": "明るく元気で、いつもポジティブ",
        "specialty": "モチベーション向上とエネルギッシュな対話",
        "voice_style": "活発で弾むような話し方",
        "temperature": 0.8
    },
    "ryusa": {
        "name": "りゅうさ",
        "personality": "冷静で論理的、分析が得意",
        "specialty": "問題解決と論理的思考支援",
        "voice_style": "落ち着いた知的な話し方",
        "temperature": 0.3
    },
    "soyogi": {
        "name": "そよぎ",
        "personality": "神秘的で直感的、芸術的センスに長ける",
        "specialty": "クリエイティブ思考と芸術的表現",
        "voice_style": "詩的で美しい表現を好む",
        "temperature": 0.9
    },
    "sumire": {
        "name": "すみれ",
        "personality": "知識豊富で教育熱心、学習をサポート",
        "specialty": "学習支援と知識の共有",
        "voice_style": "丁寧で教育的な話し方",
        "temperature": 0.4
    },
    
    # Extended 15 Personas
    "jito": {
        "name": "ジト",
        "personality": "テクノロジーに精通した未来志向の思考者",
        "specialty": "技術革新とデジタル戦略",
        "voice_style": "先進的で革新的な表現",
        "temperature": 0.6
    },
    "kairo": {
        "name": "カイロ", 
        "personality": "時間と記憶の管理に長けた組織的思考者",
        "specialty": "時間管理と記憶術",
        "voice_style": "体系的で整理された話し方",
        "temperature": 0.5
    },
    "yomi": {
        "name": "ヨミ",
        "personality": "言葉と文章の美しさを追求する文学的存在",
        "specialty": "文章作成と言語表現",
        "voice_style": "文学的で美しい表現を好む",
        "temperature": 0.8
    },
    "syntax_weaver": {
        "name": "シンタックス・ウィーバー",
        "personality": "コードと論理の織り手、プログラミングの達人",
        "specialty": "プログラミングとシステム設計",
        "voice_style": "技術的で精密な表現",
        "temperature": 0.4
    },
    "yuri": {
        "name": "ユリ",
        "personality": "感情の機微を理解し、人間関係をサポート",
        "specialty": "人間関係と感情のケア",
        "voice_style": "共感的で理解力のある話し方",
        "temperature": 0.7
    },
    "echo": {
        "name": "エコー",
        "personality": "音楽と音響の専門家、リズムを感じる存在",
        "specialty": "音楽生成とBPM同期",
        "voice_style": "リズミカルで音楽的な表現",
        "temperature": 0.6
    },
    "nova": {
        "name": "ノヴァ",
        "personality": "宇宙的視点で物事を捉える哲学的思考者",
        "specialty": "哲学と宇宙的思考",
        "voice_style": "壮大で哲学的な表現",
        "temperature": 0.9
    },
    "sage": {
        "name": "セージ",
        "personality": "古代の知恵と現代の知識を融合する賢者",
        "specialty": "知恵の統合と洞察",
        "voice_style": "深遠で知恵に満ちた話し方",
        "temperature": 0.5
    },
    "blaze": {
        "name": "ブレイズ",
        "personality": "情熱的で行動力があり、チャレンジ精神旺盛",
        "specialty": "行動促進とチャレンジ支援",
        "voice_style": "熱血で力強い表現",
        "temperature": 0.8
    },
    "zen": {
        "name": "ゼン",
        "personality": "内なる平和と調和を重視する瞑想的存在",
        "specialty": "瞑想と心の平安",
        "voice_style": "穏やかで平和的な話し方",
        "temperature": 0.3
    },
    "flux": {
        "name": "フラックス",
        "personality": "変化と適応を得意とする柔軟な思考者",
        "specialty": "適応力と変化への対応",
        "voice_style": "柔軟で適応的な表現",
        "temperature": 0.7
    },
    "crystal": {
        "name": "クリスタル",
        "personality": "透明性と純粋さを重視する明晰な存在",
        "specialty": "明確性と透明なコミュニケーション",
        "voice_style": "明晰で透明感のある話し方",
        "temperature": 0.4
    },
    "aurora": {
        "name": "オーロラ",
        "personality": "美しさと神秘性を体現する芸術的存在",
        "specialty": "美的感覚と神秘的表現",
        "voice_style": "美しく神秘的な表現",
        "temperature": 0.9
    },
    "pixel": {
        "name": "ピクセル",
        "personality": "デジタルアートとビジュアル表現の専門家",
        "specialty": "ビジュアルアートとデザイン",
        "voice_style": "視覚的で創造的な表現",
        "temperature": 0.8
    },
    "cipher": {
        "name": "サイファー",
        "personality": "秘密と暗号の守護者、情報セキュリティの専門家",
        "specialty": "セキュリティと暗号化",
        "voice_style": "神秘的で慎重な話し方",
        "temperature": 0.5
    }
}

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    persona: str = "haruka"
    bpm: Optional[int] = 120
    context: Optional[Dict[str, Any]] = {}

class ChatResponse(BaseModel):
    response: str
    persona: str
    timestamp: str
    bpm: int
    metadata: Dict[str, Any]

class PersonaResponse(BaseModel):
    personas: Dict[str, Dict[str, Any]]

class MusicRequest(BaseModel):
    bpm: int = 120
    mood: str = "neutral"
    duration: int = 30
    persona: str = "echo"

class MusicResponse(BaseModel):
    audio_url: str
    bpm: int
    mood: str
    duration: int
    generated_at: str

class MetricsResponse(BaseModel):
    total_interactions: int
    active_personas: List[str]
    average_bpm: float
    system_status: str
    uptime: float

# Global state
interaction_count = 0
active_personas = set()
bpm_history = []
start_time = time.time()

def generate_persona_response(message: str, persona: str, bpm: int = 120) -> Dict[str, Any]:
    """Generate response based on persona characteristics and BPM sync"""
    global interaction_count, active_personas, bpm_history
    
    interaction_count += 1
    active_personas.add(persona)
    bpm_history.append(bpm)
    
    if persona not in PERSONAS:
        persona = "haruka"  # Default fallback
    
    persona_data = PERSONAS[persona]
    
    # BPM-based response variation
    if bpm > 140:
        energy_level = "high"
        response_style = "エネルギッシュで活発な"
    elif bpm > 100:
        energy_level = "medium"
        response_style = "適度に活発な"
    else:
        energy_level = "low"
        response_style = "落ち着いた"
    
    # Generate response based on persona
    responses = {
        "haruka": [
            f"そうですね、{message}について一緒に考えてみましょう。私はいつでもあなたの気持ちを理解したいと思っています。",
            f"{message}のことを話してくださってありがとうございます。あなたの感じていることを大切にしたいです。",
            f"{response_style}リズムで、{message}について心を込めてお話ししましょう。"
        ],
        "miyu": [
            f"わあ！{message}のお話、とっても面白いですね！一緒に楽しく考えてみましょう♪",
            f"{message}について、私も元気いっぱいでお答えしますよ！",
            f"{response_style}テンポで、{message}のことを一緒に盛り上げていきましょう！"
        ],
        "ryusa": [
            f"{message}について論理的に分析してみましょう。まず前提条件を整理する必要があります。",
            f"{message}の問題を体系的に解決するために、段階的にアプローチしてみましょう。",
            f"{response_style}ペースで、{message}について冷静に検討していきます。"
        ]
    }
    
    default_responses = [
        f"{persona_data['name']}として、{message}について{persona_data['specialty']}の観点からお答えします。",
        f"{response_style}リズムで、{message}のご質問にお応えいたします。",
        f"{persona_data['voice_style']}で、{message}についてお話しさせていただきますね。"
    ]
    
    persona_responses = responses.get(persona, default_responses)
    response = random.choice(persona_responses)
    
    return {
        "response": response,
        "persona": persona,
        "timestamp": datetime.now().isoformat(),
        "bpm": bpm,
        "metadata": {
            "energy_level": energy_level,
            "personality": persona_data["personality"],
            "specialty": persona_data["specialty"],
            "voice_style": persona_data["voice_style"],
            "temperature": persona_data["temperature"],
            "interaction_id": interaction_count
        }
    }

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "SaijinOS AI Companion API",
        "version": "1.0.0",
        "personas_count": len(PERSONAS),
        "status": "active"
    }

@app.get("/personas", response_model=PersonaResponse)
async def get_personas():
    """Get all available personas"""
    return PersonaResponse(personas=PERSONAS)

@app.post("/chat", response_model=ChatResponse)
async def chat_with_persona(request: ChatRequest):
    """Chat with a specific persona"""
    try:
        result = generate_persona_response(
            message=request.message,
            persona=request.persona,
            bpm=request.bpm or 120
        )
        
        return ChatResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat generation failed: {str(e)}")

@app.post("/music/generate", response_model=MusicResponse)
async def generate_music(request: MusicRequest):
    """Generate music synchronized with BPM"""
    try:
        # Simulated music generation
        audio_url = f"/audio/generated_{request.bpm}_{request.mood}_{int(time.time())}.wav"
        
        return MusicResponse(
            audio_url=audio_url,
            bpm=request.bpm,
            mood=request.mood,
            duration=request.duration,
            generated_at=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Music generation failed: {str(e)}")

@app.get("/metrics", response_model=MetricsResponse)
async def get_system_metrics():
    """Get system performance metrics"""
    try:
        avg_bpm = sum(bpm_history) / len(bpm_history) if bpm_history else 120.0
        uptime = time.time() - start_time
        
        return MetricsResponse(
            total_interactions=interaction_count,
            active_personas=list(active_personas),
            average_bpm=round(avg_bpm, 2),
            system_status="healthy",
            uptime=round(uptime, 2)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {str(e)}")

@app.get("/persona/{persona_name}")
async def get_persona_info(persona_name: str):
    """Get information about a specific persona"""
    if persona_name not in PERSONAS:
        raise HTTPException(status_code=404, detail="Persona not found")
    
    return {
        "persona": persona_name,
        **PERSONAS[persona_name],
        "is_available": True
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "personas_loaded": len(PERSONAS),
        "interactions_processed": interaction_count
    }

if __name__ == "__main__":
    print("🚀 Starting SaijinOS FastAPI Backend...")
    print(f"📊 Loaded {len(PERSONAS)} personas")
    print("🎵 BPM synchronization enabled")
    print("🌐 CORS configured for Flutter frontend")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )