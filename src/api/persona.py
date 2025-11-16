# -*- coding: utf-8 -*-
"""
ペルソナAPI ルート
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter()

@router.get("/core")
async def get_core_personas():
    """コアペルソナ一覧取得"""
    return {
        "personas": [
            {"id": "code", "name": "Code-chan♫", "role": "テクニカルリーダー"},
            {"id": "yurika", "name": "Yurika", "role": "UI/UXデザイナー"},
            {"id": "ana", "name": "Ana", "role": "データサイエンティスト"},
            {"id": "haruka", "name": "Haruka", "role": "音楽プロデューサー"},
            {"id": "misaki", "name": "Misaki", "role": "品質保証エンジニア"},
            {"id": "ren", "name": "Ren", "role": "DevOpsエンジニア"}
        ],
        "total": 6
    }

@router.get("/{persona_id}")
async def get_persona_info(persona_id: str):
    """特定ペルソナ情報取得"""
    # TODO: PersonaManagerから情報取得
    return {
        "id": persona_id,
        "name": f"Persona {persona_id}",
        "status": "active"
    }

@router.get("/recommend/{workspace}")
async def recommend_personas(workspace: str):
    """ワークスペース別推奨ペルソナ"""
    recommendations = {
        "chat": ["code", "yurika", "haruka"],
        "development": ["code", "ana", "misaki"],
        "design": ["yurika", "haruka", "code"],
        "analysis": ["ana", "code", "misaki"],
        "music": ["haruka", "yurika", "code"]
    }
    
    return {
        "workspace": workspace,
        "recommended": recommendations.get(workspace, ["code"])
    }