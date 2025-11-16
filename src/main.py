#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SaijinOS Creative Studio - メインアプリケーション (リファクタリング版)
FastAPI + Jinja2テンプレート + モジュール分離

🎯 目標: 元ファイル 277KB → 新ファイル ~30KB (90%削減)
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn
import os
from typing import Dict, Any, Optional

# モジュールインポート
from api.chat import router as chat_router
from api.workspace import router as workspace_router
from api.code_execution import router as code_execution_router
from api.persona import router as persona_router
from api.enhanced_workspace import router as enhanced_workspace_router
from api.ai_integration import router as ai_router
from api.real_ai import router as real_ai_router
from core.persona_manager import PersonaManager
from core.workspace_manager import WorkspaceManager
from core.vibration_system import VibrationSystem

# FastAPI アプリケーション
app = FastAPI(
    title="SaijinOS Creative Studio",
    description="Ultimate Creative Studio with Hybrid Persona System",
    version="2.0.0"
)

# 静的ファイルとテンプレート設定
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# システム初期化
persona_manager = PersonaManager()
workspace_manager = WorkspaceManager()
vibration_system = VibrationSystem()

# APIルート登録
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(workspace_router, prefix="/api/workspace", tags=["workspace"])
app.include_router(persona_router, prefix="/api/persona", tags=["persona"])
app.include_router(enhanced_workspace_router, prefix="/enhanced", tags=["enhanced"])
app.include_router(ai_router, prefix="/api/ai", tags=["ai"])
app.include_router(real_ai_router, prefix="/api/real-ai", tags=["real-ai"])
app.include_router(code_execution_router, prefix="/api", tags=["code-execution"])

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """メインページ"""
    context = {
        "request": request,
        "title": "SaijinOS Creative Studio",
        "personas": persona_manager.get_core_personas(),
        "workspaces": workspace_manager.get_available_workspaces(),
        "vibrations": vibration_system.get_vibration_modes()
    }
    return templates.TemplateResponse("index.html", context)

@app.get("/workspace/{workspace_name}", response_class=HTMLResponse)
async def workspace(request: Request, workspace_name: str):
    """ワークスペースページ"""
    if not workspace_manager.is_valid_workspace(workspace_name):
        raise HTTPException(status_code=404, detail="Workspace not found")
    
    context = {
        "request": request,
        "workspace": workspace_manager.get_workspace_config(workspace_name),
        "workspace_name": workspace_name,
        "recommended_personas": persona_manager.get_recommended_personas(workspace_name),
        "tools": workspace_manager.get_workspace_tools(workspace_name)
    }
    return templates.TemplateResponse("workspace.html", context)

@app.get("/api/system/status")
async def system_status():
    """システム状況API"""
    return {
        "status": "active",
        "version": "2.0.0",
        "personas_loaded": persona_manager.get_persona_count(),
        "workspaces_available": len(workspace_manager.get_available_workspaces()),
        "vibration_modes": len(vibration_system.get_vibration_modes()),
        "integration_type": "hybrid"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8017,
        reload=True,
        log_level="info"
    )