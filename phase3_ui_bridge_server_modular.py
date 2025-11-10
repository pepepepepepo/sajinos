"""
SaijinOS Phase 3 UI Bridge Server (Modular Version with Pandora)
IDEエンドポイントを提供するFastAPIサーバー（モジュール化版 + パンドラ統合）
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

# Core modules import
from core.personas.persona_manager import persona_manager
from core.ui.ui_handler import ui_handler
from core.pandora.guardian_system import pandora_guardian

app = FastAPI()

# UI Endpoints
@app.get("/ide", response_class=HTMLResponse)
async def get_ide():
    """IDEインターフェースを提供"""
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

if __name__ == "__main__":
    print("🚀 Starting SaijinOS Phase 3 UI Bridge Server (Modular + Pandora)...")
    print("📍 IDE available at: http://localhost:8002/ide")
    print("📍 Control Panel at: http://localhost:8002/control-panel")
    print("🛡️ Pandora APIs at: http://localhost:8002/api/v3/pandora/*")
    print("🔧 Architecture: Modular (core/personas, core/ui, core/pandora)")
    
    if pandora_guardian:
        print("💖 パンドラ危機管理システム: 正常稼働")
    else:
        print("⚠️ パンドラシステム: 利用不可")
    
    uvicorn.run(app, host="127.0.0.1", port=8002)