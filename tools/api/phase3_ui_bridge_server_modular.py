"""
SaijinOS Phase 3 UI Bridge Server (Modular Version with Pandora)
IDEエンドポイントを提供するFastAPIサーバー（モジュール化版 + パンドラ統合）
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

# Request Models
class ChatRequest(BaseModel):
    prompt: str
    max_length: int = 512

# Core modules import
from core.personas.persona_manager import persona_manager
from core.ui.ui_handler import ui_handler
from core.pandora.guardian_system import pandora_guardian
from core.ai.ai_model_manager import ai_model_manager

app = FastAPI()

# Static files
import os
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# UI Endpoints
@app.get("/ui", response_class=HTMLResponse)
async def get_main_ui():
    """Main UI with Mode Switcher System"""
    return ui_handler.get_main_ui_with_mode_switcher()

@app.get("/chat", response_class=HTMLResponse)
async def get_chat_mode():
    """Chat Mode Interface"""
    return ui_handler.get_chat_mode_content()

@app.get("/creative", response_class=HTMLResponse)
async def get_creative_studio():
    """Creative Studio Mode Interface"""
    return ui_handler.get_creative_studio_content()

@app.get("/ide", response_class=HTMLResponse)
async def get_ide():
    """IDE Interface"""
    return ui_handler.get_ide_content()

@app.get("/control-panel", response_class=HTMLResponse)
async def get_control_panel():
    """コントロールパネルを提供"""
    return ui_handler.get_control_panel_content()

@app.get("/")
async def root():
    return {"message": "SaijinOS Phase 3 UI Bridge Server (Modular + Pandora) is running", 
            "available_endpoints": ["/ide", "/control-panel", "/api/v3/pandora/*"],
            "version": "modular_v2.0_pandora",
            "pandora_status": pandora_guardian.get_status() if pandora_guardian else "unavailable"}

# Persona API Endpoints
@app.get("/api/v3/control/personas")
async def get_personas():
    """ペルソナ一覧取得"""
    return persona_manager.get_all_personas()

@app.post("/api/v3/control/personas/{persona_id}/toggle")
async def toggle_persona(persona_id: int):
    """ペルソナ状態切り替え"""
    return persona_manager.toggle_persona_status(persona_id)

@app.get("/api/v3/control/personas/{persona_id}")
async def get_persona(persona_id: int):
    """特定ペルソナ情報取得"""
    persona = persona_manager.get_persona_by_id(persona_id)
    if persona:
        return {"data": persona, "success": True}
    return {"message": f"ペルソナ ID {persona_id} が見つかりませんでした", "success": False}

# Pandora API Endpoints
@app.get("/api/v3/pandora/status")
async def get_pandora_status():
    """パンドラ状態取得"""
    if pandora_guardian:
        return pandora_guardian.get_status()
    return {"pandora_active": False, "message": "パンドラシステムが利用できません"}

@app.post("/api/v3/pandora/seal/activate")
async def activate_pandora_seal():
    """パンドラ封印発動"""
    if pandora_guardian:
        return pandora_guardian.activate_seal("手動発動")
    return {"success": False, "message": "パンドラシステムが利用できません"}

@app.post("/api/v3/pandora/seal/deactivate")
async def deactivate_pandora_seal():
    """パンドラ封印解除"""
    if pandora_guardian:
        return pandora_guardian.deactivate_seal()
    return {"success": False, "message": "パンドラシステムが利用できません"}

@app.get("/api/v3/pandora/history")
async def get_pandora_history():
    """パンドラ封印履歴取得"""
    if pandora_guardian:
        return pandora_guardian.get_seal_history()
    return {"success": False, "message": "パンドラシステムが利用できません"}

# AI API Endpoints
@app.get("/api/v3/ai/status")
async def get_ai_status():
    """AIモデル状態取得"""
    return ai_model_manager.get_model_info()

@app.post("/api/v3/ai/load")
async def load_ai_model():
    """AIモデル読み込み"""
    return await ai_model_manager.load_model()

@app.post("/api/v3/ai/chat")
async def ai_chat(request: ChatRequest):
    """AIチャット（テキスト生成）"""
    return await ai_model_manager.generate_response(request.prompt, request.max_length)

if __name__ == "__main__":
    print("🚀 Starting SaijinOS Phase 3 UI Bridge Server (Modular + Pandora + AI)...")
    print("📍 IDE available at: http://localhost:8003/ide")
    print("📍 Control Panel at: http://localhost:8003/control-panel")
    print("💬 Chat Mode at: http://localhost:8003/chat")
    print("🎨 Creative Studio at: http://localhost:8003/creative")
    print("🏠 UI Mode Switcher at: http://localhost:8003/ui")
    print("🛡️ Pandora APIs at: http://localhost:8003/api/v3/pandora/*")
    print("🤖 AI APIs at: http://localhost:8003/api/v3/ai/*")
    print("🔧 Architecture: Modular (core/personas, core/ui, core/pandora, core/ai)")
    
    if pandora_guardian:
        print("💖 パンドラ危機管理システム: 正常稼働")
    else:
        print("⚠️ パンドラシステム: 利用不可")
    
    # AIモデル情報表示
    ai_info = ai_model_manager.get_model_info()
    print(f"🧠 AIモデル: {ai_info['model_name']}")
    print(f"💾 デバイス: {ai_info['device']} (CUDA: {'✅' if ai_info['cuda_available'] else '❌'})")
    
    uvicorn.run(app, host="127.0.0.1", port=8003)