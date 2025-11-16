# -*- coding: utf-8 -*-
"""
SaijinOS スマートVRAM管理システム
4振動システム × VRAM最適化 × 自動切り替え

メンタル削られるVRAM OOMを根絶！😇
"""

import torch
import psutil
import time
import json
from typing import Dict, List, Optional, Any
from datetime import datetime

try:
    import nvidia_ml_py3 as nvml
    NVML_AVAILABLE = True
except ImportError:
    NVML_AVAILABLE = False
    print("Warning: nvidia-ml-py3 not available. VRAM monitoring disabled.")

class SaijinOSSmartVRAMManager:
    """SaijinOS スマートVRAM管理システム"""
    
    def __init__(self):
        self.nvml_available = NVML_AVAILABLE
        if self.nvml_available:
            nvml.nvmlInit()
            self.handle = nvml.nvmlDeviceGetHandleByIndex(0)
        
        # 4振動システムのVRAM要件定義
        self.vibration_requirements = {
            "goonro": {
                "name": "🌸語温灯",
                "model": "TinyLlama",
                "vram_gb": 2.5,
                "context_limit": 1024,
                "priority": 1,  # 最優先（常時起動）
                "description": "軽量・高速・温かい対話"
            },
            "musumekko": {
                "name": "💫娘っ子灯", 
                "model": "Rinna 3.6B",
                "vram_gb": 4.0,
                "context_limit": 1536,
                "priority": 2,
                "description": "親しみやすい・創造的・表現豊か"
            },
            "structure": {
                "name": "🔧構造灯",
                "model": "Qwen 7B", 
                "vram_gb": 6.5,
                "context_limit": 2048,
                "priority": 3,
                "description": "論理的・体系的・分析的"
            },
            "auto": {
                "name": "🔄AUTO",
                "model": "DeepSeek 6.7B",
                "vram_gb": 8.0,
                "context_limit": 2048,
                "priority": 4,
                "description": "高性能・適応的・自動最適化"
            }
        }
        
        self.loaded_models = {}
        self.vram_history = []
        
    def get_vram_status(self) -> Dict[str, Any]:
        """VRAM使用状況取得"""
        if not self.nvml_available:
            return {
                "total": 12.0,  # RTX 4070 Ti仮定
                "used": 2.0,    # 推定値
                "free": 10.0,   # 推定値
                "utilization": 16.7,
                "status": "monitoring_unavailable"
            }
        
        try:
            info = nvml.nvmlDeviceGetMemoryInfo(self.handle)
            status = {
                "total": round(info.total / 1024**3, 2),
                "used": round(info.used / 1024**3, 2),
                "free": round(info.free / 1024**3, 2),
                "utilization": round(info.used / info.total * 100, 1),
                "status": "active",
                "timestamp": datetime.now().isoformat()
            }
            
            # 履歴記録（最新50件）
            self.vram_history.append(status)
            if len(self.vram_history) > 50:
                self.vram_history.pop(0)
                
            return status
        except Exception as e:
            return {
                "total": 0, "used": 0, "free": 0, "utilization": 0,
                "status": f"error: {str(e)}"
            }
    
    def analyze_vibration_capacity(self) -> Dict[str, Any]:
        """振動モード別キャパシティ分析"""
        vram = self.get_vram_status()
        free_gb = vram["free"]
        
        analysis = {
            "vram_status": vram,
            "available_vibrations": [],
            "unavailable_vibrations": [],
            "recommended_strategy": "",
            "warning_level": "normal"
        }
        
        # Windows側のVRAM食いを考慮（実効VRAM = 表示VRAM - 1GB）
        effective_free = max(0, free_gb - 1.0)
        
        for vibration, config in self.vibration_requirements.items():
            required = config["vram_gb"]
            
            if effective_free >= required:
                analysis["available_vibrations"].append({
                    "vibration": vibration,
                    "name": config["name"],
                    "required_gb": required,
                    "priority": config["priority"]
                })
            else:
                analysis["unavailable_vibrations"].append({
                    "vibration": vibration,
                    "name": config["name"], 
                    "required_gb": required,
                    "shortage_gb": round(required - effective_free, 2)
                })
        
        # 推奨戦略決定
        analysis["recommended_strategy"] = self._determine_strategy(effective_free)
        analysis["warning_level"] = self._determine_warning_level(vram["utilization"])
        
        return analysis
    
    def _determine_strategy(self, free_gb: float) -> str:
        """使用可能VRAM based戦略決定"""
        if free_gb >= 10:
            return "🚀 Full Performance: All vibrations available"
        elif free_gb >= 8:
            return "⚡ High Performance: Skip AUTO, use Structure + others"
        elif free_gb >= 6:
            return "🎯 Balanced: Structure + Musumekko + Goonro"
        elif free_gb >= 4:
            return "💫 Creative: Musumekko + Goonro only"
        elif free_gb >= 2:
            return "🌸 Safe Mode: Goonro only (TinyLlama)"
        else:
            return "⚠️ Critical: Consider freeing VRAM or restart"
    
    def _determine_warning_level(self, utilization: float) -> str:
        """警告レベル判定"""
        if utilization >= 90:
            return "critical"
        elif utilization >= 80:
            return "warning"
        elif utilization >= 70:
            return "caution"
        else:
            return "normal"
    
    def get_optimal_vibration_sequence(self) -> List[str]:
        """最適な振動モード起動順序"""
        capacity = self.analyze_vibration_capacity()
        available = capacity["available_vibrations"]
        
        # 優先度順にソート
        available.sort(key=lambda x: x["priority"])
        
        return [v["vibration"] for v in available]
    
    def simulate_model_loading(self, vibration_mode: str) -> Dict[str, Any]:
        """モデル読み込みシミュレーション（OOM回避チェック）"""
        if vibration_mode not in self.vibration_requirements:
            return {"success": False, "error": "Unknown vibration mode"}
        
        config = self.vibration_requirements[vibration_mode]
        vram = self.get_vram_status()
        
        # Windows側VRAM使用量を考慮
        effective_free = max(0, vram["free"] - 1.0)
        required = config["vram_gb"]
        
        simulation = {
            "vibration": vibration_mode,
            "name": config["name"],
            "required_gb": required,
            "available_gb": effective_free,
            "success": effective_free >= required,
            "safety_margin": round(effective_free - required, 2),
            "recommended_settings": {}
        }
        
        if simulation["success"]:
            # 成功時の推奨設定
            simulation["recommended_settings"] = {
                "max_model_len": config["context_limit"],
                "gpu_memory_utilization": min(0.85, (required / vram["total"]) + 0.1),
                "max_num_seqs": max(1, int(effective_free / required)),
                "dtype": "float16"
            }
        else:
            # 失敗時の代替案
            simulation["alternatives"] = self._suggest_alternatives(vibration_mode, effective_free)
        
        return simulation
    
    def _suggest_alternatives(self, failed_vibration: str, available_gb: float) -> List[str]:
        """代替振動モード提案"""
        alternatives = []
        
        for vibration, config in self.vibration_requirements.items():
            if vibration != failed_vibration and config["vram_gb"] <= available_gb:
                alternatives.append(vibration)
        
        return sorted(alternatives, key=lambda x: self.vibration_requirements[x]["priority"])
    
    def get_vram_health_report(self) -> Dict[str, Any]:
        """VRAM健康状態レポート"""
        if len(self.vram_history) < 2:
            return {"status": "insufficient_data"}
        
        recent = self.vram_history[-10:]  # 最新10件
        avg_utilization = sum(h["utilization"] for h in recent) / len(recent)
        
        return {
            "average_utilization": round(avg_utilization, 1),
            "peak_utilization": max(h["utilization"] for h in recent),
            "stability": "stable" if max(h["utilization"] for h in recent) - min(h["utilization"] for h in recent) < 10 else "unstable",
            "trend": "increasing" if recent[-1]["utilization"] > recent[0]["utilization"] else "stable",
            "health_score": max(0, 100 - avg_utilization),
            "recommendations": self._generate_health_recommendations(avg_utilization)
        }
    
    def _generate_health_recommendations(self, avg_util: float) -> List[str]:
        """健康状態 based 推奨事項"""
        recommendations = []
        
        if avg_util > 85:
            recommendations.append("⚠️ Consider reducing context length")
            recommendations.append("🔄 Switch to lighter vibration modes")
            recommendations.append("💾 Close unnecessary applications")
        elif avg_util > 70:
            recommendations.append("⚡ Monitor for memory leaks") 
            recommendations.append("🎯 Consider model rotation strategy")
        else:
            recommendations.append("✅ VRAM usage is healthy")
            recommendations.append("🚀 Room for additional models")
        
        return recommendations

