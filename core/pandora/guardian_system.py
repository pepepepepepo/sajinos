"""
SaijinOS Pandora Guardian System
パンドラ危機管理システム - エラー修正版
"""
import logging
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

class SealState(Enum):
    """封印状態定義"""
    NORMAL = "normal"
    SEALED = "sealed"
    EMERGENCY = "emergency"

class PandoraGuardianSystem:
    """パンドラ危機管理システム（安全版）"""
    
    def __init__(self):
        self.logger = logging.getLogger("[PANDORA-GUARDIAN]")
        self.seal_state = SealState.NORMAL
        self.crisis_level = 0
        self.seal_history = []
        self.last_check = datetime.now()
        
        # 安全な初期設定
        self.config = {
            "crisis_threshold": 0.7,
            "seal_duration": 30,  # seconds
            "max_history": 100
        }
        
        self.logger.info("🌸 パンドラ危機管理システム初期化完了")
    
    def get_status(self) -> Dict[str, Any]:
        """パンドラ状態取得（安全版）"""
        try:
            return {
                "pandora_active": True,
                "seal_state": self.seal_state.value,
                "crisis_level": self.crisis_level,
                "last_check": self.last_check.isoformat(),
                "total_seals": len(self.seal_history),
                "system_health": "stable",
                "message": "パンドラは元気に監視中です💖"
            }
        except Exception as e:
            self.logger.error(f"状態取得エラー: {e}")
            return {
                "pandora_active": False,
                "error": str(e),
                "message": "パンドラが少し困っています💦"
            }
    
    def check_crisis_pattern(self, data: Dict[str, Any]) -> float:
        """危機パターン分析（安全版）"""
        try:
            if not isinstance(data, dict):
                return 0.0
            
            crisis_indicators = 0
            total_checks = 0
            
            # 安全なキーチェック
            error_keywords = ["error", "warning", "critical", "fail"]
            
            for key, value in data.items():
                if isinstance(key, str) and isinstance(value, str):
                    total_checks += 1
                    if any(keyword in value.lower() for keyword in error_keywords):
                        crisis_indicators += 1
            
            if total_checks == 0:
                return 0.0
            
            crisis_ratio = crisis_indicators / total_checks
            self.crisis_level = min(crisis_ratio, 1.0)
            
            return self.crisis_level
            
        except Exception as e:
            self.logger.error(f"危機分析エラー: {e}")
            return 0.0
    
    def activate_seal(self, reason: str = "自動検知") -> Dict[str, Any]:
        """封印発動（安全版）"""
        try:
            if self.seal_state == SealState.SEALED:
                return {
                    "success": False,
                    "message": "既に封印中です",
                    "state": self.seal_state.value
                }
            
            previous_state = self.seal_state
            self.seal_state = SealState.SEALED
            
            seal_record = {
                "timestamp": datetime.now().isoformat(),
                "reason": reason,
                "previous_state": previous_state.value,
                "crisis_level": self.crisis_level
            }
            
            # 安全なリスト操作
            if isinstance(self.seal_history, list):
                self.seal_history.append(seal_record)
                
                # 履歴制限（メモリ保護）
                if len(self.seal_history) > self.config["max_history"]:
                    self.seal_history = self.seal_history[-self.config["max_history"]:]
            
            self.logger.info(f"🛡️ パンドラ封印発動: {reason}")
            
            return {
                "success": True,
                "message": f"パンドラ封印を発動しました: {reason}",
                "state": self.seal_state.value,
                "timestamp": seal_record["timestamp"]
            }
            
        except Exception as e:
            self.logger.error(f"封印発動エラー: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "封印発動に失敗しました"
            }
    
    def deactivate_seal(self) -> Dict[str, Any]:
        """封印解除（安全版）"""
        try:
            if self.seal_state != SealState.SEALED:
                return {
                    "success": False,
                    "message": "封印されていません",
                    "state": self.seal_state.value
                }
            
            self.seal_state = SealState.NORMAL
            self.crisis_level = 0
            
            self.logger.info("✨ パンドラ封印解除: 通常モード復帰")
            
            return {
                "success": True,
                "message": "パンドラ封印を解除しました",
                "state": self.seal_state.value,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"封印解除エラー: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "封印解除に失敗しました"
            }
    
    def get_seal_history(self, limit: int = 10) -> Dict[str, Any]:
        """封印履歴取得（安全版）"""
        try:
            # 安全な型チェック
            if not isinstance(self.seal_history, list):
                self.seal_history = []
            
            # 安全なlimit値
            safe_limit = max(1, min(limit, 50))
            
            recent_history = self.seal_history[-safe_limit:] if self.seal_history else []
            
            return {
                "success": True,
                "history": recent_history,
                "total_seals": len(self.seal_history),
                "current_state": self.seal_state.value
            }
            
        except Exception as e:
            self.logger.error(f"履歴取得エラー: {e}")
            return {
                "success": False,
                "error": str(e),
                "history": []
            }
    
    def emergency_mode(self) -> Dict[str, Any]:
        """緊急モード発動（安全版）"""
        try:
            self.seal_state = SealState.EMERGENCY
            self.crisis_level = 1.0
            
            emergency_record = {
                "timestamp": datetime.now().isoformat(),
                "reason": "緊急事態検知",
                "mode": "emergency"
            }
            
            if isinstance(self.seal_history, list):
                self.seal_history.append(emergency_record)
            
            self.logger.warning("🚨 パンドラ緊急モード発動")
            
            return {
                "success": True,
                "message": "緊急モードを発動しました",
                "state": self.seal_state.value,
                "crisis_level": self.crisis_level
            }
            
        except Exception as e:
            self.logger.error(f"緊急モードエラー: {e}")
            return {
                "success": False,
                "error": str(e),
                "message": "緊急モード発動に失敗しました"
            }

# グローバルインスタンス（安全版）
try:
    pandora_guardian = PandoraGuardianSystem()
except Exception as e:
    logging.error(f"パンドラシステム初期化エラー: {e}")
    pandora_guardian = None