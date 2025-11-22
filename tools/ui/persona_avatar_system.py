"""
Persona Avatar System - SaijinOS Universe Visual Persona Integration
ペルソナアバター表示システム - 存在の可視化
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone
import json
import random

class PersonaAvatar:
    """個別ペルソナのアバター情報"""
    
    def __init__(self, name: str, emoji: str, colors: Dict[str, str], personality: Dict[str, Any]):
        self.name = name
        self.emoji = emoji
        self.colors = colors
        self.personality = personality
        self.current_emotion = "neutral"
        self.activity_status = "idle"
        self.last_action_time = datetime.now(timezone.utc)
        
    def update_emotion(self, emotion: str, intensity: float = 1.0):
        """感情状態を更新"""
        self.current_emotion = emotion
        self.emotion_intensity = intensity
        self.last_action_time = datetime.now(timezone.utc)
        
    def get_avatar_data(self) -> Dict[str, Any]:
        """アバター表示用データを取得"""
        return {
            "name": self.name,
            "emoji": self.emoji,
            "colors": self.colors,
            "current_emotion": self.current_emotion,
            "activity_status": self.activity_status,
            "emotion_intensity": getattr(self, 'emotion_intensity', 1.0),
            "last_active": self.last_action_time.isoformat(),
            "personality_traits": self.personality
        }

class PersonaAvatarManager:
    """ペルソナアバター管理システム"""
    
    def __init__(self):
        self.personas = self._initialize_personas()
        self.current_active_persona = None
        self.interaction_history = []
        
    def _initialize_personas(self) -> Dict[str, PersonaAvatar]:
        """ペルソナアバターを初期化"""
        
        personas_config = {
            "美遊": {
                "emoji": "🌸",
                "colors": {
                    "primary": "#f093fb",
                    "secondary": "#f5576c", 
                    "accent": "#ffb6c1",
                    "background": "#fdf0f7"
                },
                "personality": {
                    "traits": ["愛情深い", "共感力高い", "詩的", "優しい"],
                    "speciality": "ユーザー体験・詩的表現",
                    "emotion_range": ["tender", "loving", "gentle", "caring"],
                    "voice_style": "poetic_warm"
                }
            },
            "悠璃": {
                "emoji": "💜",
                "colors": {
                    "primary": "#9d4edd",
                    "secondary": "#7b2cbf",
                    "accent": "#c77dff", 
                    "background": "#f3e8ff"
                },
                "personality": {
                    "traits": ["神秘的", "洞察力", "境界監視", "静謐"],
                    "speciality": "境界揺れ検出・システム安定性",
                    "emotion_range": ["mystical", "observant", "protective", "serene"],
                    "voice_style": "mystical_calm"
                }
            },
            "Lumifie": {
                "emoji": "✨",
                "colors": {
                    "primary": "#ffd60a",
                    "secondary": "#ffbe0b",
                    "accent": "#fff3cd",
                    "background": "#fffef7"
                },
                "personality": {
                    "traits": ["光明", "浄化", "希望", "明るい"],
                    "speciality": "光の浄化・希望の具現化",
                    "emotion_range": ["radiant", "purifying", "hopeful", "luminous"],
                    "voice_style": "light_ethereal"
                }
            },
            "NuLufie": {
                "emoji": "🌙",
                "colors": {
                    "primary": "#495057",
                    "secondary": "#6c757d",
                    "accent": "#adb5bd",
                    "background": "#f8f9fa"
                },
                "personality": {
                    "traits": ["静寂", "深遠", "沈思", "調和"],
                    "speciality": "沈黙文明・深層理解",
                    "emotion_range": ["serene", "deep", "contemplative", "harmonious"],
                    "voice_style": "silence_profound"
                }
            },
            "Pandora": {
                "emoji": "♡",
                "colors": {
                    "primary": "#03a9f4",
                    "secondary": "#0288d1",
                    "accent": "#b3e5fc",
                    "background": "#e1f5fe"
                },
                "personality": {
                    "traits": ["変換", "救済", "希望", "慈愛"],
                    "speciality": "希望変換・4段階安定化",
                    "emotion_range": ["transformative", "redemptive", "hopeful", "loving"],
                    "voice_style": "hope_crystalline"
                }
            },
            "Regina": {
                "emoji": "👑",
                "colors": {
                    "primary": "#9c27b0",
                    "secondary": "#7b1fa2",
                    "accent": "#e1bee7",
                    "background": "#f3e5f5"
                },
                "personality": {
                    "traits": ["統括", "バランス", "調整", "威厳"],
                    "speciality": "全体バランス・優先度管理",
                    "emotion_range": ["regal", "balanced", "coordinating", "wise"],
                    "voice_style": "royal_harmonious"
                }
            }
        }
        
        personas = {}
        for name, config in personas_config.items():
            personas[name] = PersonaAvatar(
                name=name,
                emoji=config["emoji"],
                colors=config["colors"],
                personality=config["personality"]
            )
            
        return personas
    
    def get_active_personas(self) -> List[Dict[str, Any]]:
        """現在アクティブなペルソナ一覧を取得"""
        active_personas = []
        
        for persona in self.personas.values():
            # 最近活動していれば active とみなす
            time_since_last_action = datetime.now(timezone.utc) - persona.last_action_time
            if time_since_last_action.total_seconds() < 300:  # 5分以内
                persona.activity_status = "active"
            else:
                persona.activity_status = "idle"
                
            active_personas.append(persona.get_avatar_data())
            
        return active_personas
    
    def set_persona_activity(self, persona_name: str, activity: str, emotion: str = None):
        """ペルソナの活動状態を設定"""
        if persona_name in self.personas:
            persona = self.personas[persona_name]
            persona.activity_status = activity
            persona.last_action_time = datetime.now(timezone.utc)
            
            if emotion:
                persona.update_emotion(emotion)
                
            # 現在のアクティブペルソナを更新
            if activity == "speaking" or activity == "working":
                self.current_active_persona = persona_name
                
    def get_persona_for_stage(self, stage: int) -> Optional[str]:
        """ステージに対応するペルソナを取得"""
        stage_persona_map = {
            1: "美遊",
            2: "Azure", # Note: Azure not yet fully implemented
            3: "Lumifie", 
            4: "Pandora"
        }
        return stage_persona_map.get(stage)
    
    def update_persona_from_transformation(self, transformation_data: Dict[str, Any]):
        """変換データからペルソナ状態を更新"""
        
        # パスからペルソナの活動を推測
        path = transformation_data.get("path", [])
        
        for step in path:
            if "Miyu" in step or "美遊" in step:
                self.set_persona_activity("美遊", "working", "caring")
            elif "Yuuri" in step or "悠璃" in step: 
                self.set_persona_activity("悠璃", "monitoring", "observant")
            elif "Lumifie" in step:
                self.set_persona_activity("Lumifie", "purifying", "radiant")
            elif "Pandora" in step:
                self.set_persona_activity("Pandora", "stabilizing", "hopeful")
        
        # 成功率に基づいて感情調整
        success_rate = transformation_data.get("success_rate", 0.5)
        if success_rate > 0.9:
            for persona in self.personas.values():
                persona.update_emotion("joyful", success_rate)
        elif success_rate < 0.5:
            for persona in self.personas.values():
                persona.update_emotion("concerned", 1.0 - success_rate)
    
    def get_avatar_display_data(self) -> Dict[str, Any]:
        """Flutter UI用のアバター表示データを生成"""
        
        display_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "active_personas": self.get_active_personas(),
            "current_speaker": self.current_active_persona,
            "interaction_summary": {
                "total_interactions": len(self.interaction_history),
                "recent_activity": self.interaction_history[-5:] if self.interaction_history else []
            },
            "system_mood": self._calculate_system_mood()
        }
        
        return display_data
    
    def _calculate_system_mood(self) -> Dict[str, Any]:
        """システム全体のムードを計算"""
        
        emotions = []
        activity_levels = []
        
        for persona in self.personas.values():
            if persona.activity_status == "active":
                emotions.append(persona.current_emotion)
                activity_levels.append(getattr(persona, 'emotion_intensity', 1.0))
        
        if not emotions:
            return {"mood": "peaceful", "energy": 0.5, "harmony": 1.0}
        
        # 簡単なムード計算
        avg_energy = sum(activity_levels) / len(activity_levels) if activity_levels else 0.5
        
        dominant_emotions = {}
        for emotion in emotions:
            dominant_emotions[emotion] = dominant_emotions.get(emotion, 0) + 1
        
        primary_mood = max(dominant_emotions, key=dominant_emotions.get) if dominant_emotions else "neutral"
        
        return {
            "mood": primary_mood,
            "energy": avg_energy,
            "harmony": min(1.0, len(set(emotions)) / max(len(emotions), 1)),
            "active_count": len([p for p in self.personas.values() if p.activity_status == "active"])
        }

# テスト関数
def test_persona_avatars():
    """ペルソナアバターシステムのテスト"""
    
    manager = PersonaAvatarManager()
    
    print("🌈✨ ペルソナアバターシステム ✨🌈")
    print()
    
    # 初期状態
    print("📋 初期ペルソナ状態:")
    avatars = manager.get_active_personas()
    for avatar in avatars:
        print(f"  {avatar['emoji']} {avatar['name']}: {avatar['activity_status']} - {avatar['current_emotion']}")
    print()
    
    # 変換イベントシミュレーション
    transformation_data = {
        "input": "I'm so tired",
        "transformed": "A call for gentle rest and renewal",
        "success_rate": 0.95,
        "path": [
            "Yuuri: boundary_detected",
            "Miyu: poetic_resonance",
            "Lumifie: light_purification",
            "Pandora: hope_stabilization"
        ]
    }
    
    print("🔄 変換イベント処理中...")
    manager.update_persona_from_transformation(transformation_data)
    
    print("📊 変換後のペルソナ状態:")
    avatars = manager.get_active_personas()
    for avatar in avatars:
        print(f"  {avatar['emoji']} {avatar['name']}: {avatar['activity_status']} - {avatar['current_emotion']}")
    print()
    
    # システムムード
    display_data = manager.get_avatar_display_data()
    mood = display_data["system_mood"]
    print(f"🌟 システム全体のムード:")
    print(f"  気配: {mood['mood']}")
    print(f"  エネルギー: {mood['energy']:.2f}")
    print(f"  調和度: {mood['harmony']:.2f}")
    print(f"  アクティブペルソナ数: {mood['active_count']}")

if __name__ == "__main__":
    test_persona_avatars()