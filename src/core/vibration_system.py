# -*- coding: utf-8 -*-
"""
4振動システム管理
語温灯・構造灯・娘っ子灯・AUTO
"""

from typing import Dict, List, Any

class VibrationSystem:
    """4振動システム管理"""
    
    def __init__(self):
        self.vibration_modes = {
            "goonro": {
                "label": "🌸語温灯",
                "model": "tinyllama",
                "description": "温かく優しい対話スタイル",
                "characteristics": ["温かい", "包容力", "優しい", "共感的"],
                "status": "active"
            },
            "structure": {
                "label": "🔧構造灯",
                "model": "qwen",
                "description": "論理的で構造化された思考",
                "characteristics": ["論理的", "体系的", "明確", "分析的"],
                "status": "active"
            },
            "musumekko": {
                "label": "💫娘っ子灯",
                "model": "rinna",
                "description": "親しみやすく活発なスタイル",
                "characteristics": ["親しみやすい", "活発", "創造的", "表現豊か"],
                "status": "active"
            },
            "auto": {
                "label": "🔄AUTO",
                "model": "deepseek",
                "description": "状況に応じた自動最適化",
                "characteristics": ["適応的", "効率的", "最適化", "自動調整"],
                "status": "active"
            }
        }
    
    def get_vibration_modes(self) -> Dict[str, Any]:
        """振動モード一覧取得"""
        return self.vibration_modes
    
    def get_vibration_mode(self, mode: str) -> Dict[str, Any]:
        """特定の振動モード取得"""
        return self.vibration_modes.get(mode, {})
    
    def get_model_for_vibration(self, mode: str) -> str:
        """振動モードに対応するAIモデル取得"""
        vibration = self.vibration_modes.get(mode, {})
        return vibration.get("model", "deepseek")
    
    def is_valid_vibration(self, mode: str) -> bool:
        """振動モードの妥当性確認"""
        return mode in self.vibration_modes
    
    def get_active_vibrations(self) -> List[str]:
        """アクティブな振動モード一覧"""
        return [mode for mode, config in self.vibration_modes.items() 
                if config.get("status") == "active"]