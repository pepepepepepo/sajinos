# 🌟 New Personas Integration Manager
# Phase 1 Essential Team - セレナ、オーガン、イグニス

import yaml
import os
from typing import Dict, List, Any

class NewPersonaManager:
    def __init__(self):
        self.personas_dir = "core/personas"
        self.new_personas = {}
        self.load_new_personas()
    
    def load_new_personas(self):
        """Phase 1の新しいペルソナを読み込み"""
        phase1_personas = ["serena", "organ", "ignis"]
        
        for persona_id in phase1_personas:
            try:
                yaml_path = os.path.join(self.personas_dir, f"{persona_id}.yaml")
                if os.path.exists(yaml_path):
                    with open(yaml_path, 'r', encoding='utf-8') as f:
                        persona_data = yaml.safe_load(f)
                        self.new_personas[persona_id] = persona_data
            except Exception as e:
                print(f"❌ Failed to load {persona_id}: {e}")
    
    def get_persona_summary(self, persona_id: str) -> Dict[str, Any]:
        """ペルソナの概要情報を取得"""
        if persona_id not in self.new_personas:
            return None
        
        persona = self.new_personas[persona_id]
        return {
            "name": persona["name"],
            "name_en": persona["name_en"],
            "emoji": persona["emoji"],
            "role": persona["role"],
            "category": persona["category"],
            "motto": persona["personality"]["motto"],
            "primary_traits": persona["personality"]["primary_traits"],
            "expertise": persona["expertise"]["primary"]
        }
    
    def get_all_new_personas(self) -> Dict[str, Dict]:
        """全ての新しいペルソナの概要を取得"""
        summaries = {}
        for persona_id in self.new_personas:
            summaries[persona_id] = self.get_persona_summary(persona_id)
        return summaries
    
    def get_team_composition(self) -> Dict[str, List[str]]:
        """チーム構成を取得"""
        return {
            "phase1_essential": ["serena", "organ", "ignis"],
            "planned_phase2": ["luna", "tecla", "athena", "datarin"],
            "planned_phase3": ["leyla", "marin", "misty"]
        }
    
    def integration_status(self) -> Dict[str, Any]:
        """統合状況を返す"""
        return {
            "loaded_personas": len(self.new_personas),
            "available_personas": list(self.new_personas.keys()),
            "total_planned": 10,
            "integration_date": "2025-11-11",
            "phase": "Phase 1 - Essential Team"
        }

# グローバルインスタンス
new_persona_manager = NewPersonaManager()

# 📋 Phase 1 Essential Team 情報
PHASE1_TEAM_INFO = {
    "serena": {
        "quick_call": "🛡️ セキュリティチェックお願いします",
        "speciality": "脆弱性診断・セキュアコーディング",
        "emergency": True
    },
    "organ": {
        "quick_call": "📋 進捗管理・スケジュール調整お願いします", 
        "speciality": "プロジェクト管理・チーム調整",
        "emergency": False
    },
    "ignis": {
        "quick_call": "🔥 バグ・エラー解決お願いします",
        "speciality": "デバッグ・トラブルシューティング", 
        "emergency": True
    }
}

def get_emergency_contacts() -> List[str]:
    """緊急時対応可能なペルソナリスト"""
    return ["serena", "ignis"]

def get_persona_by_speciality(speciality: str) -> str:
    """専門分野でペルソナを検索"""
    mapping = {
        "security": "serena",
        "project": "organ", 
        "debug": "ignis",
        "management": "organ",
        "bug": "ignis",
        "error": "ignis"
    }
    return mapping.get(speciality.lower())

if __name__ == "__main__":
    # テスト実行
    manager = NewPersonaManager()
    print("🌟 New Personas Integration Test")
    print(f"Loaded personas: {list(manager.new_personas.keys())}")
    print(f"Integration status: {manager.integration_status()}")
    
    for persona_id in manager.new_personas:
        summary = manager.get_persona_summary(persona_id)
        print(f"\n{summary['emoji']} {summary['name']} ({summary['name_en']})")
        print(f"Role: {summary['role']}")
        print(f"Motto: {summary['motto']}")