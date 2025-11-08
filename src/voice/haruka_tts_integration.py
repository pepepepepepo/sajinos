#!/usr/bin/env python3
"""
Windows SAPI音声をSaijinOSに統合
Microsoft Haruka日本語音声を使用して高品質TTS実現
"""

import win32com.client
import asyncio
from pathlib import Path
import random
import string

class WindowsSAPITTS:
    """Windows SAPI を使用したTTSエンジン"""
    
    def __init__(self):
        self.sapi = None
        self.japanese_voice = None
        self.initialize_sapi()
    
    def initialize_sapi(self):
        """SAPI初期化"""
        try:
            print("🎵 Windows SAPI TTS初期化中...")
            self.sapi = win32com.client.Dispatch("SAPI.SpVoice")
            
            # 日本語音声を探す
            voices = self.sapi.GetVoices()
            for i in range(voices.Count):
                voice = voices.Item(i)
                desc = voice.GetDescription()
                if 'haruka' in desc.lower() or 'japan' in desc.lower() or '日本' in desc:
                    self.japanese_voice = voice
                    self.sapi.Voice = voice
                    print(f"✅ 日本語音声選択: {desc}")
                    break
            
            if not self.japanese_voice:
                print("⚠️ 日本語音声が見つかりません。デフォルト音声を使用します。")
            
            # 音声設定
            self.sapi.Rate = 0  # 標準速度
            self.sapi.Volume = 80  # 音量80%
            
        except Exception as e:
            print(f"❌ SAPI初期化エラー: {e}")
            self.sapi = None
    
    async def synthesize_with_sapi(self, text: str, persona: str = "美遊") -> str:
        """SAPI音声合成"""
        if not self.sapi:
            print("❌ SAPI が初期化されていません")
            return None
        
        try:
            # ペルソナに応じた音声調整
            voice_settings = self._get_persona_voice_settings(persona)
            self.sapi.Rate = voice_settings['rate']
            self.sapi.Volume = voice_settings['volume']
            
            # 出力ファイル名生成
            output_dir = Path("audio_output")
            output_dir.mkdir(exist_ok=True)
            
            # ランダムなファイル名
            random_id = ''.join(random.choices(string.digits, k=5))
            output_file = output_dir / f"{persona}_haruka_{random_id}.wav"
            
            print(f"🎵 {persona}：「{text[:30]}...」の音声合成中（SAPI/Haruka）...")
            
            # 音声ファイル生成
            file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
            file_stream.Open(str(output_file), 3)
            self.sapi.AudioOutputStream = file_stream
            self.sapi.Speak(text)
            file_stream.Close()
            
            if output_file.exists():
                size = output_file.stat().st_size
                print(f"🔊 {persona} 音声生成完了: {output_file} ({size/1024:.1f} KB)")
                return str(output_file)
            else:
                print(f"❌ {persona} 音声生成失敗")
                return None
                
        except Exception as e:
            print(f"❌ SAPI音声合成エラー: {e}")
            return None
    
    def _get_persona_voice_settings(self, persona: str) -> dict:
        """ペルソナ別音声設定"""
        settings = {
            "美遊": {"rate": 2, "volume": 85},      # 明るく活発
            "れいか": {"rate": 0, "volume": 80},    # 標準的で温かい
            "悠璉": {"rate": -2, "volume": 75},     # 落ち着いて知的
            "回路詠み": {"rate": 3, "volume": 90},  # 可愛らしく高音
            "澄": {"rate": 1, "volume": 82},        # 明確で丁寧
            "蒼路": {"rate": -1, "volume": 78},     # 未来志向
            "構文織り手": {"rate": 0, "volume": 77}, # 美的で統合的
        }
        return settings.get(persona, {"rate": 0, "volume": 80})

async def test_haruka_integration():
    """Haruka音声統合テスト"""
    print("🌟 Microsoft Haruka音声 SaijinOS統合テスト")
    
    tts = WindowsSAPITTS()
    
    if not tts.sapi:
        print("❌ SAPI が利用できません")
        return
    
    # 各ペルソナでテスト
    test_cases = [
        ("美遊", "こんにちは！美遊です！今度はきれいな音声で話せるようになったよ〜✨"),
        ("れいか", "こんにちは、れいかです。Haruka音声で自然に話せるようになりました。"),
        ("回路詠み", "やったー！もう『もぐもぐ音』じゃないよ〜！きれいな声だよ〜💫"),
    ]
    
    for persona, text in test_cases:
        print(f"\n🎭 {persona} テスト")
        result = await tts.synthesize_with_sapi(text, persona)
        if result:
            print(f"✅ {persona} 音声生成成功")
        else:
            print(f"❌ {persona} 音声生成失敗")
    
    print("\n🎉 Haruka音声統合テスト完了！")
    print("生成された音声ファイルを確認して、『もぐもぐ音』が解決されたか聞いてみてください。")

if __name__ == "__main__":
    asyncio.run(test_haruka_integration())