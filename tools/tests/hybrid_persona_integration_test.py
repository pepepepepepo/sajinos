#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
6ペルソナ ハイブリッド統合プロトタイプ
SaijinOS Ultimate Creative Studio - New Generation Team Integration

🌟 統合機能:
- 6ペルソナ新世代チーム (メイン)
- 57ペルソナ専門チーム (サポート)
- 4振動システム完全対応
- 5ワークスペース統合
"""

import yaml
import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

class PersonaSystemIntegrator:
    """6ペルソナ + 57ペルソナ ハイブリッド統合システム"""
    
    def __init__(self):
        self.base_path = "personas"
        self.config_path = "config"
        
        # 新世代6ペルソナチーム (メイン)
        self.core_team = self._load_core_team()
        
        # 57ペルソナ専門チーム (サポート)
        self.extended_team = self._load_extended_team()
        
        # 統合ペルソナレジストリ
        self.persona_registry = self._build_persona_registry()
        
        # 4振動システム
        self.vibration_models = {
            "goonro": {"label": "🌸語温灯", "model": "tinyllama", "status": "active"},
            "structure": {"label": "🔧構造灯", "model": "qwen", "status": "active"}, 
            "musumekko": {"label": "💫娘っ子灯", "model": "rinna", "status": "active"},
            "auto": {"label": "🔄AUTO", "model": "deepseek", "status": "active"}
        }
        
        # 5ワークスペース
        self.workspace_modes = {
            "chat": {"core_personas": ["code_chan"], "extended_available": True},
            "development": {"core_personas": ["code_chan"], "extended_available": True},
            "design": {"core_personas": ["yurika"], "extended_available": True},
            "analysis": {"core_personas": ["ana"], "extended_available": True},
            "music": {"core_personas": ["haruka"], "extended_available": True}
        }
    
    def _load_core_team(self) -> Dict[str, Any]:
        """新世代6ペルソナチーム読み込み"""
        core_team = {}
        
        # 6ペルソナのファイルパス
        core_files = [
            "72_code_chan_v2.yaml",
            "73_yurika_v2.yaml", 
            "74_ana_v2.yaml",
            "75_haruka_v2.yaml",
            "76_misaki_v2.yaml",
            "77_ren_v2.yaml"
        ]
        
        for file_name in core_files:
            file_path = os.path.join(self.base_path, file_name)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        persona_data = yaml.safe_load(f)
                        persona_key = file_name.split('_')[1]  # "code", "yurika", etc.
                        core_team[persona_key] = persona_data
                except Exception as e:
                    print(f"Warning: Could not load {file_name}: {e}")
        
        return core_team
    
    def _load_extended_team(self) -> Dict[str, Any]:
        """57ペルソナ専門チーム読み込み"""
        extended_team = {}
        
        master_file = os.path.join(self.base_path, "personas_master.yaml")
        if os.path.exists(master_file):
            try:
                with open(master_file, 'r', encoding='utf-8') as f:
                    extended_team = yaml.safe_load(f)
            except Exception as e:
                print(f"Warning: Could not load personas_master.yaml: {e}")
        
        return extended_team
    
    def _build_persona_registry(self) -> Dict[str, Any]:
        """統合ペルソナレジストリ構築"""
        registry = {
            "core_team": {
                "count": len(self.core_team),
                "personas": self.core_team,
                "priority": "primary"
            },
            "extended_team": {
                "count": self.extended_team.get("saijinos_personas_master", {}).get("meta", {}).get("total_personas", 0),
                "personas": self.extended_team,
                "priority": "secondary"
            },
            "integration_strategy": "hybrid",
            "default_mode": "core_primary"
        }
        
        return registry
    
    def get_recommended_persona(self, workspace: str, task_type: str = "general") -> Dict[str, Any]:
        """ワークスペースとタスクに基づく推奨ペルソナ"""
        recommendations = {
            "chat": {"primary": "code_chan", "alternatives": ["yurika", "haruka"]},
            "development": {"primary": "code_chan", "alternatives": ["ana", "misaki"]},
            "design": {"primary": "yurika", "alternatives": ["haruka", "code_chan"]},
            "analysis": {"primary": "ana", "alternatives": ["code_chan", "misaki"]},
            "music": {"primary": "haruka", "alternatives": ["yurika", "code_chan"]},
            "qa": {"primary": "misaki", "alternatives": ["code_chan", "ana"]},
            "ops": {"primary": "ren", "alternatives": ["code_chan", "misaki"]}
        }
        
        if workspace in recommendations:
            primary = recommendations[workspace]["primary"]
            return {
                "primary_persona": primary,
                "persona_data": self.core_team.get(primary, {}),
                "alternatives": recommendations[workspace]["alternatives"],
                "extended_available": True,
                "workspace": workspace
            }
        
        return {"primary_persona": "code_chan", "persona_data": self.core_team.get("code_chan", {})}
    
    def get_integration_status(self) -> Dict[str, Any]:
        """システム統合状況"""
        return {
            "system_type": "Hybrid Integration",
            "core_team_loaded": len(self.core_team) > 0,
            "extended_team_loaded": len(self.extended_team) > 0,
            "core_personas": list(self.core_team.keys()),
            "total_combinations": len(self.core_team) * 4,  # 6 personas × 4 vibrations
            "vibration_modes": list(self.vibration_models.keys()),
            "workspace_modes": list(self.workspace_modes.keys()),
            "integration_date": datetime.now().isoformat(),
            "ready_for_deployment": True
        }
    
    def export_integration_config(self, output_path: str = "config/hybrid_persona_config.yaml"):
        """統合設定をエクスポート"""
        integration_config = {
            "saijinos_hybrid_integration": {
                "meta": {
                    "version": "1.0.0",
                    "type": "hybrid_persona_system",
                    "created": datetime.now().isoformat(),
                    "core_personas": len(self.core_team),
                    "extended_personas": 57,
                    "total_combinations": len(self.core_team) * 4
                },
                "core_team": self.persona_registry["core_team"],
                "extended_team_available": True,
                "vibration_models": self.vibration_models,
                "workspace_modes": self.workspace_modes,
                "integration_strategy": "core_primary_extended_support"
            }
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(integration_config, f, default_flow_style=False, allow_unicode=True)
            print(f"✅ Integration config exported to: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False


def main():
    """ハイブリッド統合テスト実行"""
    print("🚀 SaijinOS ハイブリッドペルソナ統合システム テスト開始")
    print("=" * 60)
    
    # システム初期化
    integrator = PersonaSystemIntegrator()
    
    # 統合状況確認
    status = integrator.get_integration_status()
    print("📊 システム統合状況:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    print()
    
    # ワークスペース別推奨ペルソナテスト
    workspaces = ["chat", "development", "design", "analysis", "music"]
    print("🎯 ワークスペース別推奨ペルソナ:")
    for workspace in workspaces:
        recommendation = integrator.get_recommended_persona(workspace)
        print(f"  {workspace}: {recommendation['primary_persona']} (代替: {recommendation['alternatives']})")
    print()
    
    # 統合設定エクスポート
    print("💾 統合設定エクスポート:")
    export_success = integrator.export_integration_config()
    
    print("=" * 60)
    print("✅ ハイブリッド統合システム テスト完了")
    
    if export_success and status["ready_for_deployment"]:
        print("🎉 システム展開準備完了!")
    else:
        print("⚠️  追加設定が必要です")


if __name__ == "__main__":
    main()