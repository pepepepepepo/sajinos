# -*- coding: utf-8 -*-
"""
ワークスペースAPI ルート
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

router = APIRouter()

class WorkspaceRequest(BaseModel):
    workspace_mode: str
    action: str
    parameters: Optional[Dict] = None

@router.get("/{workspace_name}")
async def get_workspace_info(workspace_name: str):
    """ワークスペース情報取得"""
    # TODO: WorkspaceManagerから情報取得
    return {
        "workspace": workspace_name,
        "status": "active",
        "tools": [],
        "features": []
    }

@router.post("/switch")
async def switch_workspace(request: WorkspaceRequest):
    """ワークスペース切り替え"""
    return {
        "success": True,
        "workspace": request.workspace_mode,
        "action": request.action
    }