def main():
    """SaijinOS VRAM管理システムテスト"""
    print("🚀 SaijinOS スマートVRAM管理システム")
    print("=" * 60)
    
    vram_manager = SaijinOSSmartVRAMManager()
    
    # VRAM状況分析
    print("📊 VRAM状況分析:")
    capacity = vram_manager.analyze_vibration_capacity()
    print(f"  Total VRAM: {capacity['vram_status']['total']}GB")
    print(f"  Free VRAM: {capacity['vram_status']['free']}GB")
    print(f"  Strategy: {capacity['recommended_strategy']}")
    print()
    
    # 利用可能振動モード
    print("✅ 利用可能振動モード:")
    for vib in capacity["available_vibrations"]:
        print(f"  {vib['name']} - {vib['required_gb']}GB")
    print()
    
    # 推奨起動順序
    print("🎯 推奨起動順序:")
    sequence = vram_manager.get_optimal_vibration_sequence()
    for i, vib in enumerate(sequence, 1):
        config = vram_manager.vibration_requirements[vib]
        print(f"  {i}. {config['name']} ({config['model']})")
    print()
    
    # モデル読み込みシミュレーション
    print("🧪 モデル読み込みシミュレーション:")
    for vibration in ["goonro", "structure", "auto"]:
        sim = vram_manager.simulate_model_loading(vibration)
        status = "✅ OK" if sim["success"] else "❌ OOM Risk"
        print(f"  {vram_manager.vibration_requirements[vibration]['name']}: {status}")
        if sim["success"]:
            settings = sim["recommended_settings"]
            print(f"    → Context: {settings['max_model_len']}, Memory: {settings['gpu_memory_utilization']:.2f}")
    
    print("=" * 60)
    print("✅ VRAM OOM地獄からの解放完了！😇")

if __name__ == "__main__":
    main()