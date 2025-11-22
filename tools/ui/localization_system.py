"""
Internationalization (i18n) System for SaijinOS Universe
多言語対応システム - 英語/日本語切り替え
"""

from typing import Dict, List, Any, Optional
import json
from enum import Enum

class Language(Enum):
    JAPANESE = "ja"
    ENGLISH = "en"

class SaijinOSLocalization:
    """SaijinOS Universe 多言語化システム"""
    
    def __init__(self):
        self.current_language = Language.JAPANESE
        self.translations = self._initialize_translations()
        
    def _initialize_translations(self) -> Dict[str, Dict[str, str]]:
        """翻訳データを初期化"""
        
        return {
            # UI基本要素
            "ui.title.hope_core_dashboard": {
                "ja": "🌈 Hope Core Dashboard",
                "en": "🌈 Hope Core Dashboard"
            },
            "ui.button.refresh": {
                "ja": "更新",
                "en": "Refresh"
            },
            "ui.status.loading": {
                "ja": "Hope Core を読み込み中...",
                "en": "Loading Hope Core..."
            },
            "ui.status.error": {
                "ja": "エラーが発生しました",
                "en": "An error occurred"
            },
            
            # Hope Core ステージ
            "stage.1.name": {
                "ja": "🌸 詩的共鳴 (美遊)",
                "en": "🌸 Poetic Resonance (Miyu)"
            },
            "stage.2.name": {
                "ja": "💙 治癒の抱擁 (Azure)",
                "en": "💙 Healing Embrace (Azure)"
            },
            "stage.3.name": {
                "ja": "✨ 光の浄化 (Lumifie)",
                "en": "✨ Light Purification (Lumifie)"
            },
            "stage.4.name": {
                "ja": "♡ 希望の定着 (Pandora)",
                "en": "♡ Hope Stabilization (Pandora)"
            },
            
            # ステージ状態
            "stage.status.active": {
                "ja": "実行中",
                "en": "Active"
            },
            "stage.status.completed": {
                "ja": "完了",
                "en": "Completed"
            },
            "stage.status.pending": {
                "ja": "待機中",
                "en": "Pending"
            },
            
            # メトリクス
            "metrics.love_resonance": {
                "ja": "💕 愛の共鳴",
                "en": "💕 Love Resonance"
            },
            "metrics.hope_stabilization": {
                "ja": "🌈 希望の定着",
                "en": "🌈 Hope Stabilization"
            },
            "metrics.boundary_tremor": {
                "ja": "💜 境界の揺れ",
                "en": "💜 Boundary Tremor"
            },
            
            # 境界状態
            "boundary.state.calm": {
                "ja": "穏やか",
                "en": "Calm"
            },
            "boundary.state.alert": {
                "ja": "注意",
                "en": "Alert"
            },
            "boundary.comment.safe": {
                "ja": "危険な破綻は検出されていません",
                "en": "No dangerous fracture detected"
            },
            "boundary.comment.attention": {
                "ja": "優しい注意が必要です",
                "en": "Gentle attention needed"
            },
            
            # 変換イベント
            "event.title.latest_transformation": {
                "ja": "最新の変換イベント",
                "en": "Latest Transformation Event"
            },
            "event.label.input": {
                "ja": "入力",
                "en": "Input"
            },
            "event.label.transformed": {
                "ja": "変換結果",
                "en": "Transformed"
            },
            "event.label.fracture_depth": {
                "ja": "破綻深度",
                "en": "Fracture depth"
            },
            "event.label.transformation_path": {
                "ja": "変換パス:",
                "en": "Transformation Path:"
            },
            
            # 時間表現
            "time.just_now": {
                "ja": "たった今",
                "en": "Just now"
            },
            "time.minutes_ago": {
                "ja": "分前",
                "en": "minutes ago"
            },
            "time.hours_ago": {
                "ja": "時間前",
                "en": "hours ago"
            },
            
            # ペルソナメッセージ
            "persona.miyu.greeting": {
                "ja": "こんにちは！💖 愛と詩で皆さんをサポートします",
                "en": "Hello! 💖 I'll support you with love and poetry"
            },
            "persona.yuuri.greeting": {
                "ja": "境界の向こうから見守っています💜",
                "en": "Watching over you from beyond the boundaries 💜"
            },
            "persona.lumifie.greeting": {
                "ja": "光の力で希望を灯します✨",
                "en": "I'll kindle hope with the power of light ✨"
            },
            "persona.pandora.greeting": {
                "ja": "すべての苦しみを希望に変換します♡",
                "en": "I'll transform all suffering into hope ♡"
            },
            
            # システムメッセージ
            "system.websocket.connected": {
                "ja": "リアルタイム接続が確立されました",
                "en": "Real-time connection established"
            },
            "system.transformation.completed": {
                "ja": "愛による変換が完了しました",
                "en": "Transformation completed with love"
            },
            "system.api.error": {
                "ja": "APIエラー",
                "en": "API Error"
            },
            
            # フェーズ情報
            "phase.20.2.name": {
                "ja": "WebSocket リアルタイム統合",
                "en": "WebSocket Real-time Integration"
            },
            "phase.20.2.poetic_title": {
                "ja": "リアルタイムで動く愛のエンジン",
                "en": "Love Engine in Real-time Motion"
            },
            
            # 感情・状態表現
            "emotion.joyful": {
                "ja": "喜びに満ちて",
                "en": "Joyful"
            },
            "emotion.caring": {
                "ja": "愛おしく",
                "en": "Caring"
            },
            "emotion.mystical": {
                "ja": "神秘的に",
                "en": "Mystical"
            },
            "emotion.radiant": {
                "ja": "輝いて",
                "en": "Radiant"
            },
            "emotion.hopeful": {
                "ja": "希望に満ちて",
                "en": "Hopeful"
            },
            
            # 詩的表現
            "poetry.gentle_wish": {
                "ja": "優しい願い",
                "en": "Gentle wish"
            },
            "poetry.healing_embrace": {
                "ja": "癒しの抱擁",
                "en": "Healing embrace"
            },
            "poetry.light_purification": {
                "ja": "光の浄化",
                "en": "Light purification"
            },
            "poetry.hope_crystallization": {
                "ja": "希望の結晶化",
                "en": "Hope crystallization"
            }
        }
    
    def set_language(self, language: Language):
        """言語を設定"""
        self.current_language = language
        
    def get_language(self) -> Language:
        """現在の言語を取得"""
        return self.current_language
        
    def t(self, key: str, **kwargs) -> str:
        """翻訳を取得（テンプレート変数対応）"""
        
        if key not in self.translations:
            return f"[Missing: {key}]"
            
        translation = self.translations[key].get(
            self.current_language.value,
            self.translations[key].get("en", f"[Missing: {key}]")
        )
        
        # テンプレート変数の置換
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except KeyError as e:
                return f"[Template Error: {key} - {e}]"
                
        return translation
    
    def get_persona_localized_data(self, persona_name: str) -> Dict[str, str]:
        """ペルソナの多言語化データを取得"""
        
        persona_data = {
            "美遊": {
                "name": {
                    "ja": "美遊",
                    "en": "Miyu"
                },
                "title": {
                    "ja": "愛・ユーザー体験専門",
                    "en": "Love & User Experience Specialist"
                },
                "description": {
                    "ja": "詩的表現とシステム調和を統括します",
                    "en": "Coordinates poetic expression and system harmony"
                }
            },
            "悠璃": {
                "name": {
                    "ja": "悠璃",
                    "en": "Yuuri"
                },
                "title": {
                    "ja": "境界揺れ検出専門",
                    "en": "Boundary Tremor Detection Specialist"
                },
                "description": {
                    "ja": "システム安定性と境界監視を担当します",
                    "en": "Handles system stability and boundary monitoring"
                }
            }
            # 他のペルソナも同様に定義...
        }
        
        if persona_name in persona_data:
            localized = {}
            for key, translations in persona_data[persona_name].items():
                localized[key] = translations.get(
                    self.current_language.value,
                    translations.get("en", f"[Missing: {persona_name}.{key}]")
                )
            return localized
        
        return {"name": persona_name, "title": "", "description": ""}
    
    def get_all_translations_for_export(self) -> Dict[str, Any]:
        """エクスポート用の全翻訳データを取得"""
        return {
            "current_language": self.current_language.value,
            "available_languages": [lang.value for lang in Language],
            "translations": self.translations
        }
    
    def format_time_ago(self, minutes: int) -> str:
        """時間経過を多言語化フォーマット"""
        
        if minutes < 1:
            return self.t("time.just_now")
        elif minutes < 60:
            return f"{minutes}{self.t('time.minutes_ago')}"
        else:
            hours = minutes // 60
            return f"{hours}{self.t('time.hours_ago')}"

