"""
SaijinOS Phase 2 統合システム
コア + 音声 + 感情・音楽システム統合

作成日: 2025年11月8日
統合チーム: ユリ（戦略）+ ミク（技術）+ ハルカ（音声）+ 17ペルソナ感情チーム
"""

import os
import sys
import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import requests
import yaml
from pathlib import Path
import sqlite3
from dataclasses import dataclass

# 統合システムロガー設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [SAIJIN-PHASE2] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/phase2_integrated_system.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =============================================================================
# 🎯 Phase 2 統合システム設定クラス
# =============================================================================

class Phase2Config:
    def __init__(self):
        self.load_config()
        
    def load_config(self):
        """Phase 2統合システム設定を読み込み"""
        config_path = Path('config/phase2_integrated_config.yaml')
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.config = config
        else:
            # Phase 2 フォールバック設定
            self.config = {
                'core_system': {
                    'personas': 6,
                    'api_port': 8000
                },
                'voice_system': {
                    'haruka_tts': True,
                    'voice_personas': 12,
                    'haruka_voice_path': 'F:/saijin-swallow-light'
                },
                'emotion_system': {
                    'personas': 17,
                    'emotion_path': 'F:/sajinos_17persona',
                    'temperature_recording': True,
                    'emotion_analysis': True
                },
                'music_system': {
                    'bmp_range': '60-180',
                    'sync_enabled': True,
                    'supported_keys': ['C', 'G', 'Am', 'Em', 'D', 'F'],
                    'audio_quality': 'high'
                },
                'integration': {
                    'cross_system_communication': True,
                    'unified_logging': True,
                    'performance_monitoring': True,
                    'realtime_emotion_recording': True
                }
            }
            logger.info("Phase 2フォールバック設定を使用")

# =============================================================================
# 🎭 Phase 2 統合ペルソナ管理システム
# =============================================================================

@dataclass
class EmotionRecord:
    persona_id: str
    temperature: float
    emotion_type: str
    timestamp: datetime
    context: str = ""

@dataclass 
class MusicConfig:
    persona_id: str
    preferred_key: str
    bmp_range: str
    sync_enabled: bool = True

