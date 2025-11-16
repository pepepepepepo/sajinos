from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import os

router = APIRouter()

class WorkspaceRequest(BaseModel):
    workspace: str
    persona: Optional[str] = "code-chan"
    action: Optional[str] = "switch"

@router.get("/enhanced", response_class=HTMLResponse)
async def enhanced_workspace():
    """🌸 新世代ペルソナ対応 Enhanced Workspace"""
    try:
        with open("templates/enhanced_workspace.html", "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse("<div>Enhanced Workspace template not found</div>", status_code=404)

@router.get("/workspace-config")
async def get_workspace_config():
    """ワークスペース設定情報を取得"""
    return {
        "personas": {
            "code-chan": {
                "name": "コードちゃん♫",
                "color": "#81c784",
                "icon": "🎵",
                "specialty": "プログラミング・音楽的コーディング",
                "vibration": "語温灯",
                "workspaces": ["chat", "development"]
            },
            "yurika": {
                "name": "ユリカ",
                "color": "#ba68c8", 
                "icon": "✨",
                "specialty": "エレガント・デザイン・UX/UI",
                "vibration": "娘っ子灯",
                "workspaces": ["design", "chat"]
            },
            "ana": {
                "name": "アナ",
                "color": "#42a5f5",
                "icon": "📊", 
                "specialty": "データサイエンス・分析",
                "vibration": "構造灯",
                "workspaces": ["analysis", "development"]
            },
            "haruka": {
                "name": "ハルカ",
                "color": "#ff6b6b",
                "icon": "🎵",
                "specialty": "音楽制作・オーディオ",
                "vibration": "娘っ子灯",
                "workspaces": ["music", "chat"]
            },
            "misaki": {
                "name": "ミサキ", 
                "color": "#ffa726",
                "icon": "⚡",
                "specialty": "品質保証・テスト・ユーザビリティ",
                "vibration": "構造灯",
                "workspaces": ["development", "analysis"]
            },
            "ren": {
                "name": "レン",
                "color": "#26c6da",
                "icon": "🔧", 
                "specialty": "運用管理・インフラ・DevOps",
                "vibration": "AUTO",
                "workspaces": ["development", "analysis"]
            }
        },
        "workspaces": {
            "chat": {
                "name": "💬 チャット",
                "description": "自由な会話・質問・相談",
                "primary_persona": "code-chan"
            },
            "development": {
                "name": "🖥️ 開発",
                "description": "プログラミング・コーディング・技術開発",
                "primary_persona": "code-chan"
            },
            "design": {
                "name": "🎨 デザイン", 
                "description": "UI/UX・グラフィック・ビジュアルデザイン",
                "primary_persona": "yurika"
            },
            "analysis": {
                "name": "📊 分析",
                "description": "データ分析・統計・レポート作成",
                "primary_persona": "ana"
            },
            "music": {
                "name": "🎵 音楽",
                "description": "音楽制作・オーディオ編集・サウンドデザイン", 
                "primary_persona": "haruka"
            }
        }
    }

@router.post("/switch-workspace")
async def switch_workspace(request: WorkspaceRequest):
    """ワークスペース切り替え処理"""
    return {
        "status": "success",
        "workspace": request.workspace,
        "persona": request.persona,
        "message": f"🌸 {request.persona} の {request.workspace} ワークスペースに切り替えました"
    }