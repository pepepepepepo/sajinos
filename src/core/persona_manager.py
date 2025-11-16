# -*- coding: utf-8 -*-
"""
ペルソナ管理システム
6ペルソナ + 57ペルソナ ハイブリッド管理
"""

import yaml
import os
from typing import Dict, List, Any, Optional

class PersonaManager:
    """ハイブリッドペルソナ管理システム"""
    
    def __init__(self, personas_path="../personas"):
        self.personas_path = personas_path
        self.core_personas = self._load_core_personas()
        self.extended_personas = self._load_extended_personas()
    
    def _load_core_personas(self) -> Dict[str, Any]:
        """6ペルソナコアチーム読み込み"""
        core_files = [
            "72_code_chan_v2.yaml",
            "73_yurika_v2.yaml", 
            "74_ana_v2.yaml",
            "75_haruka_v2.yaml",
            "76_misaki_v2.yaml",
            "77_ren_v2.yaml"
        ]
        
        personas = {}
        for file_name in core_files:
            file_path = os.path.join(self.personas_path, file_name)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                        key = file_name.split('_')[1]  # "code", "yurika", etc
                        personas[key] = data
                except Exception as e:
                    print(f"Warning: Could not load {file_name}: {e}")
        
        return personas
    
    def _load_extended_personas(self) -> Dict[str, Any]:
        """57ペルソナ拡張チーム読み込み"""
        master_file = os.path.join(self.personas_path, "personas_master.yaml")
        if os.path.exists(master_file):
            try:
                with open(master_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                print(f"Warning: Could not load personas_master.yaml: {e}")
        return {}
    
    def get_core_personas(self) -> List[Dict[str, Any]]:
        """コアペルソナ一覧取得"""
        return [
            {"id": "code", "name": "Code-chan♫", "role": "テクニカルリーダー"},
            {"id": "yurika", "name": "Yurika", "role": "UI/UXデザイナー"},
            {"id": "ana", "name": "Ana", "role": "データサイエンティスト"},
            {"id": "haruka", "name": "Haruka", "role": "音楽プロデューサー"},
            {"id": "misaki", "name": "Misaki", "role": "品質保証エンジニア"},
            {"id": "ren", "name": "Ren", "role": "DevOpsエンジニア"}
        ]
    
    def get_recommended_personas(self, workspace: str) -> List[str]:
        """ワークスペース別推奨ペルソナ"""
        recommendations = {
            "chat": ["code", "yurika", "haruka"],
            "development": ["code", "ana", "misaki"],
            "design": ["yurika", "haruka", "code"],
            "analysis": ["ana", "code", "misaki"],
            "music": ["haruka", "yurika", "code"]
        }
        return recommendations.get(workspace, ["code"])
    
    def get_persona_count(self) -> int:
        """総ペルソナ数"""
        return len(self.core_personas) + 57  # 6 + 57 = 63
    
    def get_persona_info(self, persona_id: str) -> Optional[Dict[str, Any]]:
        """ペルソナ情報取得"""
        if persona_id in self.core_personas:
            return self.core_personas[persona_id]
        return None