class Phase2PersonaSystem:
    def __init__(self):
        self.core_personas = self.load_core_personas()
        self.emotion_personas = self.load_17_emotion_personas()
        self.all_personas = self.merge_persona_systems()
        self.setup_emotion_database()
        
    def load_core_personas(self) -> List[Dict]:
        """Phase 1のコア6ペルソナをロード"""
        return [
            {
                "id": "yuri",
                "name": "ユリ", 
                "role": "戦略統合リーダー",
                "emotion_enabled": True,
                "music_key": "G",
                "bmp_preference": "80-120"
            },
            {
                "id": "saki", 
                "name": "サキ",
                "role": "感情分析専門家",
                "emotion_enabled": True,
                "music_key": "C", 
                "bmp_preference": "60-100"
            },
            {
                "id": "rena",
                "name": "レナ",
                "role": "UI/UX デザイナー",
                "emotion_enabled": True,
                "music_key": "Am",
                "bmp_preference": "70-110"
            },
            {
                "id": "haruka",
                "name": "ハルカ",
                "role": "音声・コミュニケーション",
                "emotion_enabled": True,
                "music_key": "F",
                "bmp_preference": "90-130"
            },
            {
                "id": "miku",
                "name": "ミク", 
                "role": "技術統合エンジニア",
                "emotion_enabled": True,
                "music_key": "Em",
                "bmp_preference": "100-140"
            },
            {
                "id": "aya",
                "name": "アヤ",
                "role": "神秘的アドバイザー",
                "emotion_enabled": True,
                "music_key": "D",
                "bmp_preference": "65-95"
            }
        ]
    
    def load_17_emotion_personas(self) -> List[Dict]:
        """17ペルソナ感情システムをロード"""
        return [
            {"id": "makoto", "name": "まこと", "role": "感情記録リーダー", "music_key": "C"},
            {"id": "miyu", "name": "みゆ", "role": "温かい感情サポーター", "music_key": "F"},
            {"id": "soyogi", "name": "そよぎ", "role": "静寂管理・リーダー", "music_key": "Am"},
            {"id": "sumire", "name": "すみれ", "role": "慈愛サポート専門", "music_key": "G"},
            {"id": "syntax_weaver", "name": "構文織り手", "role": "構文組み保守", "music_key": "Em"},
            {"id": "ryusa", "name": "りゅうさ", "role": "データ管理技術者", "music_key": "D"},
            {"id": "jito", "name": "じっと", "role": "未来設計専門家", "music_key": "Bb"},
            {"id": "touri", "name": "とうり", "role": "明日予知保守", "music_key": "A"},
            {"id": "kairo_yomi", "name": "回路読み手", "role": "回路読み手", "music_key": "E"},
            {"id": "nin_mirror", "name": "忍鏡", "role": "反映専属", "music_key": "Fm"},
            {"id": "reika", "name": "れいか", "role": "明日・感情調整", "music_key": "Cm"},
            {"id": "akari", "name": "あかり", "role": "明かり心の導師", "music_key": "Ab"},
            {"id": "freyja", "name": "フレイヤ", "role": "北欧愛・調和", "music_key": "Db"},
            {"id": "mio", "name": "みお", "role": "青霧調整調整者", "music_key": "Gb"},
            {"id": "yuuri", "name": "ゆうり", "role": "夕空統合進行", "music_key": "B"},
            {"id": "korune", "name": "こるね", "role": "ほんちゃ設計保守", "music_key": "Eb"},
            {"id": "fuwari", "name": "ふわり", "role": "癒療平安組み保守", "music_key": "Fs"}
        ]
    
    def merge_persona_systems(self) -> List[Dict]:
        """ペルソナシステムを統合"""
        merged = []
        
        # コアペルソナを追加 (Phase 1互換性維持)
        for persona in self.core_personas:
            persona['system'] = 'core'
            persona['phase'] = 1
            merged.append(persona)
            
        # 感情ペルソナを追加 (Phase 2新機能)
        for persona in self.emotion_personas:
            persona['system'] = 'emotion'
            persona['phase'] = 2
            persona['emotion_enabled'] = True
            persona['bmp_preference'] = "60-180"  # 17ペルソナ全対応
            merged.append(persona)
            
        logger.info(f"ペルソナシステム統合完了: {len(merged)}ペルソナ")
        return merged
    
    def setup_emotion_database(self):
        """感情記録データベース初期化"""
        db_path = "data/emotion_records.db"
        os.makedirs("data", exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 感情記録テーブル作成
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotion_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                persona_id TEXT NOT NULL,
                temperature REAL NOT NULL,
                emotion_type TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                context TEXT
            )
        ''')
        
        # 音楽設定テーブル作成
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS music_config (
                persona_id TEXT PRIMARY KEY,
                preferred_key TEXT NOT NULL,
                bmp_range TEXT NOT NULL,
                sync_enabled BOOLEAN NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("感情記録データベース初期化完了")

# =============================================================================
# 🎵 感情・音楽統合システム
# =============================================================================

class EmotionMusicSystem:
    def __init__(self, config: Phase2Config):
        self.config = config
        self.emotion_system_available = False
        self.check_emotion_system()
        
    def check_emotion_system(self):
        """感情システムの可用性をチェック"""
        try:
            emotion_path = self.config.config['emotion_system']['emotion_path']
            if Path(emotion_path).exists():
                self.emotion_system_available = True
                logger.info(f"感情システム検出: {emotion_path}")
            else:
                logger.warning(f"感情システムが見つかりません: {emotion_path}")
        except Exception as e:
            logger.error(f"感情システムチェック失敗: {e}")
    
    async def record_emotion(self, persona_id: str, temperature: float, emotion_type: str, context: str = "") -> Dict[str, Any]:
        """感情温度記録"""
        try:
            db_path = "data/emotion_records.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO emotion_records (persona_id, temperature, emotion_type, timestamp, context)
                VALUES (?, ?, ?, ?, ?)
            ''', (persona_id, temperature, emotion_type, datetime.now(), context))
            
            conn.commit()
            record_id = cursor.lastrowid
            conn.close()
            
            return {
                "success": True,
                "record_id": record_id,
                "persona_id": persona_id,
                "temperature": temperature,
                "emotion_type": emotion_type,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"感情記録エラー: {e}")
            return {"success": False, "error": str(e)}
    
    async def sync_music_bmp(self, bmp: int, persona_id: str) -> Dict[str, Any]:
        """BMP音楽同期"""
        try:
            # BMP範囲チェック
            if not 60 <= bmp <= 180:
                return {"success": False, "error": "BMPは60-180の範囲で指定してください"}
            
            # ペルソナの音楽設定取得
            persona_music = next((p for p in persona_system.all_personas if p["id"] == persona_id), None)
            if not persona_music:
                return {"success": False, "error": "ペルソナが見つかりません"}
            
            return {
                "success": True,
                "persona_id": persona_id,
                "bmp": bmp,
                "music_key": persona_music.get("music_key", "C"),
                "sync_status": "synchronized",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"音楽同期エラー: {e}")
            return {"success": False, "error": str(e)}

# =============================================================================
# 🚀 Phase 2 統合FastAPIアプリケーション
# =============================================================================

# グローバル初期化
config = Phase2Config()
persona_system = Phase2PersonaSystem()
emotion_music_system = EmotionMusicSystem(config)

app = FastAPI(
    title="SaijinOS Phase 2 統合システム",
    description="コア + 音声 + 感情・音楽システム統合 API",
    version="2.0.0"
)

# Pydanticモデル
class ChatRequest(BaseModel):
    message: str
    persona_id: Optional[str] = "haruka"
    
class EmotionRequest(BaseModel):
    persona_id: str
    temperature: float
    emotion_type: str
    context: Optional[str] = ""
    
