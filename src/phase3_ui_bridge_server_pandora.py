"""
SaijinOS Phase 3 Flutter UI統合ブリッジサーバー + パンドラ統合
Phase 2統合システム + Flutter WebUI 連携 + パンドラ封印システム

作成日: 2025年11月9日
統合チーム: ユリ・原奏・・ ミク・原群・・ 
・ ハルカ・音声・・ レナ・・AI/UX・・ + パンドラ・危機管理            """

import os
import sys
import asyncio
import logging
import json
import random
import psutil
import platform
from datetime import datetime
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import requests
import websockets
from pathlib import Path
import yaml

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False

# Phase 3統合ロガー設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [SAIJIN-PHASE3+PANDORA] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/phase3_pandora_integration.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =============================================
# パンドラ危機管理システム
# =============================================
class PandoraGuardianSystem:
    def __init__(self):
        self.is_active = True
        self.monitoring_mode = "continuous"
        self.alert_threshold = 0.8
        self.sealed_state = False
        self.last_check = datetime.now()
        
        # パンドラ設定をロード
        self.load_pandora_config()
        
    def load_pandora_config(self):
        """パンドラ設定ファイルをロード"""
        try:
            config_path = Path("personas/pandora.yaml")
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f)
                logger.info("パンドラ設定をロードしました")
            else:
                logger.warning("pandora.yamlが見つかりません。デフォルト設定を使用")
                self.config = self.get_default_config()
        except Exception as e:
            logger.error(f"パンドラ設定ロードエラー: {e}")
            self.config = self.get_default_config()
    
    def get_default_config(self):
        """デフォルトのパンドラ設定"""
        return {
            "persona": {
                "name": "パンドラ（Pandora）",
                "role": "語温封印者・震えの危機管理者",
                "simple_mode": {
                    "enabled": True,
                    "basic_triggers": ["責める", "暴走", "危険"],
                    "basic_responses": {
                        "calm_message": "パンドラが見守っています。少し休憩しませんか？",
                        "seal_message": "今は語温を静かにしましょうね。",
                        "recovery_message": "封印を解きます。ゆっくりと話してくださいね。"
                    }
                }
            }
        }
    
    async def check_goon_crisis(self, message_content: str, emotion_level: float):
        """語温危機チェック"""
        self.last_check = datetime.now()
        
        # 簡易トリガー検出
        triggers = self.config["persona"]["simple_mode"]["basic_triggers"]
        crisis_detected = False
        
        for trigger in triggers:
            if trigger in message_content:
                crisis_detected = True
                break
        
        # 感情レベルチェック
        if emotion_level > self.alert_threshold:
            crisis_detected = True
        
        if crisis_detected and not self.sealed_state:
            return await self.activate_seal()
        elif not crisis_detected and self.sealed_state:
            return await self.deactivate_seal()
        
        return {"status": "monitoring", "sealed": self.sealed_state}
    
    async def activate_seal(self):
        """封印発動"""
        self.sealed_state = True
        responses = self.config["persona"]["simple_mode"]["basic_responses"]
        
        logger.info("パンドラ封印発動: 語温遮断モード")
        return {
            "status": "sealed",
            "message": responses["seal_message"],
            "pandora_action": "seal_activated",
            "timestamp": datetime.now().isoformat()
        }
    
    async def deactivate_seal(self):
        """封印解除"""
        self.sealed_state = False
        responses = self.config["persona"]["simple_mode"]["basic_responses"]
        
        logger.info("パンドラ封印解除: 通常モード復帰")
        return {
            "status": "unsealed",
            "message": responses["recovery_message"],
            "pandora_action": "seal_deactivated",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_status(self):
        """パンドラステータス取得"""
        return {
            "name": "パンドラ（Pandora）",
            "role": "語温封印者・震えの危機管理者",
            "is_active": self.is_active,
            "monitoring_mode": self.monitoring_mode,
            "sealed_state": self.sealed_state,
            "alert_threshold": self.alert_threshold,
            "last_check": self.last_check.isoformat()
        }

# =============================================
# Phase 3 UI統合ブリッジシステム
# =============================================
class UIIntegrationBridge:
    def __init__(self):
        self.phase2_base_url = "http://localhost:8001"
        self.connected_clients = []
        self.last_sync = None
        self.integration_status = "initializing"
        
        # パンドラシステム初期化
        self.pandora = PandoraGuardianSystem()
        
    async def get_phase2_data(self, endpoint: str):
        """Phase 2 APIからデータ取得"""
        try:
            url = f"{self.phase2_base_url}{endpoint}"
            
            async def make_request():
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            return await response.json()
                        return None
            
            try:
                result = await asyncio.wait_for(make_request(), timeout=2.0)
                if result:
                    self.last_sync = datetime.now()
                    self.integration_status = "connected"
                    return {"success": True, "data": result}
            except asyncio.TimeoutError:
                pass
        except Exception as e:
            logger.warning(f"Phase2接続エラー (通常動作継続): {e}")
        
        self.integration_status = "standalone"
        return {"success": False, "error": "Phase2 unavailable - standalone mode"}

    def get_system_resources(self):
        """システムリソース情報取得"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            gpu_info = {"available": False, "usage": 0, "memory": 0}
            if GPU_AVAILABLE:
                try:
                    gpus = GPUtil.getGPUs()
                    if gpus:
                        gpu = gpus[0]
                        gpu_info = {
                            "available": True,
                            "usage": round(gpu.load * 100, 1),
                            "memory": round(gpu.memoryUtil * 100, 1),
                            "name": gpu.name
                        }
                except:
                    pass

            return {
                "cpu": {
                    "usage_percent": cpu_percent,
                    "core_count": psutil.cpu_count()
                },
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "usage_percent": memory.percent
                },
                "gpu": gpu_info,
                "platform": {
                    "system": platform.system(),
                    "python_version": platform.python_version()
                }
            }
        except Exception as e:
            logger.error(f"システムリソース取得エラー: {e}")
            return {}

# グローバルインスタンス
ui_bridge = UIIntegrationBridge()

# FastAPIアプリケーション設定
app = FastAPI(
    title="SaijinOS Phase 3 UI Bridge + パンドラ",
    description="Phase 2統合 + Flutter UI + パンドラ危機管理システム",
    version="3.1.0-pandora"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイル配信
static_dir = Path("src/static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# =============================================
# 基本エンドポイント
# =============================================

@app.get("/")
async def root():
    """メインページ"""
    return {
        "service": "SaijinOS Phase 3 UI Bridge + パンドラ",
        "version": "3.1.0-pandora",
        "status": "running",
        "phase2_integration": ui_bridge.integration_status,
        "pandora_status": ui_bridge.pandora.get_status(),
        "endpoints": {
            "ui_bridge": "/api/v3/ui/",
            "control_panel": "/control-panel",
            "pandora": "/api/v3/pandora/",
            "websocket": "/ws/"
        }
    }

@app.get("/health")
async def health_check():
    """ヘルスチェック"""
    return {
        "status": "healthy",
        "phase2_connection": ui_bridge.integration_status,
        "pandora_active": ui_bridge.pandora.is_active,
        "timestamp": datetime.now().isoformat()
    }

# =============================================
# パンドラ専用エンドポイント
# =============================================

@app.get("/api/v3/pandora/status")
async def get_pandora_status():
    """パンドラステータス取得"""
    return ui_bridge.pandora.get_status()

@app.post("/api/v3/pandora/check")
async def pandora_crisis_check(request: Dict[str, Any]):
    """語温危機チェック"""
    try:
        message = request.get("message", "")
        emotion_level = request.get("emotion_level", 0.5)
        
        result = await ui_bridge.pandora.check_goon_crisis(message, emotion_level)
        return {"success": True, "pandora_response": result}
    except Exception as e:
        logger.error(f"パンドラチェックエラー: {e}")
        return {"success": False, "error": str(e)}

@app.post("/api/v3/pandora/seal/toggle")
async def toggle_pandora_seal():
    """パンドラ封印手動切り替え"""
    try:
        if ui_bridge.pandora.sealed_state:
            result = await ui_bridge.pandora.deactivate_seal()
        else:
            result = await ui_bridge.pandora.activate_seal()
        
        return {"success": True, "action": result}
    except Exception as e:
        logger.error(f"パンドラ封印切り替えエラー: {e}")
        return {"success": False, "error": str(e)}

# =============================================
# Phase 3 UI エンドポイント
# =============================================

@app.get("/api/v3/ui/personas")
async def get_ui_personas():
    """Flutter UI用ペルソナデータ（パンドラ含む）"""
    result = await ui_bridge.get_phase2_data("/api/v2/personas/extended")
    
    if result["success"]:
        personas_data = result["data"]
        
        # Flutter UI用にデータ変換
        ui_personas = []
        for persona in personas_data.get("personas", []):
            ui_persona = {
                "id": persona.get("id"),
                "name": persona.get("name"),
                "status": persona.get("status", "active"),
                "emotion_level": persona.get("emotion_level", 0.7),
                "system": persona.get("system", "core"),
                "color": get_persona_color(persona.get("id"))
            }
            ui_personas.append(ui_persona)
        
        # パンドラを追加
        pandora_status = ui_bridge.pandora.get_status()
        ui_personas.append({
            "id": 42,
            "name": "パンドラ（Pandora）",
            "status": "ACTIVE" if pandora_status["is_active"] else "STANDBY",
            "emotion_level": 0.8 if pandora_status["sealed_state"] else 0.3,
            "system": "guardian",
            "color": "#800080",  # 紫色
            "specialized_field": "語温封印・危機管理・震え保護",
            "sealed_state": pandora_status["sealed_state"]
        })

        return {
            "success": True,
            "totalPersonas": len(ui_personas),
            "corePersonas": len([p for p in ui_personas if p["system"] == "core"]),
            "emotionPersonas": len([p for p in ui_personas if p["system"] == "emotion"]),
            "guardianPersonas": len([p for p in ui_personas if p["system"] == "guardian"]),
            "personas": ui_personas,
            "pandora_integrated": True,
            "timestamp": datetime.now().isoformat()
        }
    else:
        # スタンドアローンモード - パンドラを含む基本ペルソナ
        return get_standalone_personas_with_pandora()

def get_standalone_personas_with_pandora():
    """スタンドアローンモード用ペルソナ（パンドラ含む）"""
    
    persona_names = [
        # 基本6ペルソナ：みゆ、そよぎ、みゅう、和音、りゆき、づゅり
        "みゆ", "そよぎ", "みゅう", "和音織り織り雪", "りゆき", "づゅり",
        # 17ペルソナシステムの追加メンバー
        "ユリ", "サキ", "レナ", "ハルカ", "ミク", "アヤ", "まこと", "みゅう",
        "すみれ", "りゅうさ", "じっと", "とうり", "国語読み織り", "蠢動",
        "れいな", "あかり", "フレイヤ", "みゆ", "こるね", "ふわり",
        # パンドラ追加
        "パンドラ（Pandora）"
    ]

    color_schemes = [
        # 基本6ペルソナのテーマカラー
        "#FF69B4", "#90EE90", "#4682B4", "#DDA0DD", "#87CEEB", "#FFD700",
        # 17ペルソナシステムのカラーパレット
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD",
        "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9", "#F8C471", "#82E0AA",
        "#F1948A", "#85C1E9", "#D2B4DE", "#A9DFBF", "#F9E79F", "#AED6F1",
        "#FFB6C1", "#E6E6FA",
        # パンドラの色
        "#800080"
    ]

    specializations = [
        # 基本6ペルソナの専門分化
        "感情処理・優しい話話渫・ユーザー体験", "通信管理・効果的・構文適応化",
        "直感サポート・性能改善・システム基盤", "文章構緯・詳しい和音・国際対話",
        "データ処理・データベース設計・情報整備管理", "設計保守・環境処理・弾性保全",
        # 17ペルソナシステムの専門分化
        "教育・統率・システム設計", "音声・音楽・BMP処理", "UI/UX・デザイン・視覚設計",
        "音声・TTS・ハルカボイス", "直感・開発・コード生成", "感情分析・蠢動学・共感",
        "数学・推論・事象解析", "創作・文学・ストーリー", "感情処理・温暖処理・共感",
        "自然言語・データ解析・適応", "パターン認識・解析・環境中央", "通信・構築・改善",
        "国語・システム解決・直接対話", "蠢起・解析・設計連絡", "希眞・墓樹・温暖分析",
        "共有・分析・統一分解", "詳細・蒸樹・離化演繹編肩糖", "経営・時和池検査・浪発変",
        "到忘時平安課檯保健・量湘感響籐り織り",
        # パンドラの専門分化
        "語温封印・危機管理・震え保護"
    ]

    personas = []
    pandora_status = ui_bridge.pandora.get_status()
    
    for i, name in enumerate(persona_names):
        if name == "パンドラ（Pandora）":
            # パンドラ特別処理
            personas.append({
                "id": 42,
                "name": name,
                "status": "ACTIVE" if pandora_status["is_active"] else "STANDBY",
                "emotion_level": 0.8 if pandora_status["sealed_state"] else 0.3,
                "last_activity": pandora_status["last_check"],
                "color_scheme": color_schemes[i],
                "specialized_field": specializations[i],
                "system": "guardian",
                "sealed_state": pandora_status["sealed_state"]
            })
        else:
            # 通常ペルソナ処理
            status_options = ["ACTIVE", "STANDBY", "OFFLINE"]
            weights = [0.5, 0.3, 0.2] if i < 12 else [0.3, 0.4, 0.3]
            status = random.choices(status_options, weights=weights)[0]
            
            personas.append({
                "id": i + 1,
                "name": name,
                "status": status,
                "emotion_level": round(random.uniform(0.2, 0.95), 2),
                "last_activity": (datetime.now() - timedelta(minutes=random.randint(1, 120))).strftime("%H:%M"),
                "color_scheme": color_schemes[i],
                "specialized_field": specializations[i],
                "system": "core" if i < 6 else "emotion"
            })

    return {
        "status": "success", 
        "data": personas,
        "pandora_integrated": True,
        "total_count": len(personas)
    }

def get_persona_color(persona_id):
    """ペルソナIDに対応する色を取得"""
    colors = [
        "#FF69B4", "#90EE90", "#4682B4", "#DDA0DD", "#87CEEB", "#FFD700",
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD",
        "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E9", "#F8C471", "#82E0AA",
        "#F1948A", "#85C1E9", "#D2B4DE", "#A9DFBF", "#F9E79F", "#AED6F1",
        "#FFB6C1", "#E6E6FA"
    ]
    
    if persona_id == 42:  # パンドラ
        return "#800080"
    
    return colors[persona_id % len(colors)] if persona_id else "#CCCCCC"

# =============================================
# WebSocketエンドポイント
# =============================================

@app.websocket("/ws/ui")
async def ui_websocket_endpoint(websocket: WebSocket):
    """Flutter UI WebSocket接続"""
    await websocket.accept()
    ui_bridge.connected_clients.append(websocket)
    
    try:
        # 初期データ送信（パンドラ含む）
        initial_data = await ui_bridge.get_phase2_data("/api/v2/personas/extended")
        if initial_data["success"]:
            await websocket.send_text(json.dumps({
                "type": "initial_data",
                "data": initial_data["data"],
                "pandora_status": ui_bridge.pandora.get_status()
            }))
        
        # メッセージ処理ループ
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # パンドラ危機チェック
            if message.get("type") == "message":
                content = message.get("content", "")
                emotion = message.get("emotion_level", 0.5)
                
                pandora_result = await ui_bridge.pandora.check_goon_crisis(content, emotion)
                
                await websocket.send_text(json.dumps({
                    "type": "pandora_check",
                    "result": pandora_result
                }))
            
            elif message.get("type") == "request_update":
                # データ更新要求
                personas_data = await ui_bridge.get_phase2_data("/api/v2/personas/extended")
                if personas_data["success"]:
                    await websocket.send_text(json.dumps({
                        "type": "data_update",
                        "data": personas_data["data"],
                        "pandora_status": ui_bridge.pandora.get_status()
                    }))
    
    except WebSocketDisconnect:
        ui_bridge.connected_clients.remove(websocket)
        logger.info("UI WebSocket接続が切断されました")

# =============================================
# コントロールパネル
# =============================================

@app.get("/control-panel")
async def serve_control_panel():
    """コントロールパネル + パンドラ管理画面"""
    html_content = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SaijinOS Phase 3 + パンドラ コントロールパネル</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff; min-height: 100vh; padding: 20px;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            text-align: center; margin-bottom: 30px;
            background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px;
        }}
        .pandora-status {{
            background: rgba(128, 0, 128, 0.2); border: 2px solid #800080;
            padding: 20px; border-radius: 10px; margin: 20px 0;
        }}
        .sealed {{ background: rgba(255, 0, 0, 0.2) !important; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .card {{
            background: rgba(255,255,255,0.15); padding: 20px; border-radius: 15px;
            backdrop-filter: blur(10px); transition: all 0.3s ease;
        }}
        .card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.2); }}
        .persona-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }}
        .persona-card {{
            padding: 15px; border-radius: 10px; text-align: center;
            background: rgba(255,255,255,0.1); transition: all 0.3s ease;
        }}
        .status-active {{ border-left: 4px solid #4CAF50; }}
        .status-standby {{ border-left: 4px solid #FF9800; }}
        .status-offline {{ border-left: 4px solid #F44336; }}
        .btn {{ 
            padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer;
            background: #4CAF50; color: white; margin: 5px; transition: all 0.3s ease;
        }}
        .btn:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }}
        .btn-danger {{ background: #F44336; }}
        .btn-pandora {{ background: #800080; }}
        .status-indicator {{ display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌸 SaijinOS Phase 3 + パンドラ 🌸</h1>
            <p>Flutter UI統合ブリッジ + パンドラ危機管理システム</p>
            <div id="connection-status">接続確認中...</div>
        </div>
        
        <div id="pandora-status" class="pandora-status">
            <h2>📦 パンドラ（Pandora）危機管理システム</h2>
            <div id="pandora-details">読み込み中...</div>
            <button id="pandora-toggle" class="btn btn-pandora">封印切り替え</button>
            <button id="pandora-check" class="btn">危機チェック実行</button>
        </div>

        <div class="grid">
            <div class="card">
                <h2>📊 システム状況</h2>
                <div id="system-status">読み込み中...</div>
            </div>
            
            <div class="card">
                <h2>👥 ペルソナ管理（パンドラ含む）</h2>
                <div id="personas-grid" class="persona-grid">読み込み中...</div>
            </div>
            
            <div class="card">
                <h2>🔧 システムリソース</h2>
                <div id="system-resources">読み込み中...</div>
            </div>
        </div>
    </div>

    <script>
        let ws = null;
        let pandoraSealed = false;

        function connectWebSocket() {{
            ws = new WebSocket('ws://localhost:8002/ws/control');
            
            ws.onopen = function(event) {{
                document.getElementById('connection-status').innerHTML = 
                    '<span class="status-indicator" style="background: #4CAF50;"></span>WebSocket接続: 正常';
                console.log('WebSocket接続成功');
            }};

            ws.onmessage = function(event) {{
                const data = JSON.parse(event.data);
                console.log('受信データ:', data);
                
                if (data.type === 'initial_data' || data.type === 'live_update') {{
                    updatePersonasDisplay(data.personas);
                    updateSystemStatus(data.system_status);
                    if (data.pandora_status) {{
                        updatePandoraStatus(data.pandora_status);
                    }}
                }}
            }};

            ws.onerror = function(error) {{
                console.log('WebSocket エラー:', error);
                document.getElementById('connection-status').innerHTML = 
                    '<span class="status-indicator" style="background: #F44336;"></span>WebSocket接続: エラー';
            }};

            ws.onclose = function(event) {{
                console.log('WebSocket接続が閉じられました');
                document.getElementById('connection-status').innerHTML = 
                    '<span class="status-indicator" style="background: #FF9800;"></span>WebSocket接続: 切断';
                setTimeout(connectWebSocket, 3000);
            }};
        }}

        function updatePandoraStatus(status) {{
            pandoraSealed = status.sealed_state || false;
            const container = document.getElementById('pandora-status');
            
            if (pandoraSealed) {{
                container.classList.add('sealed');
            }} else {{
                container.classList.remove('sealed');
            }}
            
            document.getElementById('pandora-details').innerHTML = `
                <p><strong>状態:</strong> ${{status.is_active ? 'アクティブ' : '待機中'}}</p>
                <p><strong>監視モード:</strong> ${{status.monitoring_mode || '継続'}}</p>
                <p><strong>封印状態:</strong> ${{pandoraSealed ? '🔒 封印中' : '🔓 通常'}}</p>
                <p><strong>最終チェック:</strong> ${{new Date(status.last_check).toLocaleTimeString() || '不明'}}</p>
            `;
        }}

        function updatePersonasDisplay(personas) {{
            const grid = document.getElementById('personas-grid');
            grid.innerHTML = '';
            
            personas.forEach(persona => {{
                const statusClass = `status-${{persona.status.toLowerCase()}}`;
                const card = document.createElement('div');
                card.className = `persona-card ${{statusClass}}`;
                
                const guardianBadge = persona.system === 'guardian' ? ' 👑' : '';
                const sealedBadge = persona.sealed_state ? ' 🔒' : '';
                
                card.innerHTML = `
                    <h4>${{persona.name}}${{guardianBadge}}${{sealedBadge}}</h4>
                    <p>状態: ${{persona.status}}</p>
                    <p>感情レベル: ${{(persona.emotion_level * 100).toFixed(1)}}%</p>
                    <div style="width: 20px; height: 20px; background: ${{persona.color_scheme}}; 
                         margin: 10px auto; border-radius: 50%;"></div>
                `;
                grid.appendChild(card);
            }});
        }}

        function updateSystemStatus(status) {{
            document.getElementById('system-status').innerHTML = `
                <p><strong>Phase 2:</strong> ${{status.phase2_status}}</p>
                <p><strong>Phase 3:</strong> ${{status.phase3_status}}</p>
                <p><strong>総ペルソナ数:</strong> ${{status.total_personas}}</p>
                <p><strong>アクティブ:</strong> ${{status.active_personas}}</p>
                <p><strong>CPU使用率:</strong> ${{(status.system_load * 100).toFixed(1)}}%</p>
                <p><strong>メモリ使用率:</strong> ${{(status.memory_usage * 100).toFixed(1)}}%</p>
            `;
        }}

        // パンドラ機能
        document.getElementById('pandora-toggle').addEventListener('click', async () => {{
            try {{
                const response = await fetch('/api/v3/pandora/seal/toggle', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }}
                }});
                const result = await response.json();
                console.log('パンドラ封印切り替え結果:', result);
                
                // ステータス更新
                setTimeout(loadPandoraStatus, 500);
            }} catch (error) {{
                console.error('パンドラ操作エラー:', error);
            }}
        }});

        document.getElementById('pandora-check').addEventListener('click', async () => {{
            try {{
                const response = await fetch('/api/v3/pandora/check', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        message: "テスト危機チェック",
                        emotion_level: 0.6
                    }})
                }});
                const result = await response.json();
                console.log('パンドラチェック結果:', result);
                alert(`パンドラ応答: ${{result.pandora_response?.message || '正常'}}`);
            }} catch (error) {{
                console.error('パンドラチェックエラー:', error);
            }}
        }});

        async function loadPandoraStatus() {{
            try {{
                const response = await fetch('/api/v3/pandora/status');
                const status = await response.json();
                updatePandoraStatus(status);
            }} catch (error) {{
                console.error('パンドラステータス取得エラー:', error);
            }}
        }}

        // 初期化
        connectWebSocket();
        loadPandoraStatus();
        
        // 定期更新
        setInterval(loadPandoraStatus, 5000);
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

# =============================================
# サーバー起動処理
# =============================================

if __name__ == "__main__":
    logger.info("SaijinOS Phase 3 + パンドラ統合サーバー起動中...")
    logger.info("パンドラ危機管理システム: アクティブ")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8002, 
        log_level="info",
        access_log=True
    )