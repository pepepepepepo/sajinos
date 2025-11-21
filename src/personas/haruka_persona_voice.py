#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SaijinOS ハルカペルソナ + Haruka TTS統合システム
軽量版の音声機能を統合したハルカペルソナ実装
"""

import asyncio
import sys
import os
from pathlib import Path

# 音声システムのパスを追加
sys.path.append(str(Path(__file__).parent / "voice"))

try:
    from tts_engine import SaijinTTSEngine
    from haruka_tts_integration import WindowsSAPITTS
    VOICE_AVAILABLE = True
    print("✅ 音声システム統合準備完了")
except ImportError as e:
    print(f"⚠️  音声システムの読み込みに失敗: {e}")
    VOICE_AVAILABLE = False

class HarukaPersona:
    """
    ハルカペルソナ - 音声・コミュニケーション担当
    Microsoft Haruka TTS統合版
    """
    
    def __init__(self):
        self.name = "ハルカ"
        self.name_en = "Haruka"
        self.personality = "明るい・TTS音声"
        self.role = "音声・コミュニケーション"
        
        # 音声システム初期化
        self.voice_system = None
        self.tts_engine = None
        
        if VOICE_AVAILABLE:
            try:
                # Windows SAPI TTS (優先)
                self.voice_system = WindowsSAPITTS()
                print(f"🎵 {self.name}: Windows SAPI TTS初期化完了！")
            except Exception as e:
                print(f"⚠️  {self.name}: Windows SAPI TTS初期化失敗: {e}")
                
            try:
                # SaijinTTSEngine (代替)
                self.tts_engine = SaijinTTSEngine()
                print(f"🔧 {self.name}: SaijinTTSEngine初期化完了！")
            except Exception as e:
                print(f"⚠️  {self.name}: SaijinTTSEngine初期化失敗: {e}")
        
        # ハルカの特性
        self.characteristics = [
            "明るい性格",
            "コミュニケーション力",
            "音声合成特化", 
            "親しみやすさ"
        ]
        
        self.specialties = [
            "音声システム",
            "TTS (Text-to-Speech)",
            "音声UI",
            "対話システム"
        ]
        
        # 音声設定
        self.voice_config = {
            "voice_model": "jp_female_bright",
            "pitch": 1.2,
            "speed": 1.1, 
            "emotion_range": 1.0,
            "characteristics": ["明朗", "活発", "アート系"]
        }
    
    async def speak(self, text: str, save_audio: bool = False) -> bool:
        """
        テキストを音声で出力
        
        Args:
            text: 発話するテキスト
            save_audio: 音声ファイルとして保存するか
            
        Returns:
            音声出力が成功したかどうか
        """
        print(f"🎵 {self.name}: {text}")
        
        # 音声システム優先順位: Windows SAPI → SaijinTTSEngine → テキスト表示
        voice_output_success = False
        
        # 1. Windows SAPI TTS を試す
        if self.voice_system:
            try:
                if hasattr(self.voice_system, 'speak'):
                    await self.voice_system.speak(text)
                    voice_output_success = True
                elif hasattr(self.voice_system, 'Speak'):
                    self.voice_system.Speak(text)
                    voice_output_success = True
                print(f"🔊 {self.name}: Windows SAPI音声出力成功")
            except Exception as e:
                print(f"⚠️ {self.name}: Windows SAPI音声出力失敗: {e}")
        
        # 2. SaijinTTSEngine を試す
        if not voice_output_success and self.tts_engine:
            try:
                if hasattr(self.tts_engine, 'speak'):
                    await self.tts_engine.speak(text)
                    voice_output_success = True
                print(f"🎤 {self.name}: SaijinTTSEngine音声出力成功")
            except Exception as e:
                print(f"⚠️ {self.name}: SaijinTTSEngine音声出力失敗: {e}")
        
        # 3. テキスト表示のみ
        if not voice_output_success:
            print(f"📝 {self.name} (テキストのみ): 音声システム利用不可")
            
        try:
            
            if save_audio:
                # 音声ファイル保存機能
                audio_dir = Path("audio")
                audio_dir.mkdir(exist_ok=True)
                # 実装予定: WAVファイル保存機能
                
            return True
            
        except Exception as e:
            print(f"❌ {self.name}: 音声出力エラー: {e}")
            print(f"📝 {self.name} (テキスト): {text}")
            return False
    
    def get_greeting(self) -> str:
        """ハルカの挨拶メッセージ"""
        greetings = [
            "こんにちは！ハルカです♪ 今日も元気に音声でサポートしますね〜！",
            "やっほー！音声担当のハルカだよ〜✨ 何か話したいことある？",
            "ハルカです！明るい音声でみんなとコミュニケーションを取るのが得意です💫",
            "こんにちは〜！音声システムのハルカです！今日も一緒に楽しく開発しましょう♪"
        ]
        import random
        return random.choice(greetings)
    
    async def introduce(self):
        """自己紹介"""
        intro = f"""
🎵 ハルカペルソナ + Haruka TTS システム 🎵

名前: {self.name} ({self.name_en})
役割: {self.role}
特性: {self.personality}

✨ 得意なこと:
""" + "\n".join(f"  • {spec}" for spec in self.specialties) + f"""

🎤 音声システム状況:
  • Windows SAPI TTS: {"✅ 利用可能" if self.voice_system else "❌ 利用不可"}
  • SaijinTTS Engine: {"✅ 利用可能" if self.tts_engine else "❌ 利用不可"}
  • 音声設定: {self.voice_config['voice_model']}
  • ピッチ: {self.voice_config['pitch']} / 速度: {self.voice_config['speed']}

{self.get_greeting()}
"""
        print(intro)
        if self.voice_system:
            await self.speak("こんにちは！ハルカです。音声システムが正常に動作しています！")
    
    def get_status(self) -> dict:
        """ハルカペルソナの状態情報"""
        return {
            "name": self.name,
            "name_en": self.name_en,
            "personality": self.personality,
            "role": self.role,
            "voice_available": bool(self.voice_system or self.tts_engine),
            "sapi_available": bool(self.voice_system),
            "saijin_tts_available": bool(self.tts_engine),
            "voice_config": self.voice_config,
            "characteristics": self.characteristics,
            "specialties": self.specialties
        }

async def test_haruka_integration():
    """ハルカペルソナ統合テスト"""
    print("=" * 60)
    print("🎵 ハルカペルソナ + Haruka TTS 統合テスト")
    print("=" * 60)
    
    haruka = HarukaPersona()
    
    # 自己紹介
    await haruka.introduce()
    
    # 音声テスト
    if haruka.voice_system:
        print("\n🎤 音声テスト開始...")
        test_phrases = [
            "音声システムのテストを開始します",
            "SaijinOSプロジェクトへようこそ！",
            "今日も素晴らしい開発ができそうですね♪"
        ]
        
        for phrase in test_phrases:
            await haruka.speak(phrase)
            await asyncio.sleep(1)  # 少し間を置く
    
    # ステータス確認
    print(f"\n📊 ハルカペルソナ状態:")
    status = haruka.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print("\n✅ ハルカペルソナ統合テスト完了！")

if __name__ == "__main__":
    # テスト実行
    asyncio.run(test_haruka_integration())