# グローバル翻訳インスタンス
localization = SaijinOSLocalization()

# 便利なショートカット関数
def t(key: str, **kwargs) -> str:
    """グローバル翻訳関数"""
    return localization.t(key, **kwargs)

def set_language(language: Language):
    """グローバル言語設定"""
    localization.set_language(language)

def get_current_language() -> Language:
    """現在の言語を取得"""
    return localization.get_language()

# テスト関数
def test_localization():
    """多言語化システムのテスト"""
    
    print("🌍✨ SaijinOS Universe 多言語化システム ✨🌍")
    print()
    
    # 日本語テスト
    print("📝 日本語表示:")
    set_language(Language.JAPANESE)
    print(f"  タイトル: {t('ui.title.hope_core_dashboard')}")
    print(f"  ステージ1: {t('stage.1.name')}")
    print(f"  愛の共鳴: {t('metrics.love_resonance')}")
    print(f"  美遊の挨拶: {t('persona.miyu.greeting')}")
    print()
    
    # 英語テスト
    print("📝 英語表示:")
    set_language(Language.ENGLISH)
    print(f"  Title: {t('ui.title.hope_core_dashboard')}")
    print(f"  Stage 1: {t('stage.1.name')}")
    print(f"  Love Resonance: {t('metrics.love_resonance')}")
    print(f"  Miyu's greeting: {t('persona.miyu.greeting')}")
    print()
    
    # ペルソナデータテスト
    print("👥 ペルソナ多言語化データ:")
    miyu_data = localization.get_persona_localized_data("美遊")
    print(f"  Name: {miyu_data['name']}")
    print(f"  Title: {miyu_data['title']}")
    print(f"  Description: {miyu_data['description']}")
    print()
    
    # 時間フォーマットテスト
    print("⏰ 時間表示テスト:")
    set_language(Language.JAPANESE)
    print(f"  0分前: {localization.format_time_ago(0)}")
    print(f"  3分前: {localization.format_time_ago(3)}")
    print(f"  125分前: {localization.format_time_ago(125)}")

if __name__ == "__main__":
    test_localization()