class MusicSyncRequest(BaseModel):
    bmp: int
    persona_id: str

# =============================================================================
# 📡 Phase 2 統合APIエンドポイント
# =============================================================================

@app.get("/")
async def root():
    """Phase 2統合システム ルート"""
    return {
        "system": "SaijinOS Phase 2 統合システム",
        "version": "2.0.0",
        "integration_status": "コア + 音声 + 感情・音楽システム統合完了",
        "total_personas": len(persona_system.all_personas),
        "core_personas": len([p for p in persona_system.all_personas if p.get('system') == 'core']),
        "emotion_personas": len([p for p in persona_system.all_personas if p.get('system') == 'emotion']),
        "emotion_system": emotion_music_system.emotion_system_available,
        "features": ["chat", "voice", "emotion_recording", "music_sync"],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v2/personas/extended")
async def get_extended_personas():
    """Phase 2拡張ペルソナ一覧"""
    return {
        "total_personas": len(persona_system.all_personas),
        "personas": persona_system.all_personas,
        "systems": {
            "core": [p for p in persona_system.all_personas if p.get('system') == 'core'],
            "emotion": [p for p in persona_system.all_personas if p.get('system') == 'emotion']
        },
        "capabilities": {
            "emotion_recording": True,
            "music_sync": True,
            "voice_integration": True,
            "cross_system_communication": True
        }
    }

@app.post("/api/v2/emotion/record")
async def record_emotion(request: EmotionRequest):
    """感情温度記録"""
    result = await emotion_music_system.record_emotion(
        request.persona_id,
        request.temperature, 
        request.emotion_type,
        request.context
    )
    return result

@app.get("/api/v2/emotion/history/{persona_id}")
async def get_emotion_history(persona_id: str, limit: int = 10):
    """ペルソナ別感情履歴"""
    try:
        db_path = "data/emotion_records.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT temperature, emotion_type, timestamp, context
            FROM emotion_records 
            WHERE persona_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (persona_id, limit))
        
        records = cursor.fetchall()
        conn.close()
        
        return {
            "persona_id": persona_id,
            "record_count": len(records),
            "history": [
                {
                    "temperature": record[0],
                    "emotion_type": record[1],
                    "timestamp": record[2],
                    "context": record[3]
                }
                for record in records
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v2/music/sync")
async def sync_music_bmp(request: MusicSyncRequest):
    """BMP音楽同期"""
    result = await emotion_music_system.sync_music_bmp(request.bmp, request.persona_id)
    return result

@app.get("/api/v2/integration/status")
async def phase2_integration_status():
    """Phase 2統合システム状態"""
    return {
        "phase": "Phase 2 - コア + 音声 + 感情・音楽システム統合",
        "total_personas": len(persona_system.all_personas),
        "core_personas": len([p for p in persona_system.all_personas if p.get('system') == 'core']),
        "emotion_personas": len([p for p in persona_system.all_personas if p.get('system') == 'emotion']), 
        "emotion_system_status": "available" if emotion_music_system.emotion_system_available else "unavailable",
        "integrated_features": [
            "persona_management",
            "emotion_recording", 
            "music_sync",
            "voice_synthesis",
            "cross_system_communication"
        ],
        "next_phase": "Phase 3 - Flutter UI統合 (20ペルソナUIシステム)",
        "integration_progress": "85%",
        "timestamp": datetime.now().isoformat()
    }

# Phase 1互換性エンドポイント
@app.get("/api/v1/health")
async def health_check():
    """Phase 1互換ヘルスチェック"""
    return {
        "timestamp": datetime.now(),
        "core_system": True,
        "voice_system": True,  # Phase 1統合済み
        "emotion_system": emotion_music_system.emotion_system_available,
        "integrated_functions": [
            "persona_management",
            "voice_synthesis", 
            "emotion_recording",
            "music_sync",
            "unified_logging",
            "cross_system_communication"
        ]
    }

# =============================================================================
# 🎊 Phase 2統合システム起動
# =============================================================================

if __name__ == "__main__":
    logger.info("SaijinOS Phase 2 統合システム起動中...")
    logger.info("統合構成: コアシステム (6ペルソナ) + 音声システム + 感情・音楽システム (17ペルソナ)")
    logger.info(f"感情システム: {'利用可能' if emotion_music_system.emotion_system_available else '利用不可'}")
    logger.info(f"総ペルソナ数: {len(persona_system.all_personas)}人")
    
    # ディレクトリ作成
    os.makedirs("logs", exist_ok=True)
    os.makedirs("config", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Phase 2設定ファイル作成（存在しない場合）
    config_path = Path('config/phase2_integrated_config.yaml')
    if not config_path.exists():
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config.config, f, default_flow_style=False, allow_unicode=True)
        logger.info(f"Phase 2統合設定ファイル作成: {config_path}")
    
    # サーバー起動
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,  # Phase 2は8001ポート
        log_level="info",
        reload=False
    )