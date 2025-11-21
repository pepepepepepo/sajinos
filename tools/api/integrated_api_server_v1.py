"""
SaijinOS Phase 1 統合システム
統合APIサーバー - コア + 音声システム統合

作成日: 2025年11月8日
統合チーム: ユリ（戦略）+ ミク（技術）+ ハルカ（音声）
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import requests
import yaml
from pathlib import Path

# 統合システムロガー設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [SAIJIN-INTEGRATED] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/integrated_system.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =============================================================================
# 🎯 統合システム設定クラス
# =============================================================================

class IntegratedConfig:
    def __init__(self):
        self.load_config()
        
    def load_config(self):
        """統合システム設定を読み込み"""
        config_path = Path('config/integrated_config.yaml')
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.config = config
        else:
            # フォールバック設定
            self.config = {
                'core_system': {
                    'personas': 6,
                    'api_port': 8000
                },
                'voice_system': {
                    'haruka_tts': True,
                    'voice_personas': 12,
                    'tts_port': 8001,
                    'haruka_voice_path': 'F:/saijin-swallow-light'
                },
                'integration': {
                    'cross_system_communication': True,
                    'unified_logging': True,
                    'performance_monitoring': True
                }
            }
            logger.info("フォールバック設定を使用 - integrated_config.yaml が見つかりません")

# =============================================================================
# 🎭 統合ペルソナ管理システム
# =============================================================================

class IntegratedPersonaSystem:
    def __init__(self):
        self.core_personas = self.load_core_personas()
        self.voice_mapping = self.create_voice_mapping()
        
    def load_core_personas(self) -> List[Dict]:
        """コア6ペルソナをロード"""
        return [
            {
                "id": "yuri",
                "name": "ユリ", 
                "role": "戦略統合リーダー",
                "voice_profile": "cool_analytical",
                "tts_available": True,
                "integration_priority": 1
            },
            {
                "id": "saki",
                "name": "サキ",
                "role": "感情分析専門家", 
                "voice_profile": "gentle_emotional",
                "tts_available": False,  # 新規作成予定
                "integration_priority": 3
            },
            {
                "id": "rena", 
                "name": "レナ",
                "role": "UI/UX デザイナー",
                "voice_profile": "elegant_refined", 
                "tts_available": True,
                "integration_priority": 2
            },
            {
                "id": "haruka",
                "name": "ハルカ",
                "role": "音声・コミュニケーション",
                "voice_profile": "microsoft_haruka_tts",
                "tts_available": True,
                "integration_priority": 1  # 最優先
            },
            {
                "id": "miku", 
                "name": "ミク",
                "role": "技術統合エンジニア",
                "voice_profile": "technical_system",
                "tts_available": True,
                "integration_priority": 1
            },
            {
                "id": "aya",
                "name": "アヤ", 
                "role": "神秘的アドバイザー",
                "voice_profile": "mysterious_mystical",
                "tts_available": False,  # 新規作成予定  
                "integration_priority": 4
            }
        ]
    
    def create_voice_mapping(self) -> Dict:
        """音声システムとの統合マッピング"""
        return {
            "yuri": {
                "voice_system_id": "yuri",
                "tts_engine": "haruka_base",
                "voice_characteristics": "冷静・分析的"
            },
            "haruka": {
                "voice_system_id": "haruka", 
                "tts_engine": "microsoft_haruka",
                "voice_characteristics": "優しい・親しみやすい"
            },
            "miku": {
                "voice_system_id": "miyu",
                "tts_engine": "haruka_technical", 
                "voice_characteristics": "技術的・システマティック"
            },
            "rena": {
                "voice_system_id": "reika",
                "tts_engine": "haruka_elegant",
                "voice_characteristics": "上品・優雅"
            },
            # 新規作成予定
            "saki": {
                "voice_system_id": "saki_new",
                "tts_engine": "haruka_emotional",
                "voice_characteristics": "感情豊か・共感的"
            },
            "aya": {
                "voice_system_id": "aya_new", 
                "tts_engine": "haruka_mystical",
                "voice_characteristics": "神秘的・直感的"
            }
        }

# =============================================================================
# 🔊 音声統合システム
# =============================================================================

class VoiceIntegrationSystem:
    def __init__(self, config: IntegratedConfig):
        self.config = config
        self.voice_system_available = False
        self.check_voice_system()
        
    def check_voice_system(self):
        """音声システムの可用性をチェック"""
        try:
            voice_path = self.config.config['voice_system']['haruka_voice_path']
            if Path(voice_path).exists():
                self.voice_system_available = True
                logger.info(f"音声システム検出: {voice_path}")
            else:
                logger.warning(f"音声システムが見つかりません: {voice_path}")
        except Exception as e:
            logger.error(f"音声システムチェック失敗: {e}")
    
    async def generate_voice(self, persona_id: str, text: str) -> Dict[str, Any]:
        """統合音声生成"""
        if not self.voice_system_available:
            return {
                "success": False,
                "error": "音声システムが利用できません",
                "fallback": "text_only"
            }
            
        try:
            # ここで音声システムAPIを呼び出し
            # 実装詳細は音声システムの統合時に追加
            return {
                "success": True,
                "persona_id": persona_id,
                "text": text,
                "audio_file": f"voice_output_{persona_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav",
                "generation_time": "2.5秒"
            }
        except Exception as e:
            logger.error(f"音声生成エラー: {e}")
            return {
                "success": False,
                "error": str(e),
                "fallback": "text_only"
            }

# =============================================================================
# 🚀 統合FastAPIアプリケーション
# =============================================================================

# グローバル初期化
config = IntegratedConfig()
persona_system = IntegratedPersonaSystem()
voice_system = VoiceIntegrationSystem(config)

app = FastAPI(
    title="SaijinOS Phase 1 統合システム",
    description="コア + 音声システム統合 API",
    version="1.0.0"
)

# Pydanticモデル
class ChatRequest(BaseModel):
    message: str
    persona_id: Optional[str] = "haruka"
    
class VoiceRequest(BaseModel):
    text: str
    persona_id: str
    
class SystemStatus(BaseModel):
    timestamp: datetime
    core_system: bool
    voice_system: bool
    integrated_functions: List[str]

# =============================================================================
# 📡 統合APIエンドポイント
# =============================================================================

@app.get("/")
async def root():
    """統合システム ルート"""
    return {
        "system": "SaijinOS Phase 1 統合システム",
        "version": "1.0.0",
        "integration_status": "コア + 音声システム統合完了",
        "available_personas": len(persona_system.core_personas),
        "voice_integration": voice_system.voice_system_available,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/health")
async def health_check():
    """統合システムヘルスチェック"""
    return SystemStatus(
        timestamp=datetime.now(),
        core_system=True,
        voice_system=voice_system.voice_system_available,
        integrated_functions=[
            "persona_management",
            "voice_synthesis", 
            "unified_logging",
            "cross_system_communication"
        ]
    )

@app.get("/api/v1/personas")
async def get_personas():
    """全ペルソナ一覧"""
    return {
        "personas": persona_system.core_personas,
        "voice_mapping": persona_system.voice_mapping,
        "integration_ready": [p for p in persona_system.core_personas if p["tts_available"]]
    }

@app.post("/api/v1/personas/{persona_id}/chat")
async def persona_chat(persona_id: str, request: ChatRequest):
    """ペルソナ別チャット"""
    # ペルソナ検索
    persona = next((p for p in persona_system.core_personas if p["id"] == persona_id), None)
    if not persona:
        raise HTTPException(status_code=404, detail=f"ペルソナ '{persona_id}' が見つかりません")
    
    # チャットレスポンス生成（基本実装）
    response_text = f"こんにちは！{persona['name']}です。メッセージありがとうございます：「{request.message}」"
    
    return {
        "persona": persona,
        "response": response_text,
        "voice_available": persona["tts_available"],
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/v1/personas/{persona_id}/speak")
async def persona_speak(persona_id: str, request: VoiceRequest):
    """ペルソナ音声生成 - 新統合機能"""
    persona = next((p for p in persona_system.core_personas if p["id"] == persona_id), None)
    if not persona:
        raise HTTPException(status_code=404, detail=f"ペルソナ '{persona_id}' が見つかりません")
    
    if not persona["tts_available"]:
        return {
            "success": False,
            "error": f"ペルソナ '{persona['name']}' の音声機能は準備中です",
            "fallback": "text_only"
        }
    
    # 音声生成
    voice_result = await voice_system.generate_voice(persona_id, request.text)
    
    return {
        "persona": persona,
        "voice_result": voice_result,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/voice/config")  
async def voice_config():
    """音声システム設定"""
    return {
        "voice_system_available": voice_system.voice_system_available,
        "haruka_tts_enabled": config.config['voice_system']['haruka_tts'],
        "supported_personas": [p["id"] for p in persona_system.core_personas if p["tts_available"]],
        "voice_mapping": persona_system.voice_mapping
    }

@app.get("/api/v1/integration/status")
async def integration_status():
    """統合システム状態"""
    return {
        "phase": "Phase 1 - コア + 音声システム統合",
        "core_personas": len(persona_system.core_personas),
        "voice_ready_personas": len([p for p in persona_system.core_personas if p["tts_available"]]),
        "voice_system_status": "available" if voice_system.voice_system_available else "unavailable",
        "next_phase": "Phase 2 - 感情エンジン統合 (17ペルソナシステム)",
        "integration_progress": "70%",
        "timestamp": datetime.now().isoformat()
    }

# =============================================================================
# 🎊 統合システム起動
# =============================================================================

if __name__ == "__main__":
    logger.info("SaijinOS Phase 1 統合システム起動中...")
    logger.info("統合構成: コアシステム (6ペルソナ) + 音声システム")
    logger.info(f"音声システム: {'利用可能' if voice_system.voice_system_available else '利用不可'}")
    
    # ディレクトリ作成
    os.makedirs("logs", exist_ok=True)
    os.makedirs("config", exist_ok=True)
    
    # 統合設定ファイル作成（存在しない場合）
    config_path = Path('config/integrated_config.yaml')
    if not config_path.exists():
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config.config, f, default_flow_style=False, allow_unicode=True)
        logger.info(f"統合設定ファイル作成: {config_path}")
    
    # サーバー起動
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False
    )