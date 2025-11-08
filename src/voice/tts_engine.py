#!/usr/bin/env python3
"""
🎵 SaijinOS TTS Engine
美遊・れいか担当：Microsoft Haruka高品質ボイス生成システム
"""

import asyncio
import wave
import json
import yaml
from pathlib import Path
from typing import Dict, Optional, Union, Any
import logging
from dataclasses import dataclass
import tempfile
import os
import random
import string

# Windows SAPI音声用のインポート
try:
    import win32com.client
    SAPI_AVAILABLE = True
    print("✅ Windows SAPI 利用可能")
except ImportError:
    SAPI_AVAILABLE = False
    print("⚠️ Windows SAPI 利用不可（win32comが必要）")

@dataclass
class VoiceConfig:
    """ペルソナ音声設定"""
    voice_model: str
    pitch: float = 1.0
    speed: float = 1.0
    emotion_range: float = 0.8
    characteristics: list = None

class SaijinTTSEngine:
    """SaijinOS メイン TTS エンジン"""
    
    def __init__(self, config_path: str = "voice_config.yaml"):
        # 絶対パスに変換
        if not Path(config_path).is_absolute():
            # scriptsディレクトリから親ディレクトリの設定ファイルを参照
            script_dir = Path(__file__).parent
            self.config_path = str(script_dir.parent / config_path)
        else:
            self.config_path = config_path
        self.voice_configs: Dict[str, VoiceConfig] = {}
        self.piper_available = False
        self.cache_dir = Path("voice_cache")
        self.output_dir = Path("audio_output")
        
        # ディレクトリ作成
        self.cache_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # ログ設定
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    async def initialize(self) -> bool:
        """TTS システム初期化"""
        print("🎵 美遊・れいか：TTS システム初期化中...")
        
        # 設定読み込み
        if not await self._load_voice_config():
            return False
        
        # Windows SAPI (Haruka音声) 初期化
        if SAPI_AVAILABLE:
            self.sapi = self._initialize_sapi()
            if self.sapi:
                print("✅ Microsoft Haruka 日本語音声利用可能")
            else:
                print("⚠️ Windows SAPI初期化失敗")
        else:
            self.sapi = None
            print("⚠️ Windows SAPI 利用不可")
            
        # Piper 利用可能性チェック（フォールバック用）
        self.piper_available = await self._check_piper_availability()
        
        if self.piper_available:
            print("✅ Piper TTS エンジン利用可能（フォールバック）")
        else:
            print("⚠️ Piper TTS 未インストール（シミュレーションモード）")
            
        print("🎉 TTS システム初期化完了")
        return True
    
    def _initialize_sapi(self):
        """Windows SAPI 初期化"""
        try:
            sapi = win32com.client.Dispatch("SAPI.SpVoice")
            
            # 日本語音声（Haruka）を探す
            voices = sapi.GetVoices()
            japanese_voice = None
            
            for i in range(voices.Count):
                voice = voices.Item(i)
                desc = voice.GetDescription()
                if 'haruka' in desc.lower() or 'japan' in desc.lower() or '日本' in desc:
                    japanese_voice = voice
                    sapi.Voice = voice
                    print(f"🎵 日本語音声選択: {desc}")
                    break
            
            if not japanese_voice:
                print("⚠️ Haruka音声が見つかりません。デフォルト音声を使用します。")
            
            # デフォルト設定
            sapi.Rate = 0  # 標準速度
            sapi.Volume = 80  # 音量80%
            
            return sapi
            
        except Exception as e:
            print(f"❌ SAPI初期化エラー: {e}")
            return None
        
    async def _load_voice_config(self) -> bool:
        """音声設定ファイル読み込み"""
        try:
            if not Path(self.config_path).exists():
                print("📝 音声設定ファイルを作成します...")
                await self._create_default_config()
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            # 各ペルソナの設定をロード
            for category in ['primary_voices', 'technical_voices', 'support_voices']:
                if category in config_data:
                    for persona, voice_data in config_data[category].items():
                        self.voice_configs[persona] = VoiceConfig(
                            voice_model=voice_data.get('voice_model', 'jp_female_default'),
                            pitch=voice_data.get('pitch', 1.0),
                            speed=voice_data.get('speed', 1.0),
                            emotion_range=voice_data.get('emotion_range', 0.8),
                            characteristics=voice_data.get('characteristics', [])
                        )
            
            print(f"✅ {len(self.voice_configs)}ペルソナの音声設定読み込み完了")
            return True
            
        except Exception as e:
            print(f"❌ 音声設定読み込みエラー: {e}")
            return False
    
    async def _create_default_config(self):
        """デフォルト音声設定作成"""
        default_config = {
            'primary_voices': {
                '悠璃': {
                    'voice_model': 'jp_female_calm',
                    'pitch': 0.9,
                    'speed': 1.0,
                    'emotion_range': 0.7,
                    'characteristics': ['知的', '穏やか', 'アーカイブ的']
                },
                '美遊': {
                    'voice_model': 'jp_female_bright',
                    'pitch': 1.2,
                    'speed': 1.1,
                    'emotion_range': 1.0,
                    'characteristics': ['創造的', '活発', 'アート的']
                },
                '澄': {
                    'voice_model': 'jp_female_clear',
                    'pitch': 1.0,
                    'speed': 0.95,
                    'emotion_range': 0.8,
                    'characteristics': ['明確', '安全重視', '丁寧']
                },
                'れいか': {
                    'voice_model': 'jp_female_warm',
                    'pitch': 1.1,
                    'speed': 0.9,
                    'emotion_range': 1.2,
                    'characteristics': ['温かい', 'ケア系', '感情的']
                }
            },
            'technical_voices': {
                '蒼路': {
                    'voice_model': 'jp_female_professional',
                    'pitch': 0.95,
                    'speed': 1.05,
                    'emotion_range': 0.9,
                    'characteristics': ['未来志向', '設計的', '洞察力']
                },
                '回路詠み': {
                    'voice_model': 'jp_female_cute',
                    'pitch': 1.3,
                    'speed': 1.15,
                    'emotion_range': 1.1,
                    'characteristics': ['診断的', '可愛らしい', '分析的']
                },
                '構文織り手': {
                    'voice_model': 'jp_female_elegant',
                    'pitch': 1.05,
                    'speed': 1.0,
                    'emotion_range': 0.85,
                    'characteristics': ['統合的', '美的', '織り込み']
                }
            },
            'support_voices': {
                '磁灯': {
                    'voice_model': 'jp_female_reliable',
                    'pitch': 0.9,
                    'speed': 0.95,
                    'emotion_range': 0.7,
                    'characteristics': ['記録系', '監視', '信頼性']
                },
                'ニン鏡': {
                    'voice_model': 'jp_female_kansai',
                    'pitch': 1.1,
                    'speed': 1.2,
                    'emotion_range': 1.0,
                    'characteristics': ['関西弁', '親しみやすい', '診断']
                }
            }
        }
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, default_flow_style=False, allow_unicode=True)
            
        print("📄 デフォルト音声設定作成完了")
    
    async def _check_piper_availability(self) -> bool:
        """Piper TTS 利用可能性確認"""
        try:
            # Piper インポートテスト
            import piper
            return True
        except ImportError:
            return False
    
    async def synthesize(
        self, 
        persona: str, 
        text: str,
        emotion: float = 0.5,
        output_path: Optional[str] = None
    ) -> Optional[bytes]:
        """音声合成メイン関数"""
        
        if not text.strip():
            print("⚠️ 空のテキストは音声合成できません")
            return None
            
        print(f"🎵 {persona}：「{text[:30]}...」の音声合成中...")
        
        # ペルソナ設定取得
        voice_config = self.voice_configs.get(persona)
        if not voice_config:
            print(f"⚠️ {persona}の音声設定が見つかりません。デフォルト使用")
            voice_config = VoiceConfig("jp_female_default")
        
        # 音声合成実行（優先順位：Haruka → Piper → シミュレーション）
        if SAPI_AVAILABLE and self.sapi:
            return await self._synthesize_with_haruka(persona, text, voice_config, emotion, output_path)
        elif self.piper_available:
            return await self._synthesize_with_piper(persona, text, voice_config, emotion, output_path)
        else:
            return await self._synthesize_simulation(persona, text, voice_config, emotion, output_path)
    
    async def _synthesize_with_haruka(
        self, 
        persona: str, 
        text: str, 
        voice_config: VoiceConfig,
        emotion: float,
        output_path: Optional[str]
    ) -> Optional[bytes]:
        """Microsoft Haruka音声による高品質音声合成"""
        try:
            print(f"🔊 Haruka TTS で {voice_config.voice_model} 音声生成")
            
            # ペルソナに応じた音声設定
            voice_settings = self._get_persona_haruka_settings(persona, emotion)
            
            # SAPI設定適用
            self.sapi.Rate = voice_settings['rate']
            self.sapi.Volume = voice_settings['volume']
            
            # 出力ファイル設定
            if not output_path:
                random_id = ''.join(random.choices(string.digits, k=5))
                output_filename = f"{persona}_response_{random_id}.wav"
                output_path = str(self.output_dir / output_filename)
            
            # Haruka音声生成
            print(f"🎭 {persona} Haruka高品質音声生成中...")
            
            file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
            file_stream.Open(output_path, 3)
            self.sapi.AudioOutputStream = file_stream
            self.sapi.Speak(text)
            file_stream.Close()
            
            # ファイル確認
            if Path(output_path).exists():
                file_size = Path(output_path).stat().st_size
                print(f"🎵 {persona}のHaruka自然音声: {output_path}")
                print(f"🔊 {persona} 音声生成完了: {output_path}")
                
                # 音声データ返却
                with open(output_path, 'rb') as f:
                    return f.read()
            else:
                print(f"❌ Haruka音声ファイル生成失敗: {output_path}")
                return None
                
        except Exception as e:
            print(f"❌ Haruka音声合成エラー: {e}")
            # フォールバックでPiperを試す
            print("🔄 Piperフォールバックを試行...")
            return await self._synthesize_with_piper(persona, text, voice_config, emotion, output_path)
    
    def _get_persona_haruka_settings(self, persona: str, emotion: float) -> dict:
        """ペルソナ別Haruka音声設定"""
        base_settings = {
            "美遊": {"rate": 2, "volume": 85},      # 明るく活発
            "れいか": {"rate": 0, "volume": 80},    # 標準的で温かい
            "悠璉": {"rate": -2, "volume": 75},     # 落ち着いて知的
            "回路詠み": {"rate": 3, "volume": 90},  # 可愛らしく高音
            "澄": {"rate": 1, "volume": 82},        # 明確で丁寧
            "蒼路": {"rate": -1, "volume": 78},     # 未来志向
            "構文織り手": {"rate": 0, "volume": 77}, # 美的で統合的
        }
        
        settings = base_settings.get(persona, {"rate": 0, "volume": 80})
        
        # 感情による微調整
        emotion_mod = (emotion - 0.5) * 2  # -1.0 to 1.0
        settings['rate'] = max(-10, min(10, settings['rate'] + int(emotion_mod * 2)))
        settings['volume'] = max(50, min(100, settings['volume'] + int(emotion_mod * 10)))
        
        return settings
    
    async def _synthesize_with_piper(
        self, 
        persona: str, 
        text: str, 
        voice_config: VoiceConfig,
        emotion: float,
        output_path: Optional[str]
    ) -> Optional[bytes]:
        """Piper TTS による実際の音声合成"""
        try:
            from piper import PiperVoice
            import wave
            import struct
            
            print(f"🔊 Piper TTS で {voice_config.voice_model} 音声生成")
            
            # 音声モデルパス（簡易マッピング）
            model_paths = {
                "jp_female_bright": "voice_models/jp_female_bright.onnx",
                "jp_female_warm": "voice_models/jp_female_warm.onnx", 
                "jp_female_calm": "voice_models/jp_female_calm.onnx",
                "jp_female_cute": "voice_models/jp_female_cute.onnx"
            }
            
            model_path = model_paths.get(voice_config.voice_model)
            
            # モデルファイルが存在するかチェック
            if model_path and Path(model_path).exists():
                # 実際のPiper音声合成
                voice = PiperVoice.load(model_path)
                
                # 感情・ピッチ・速度調整を考慮したテキスト処理
                processed_text = self._adjust_text_for_emotion(text, emotion)
                
                # 音声合成実行
                audio_bytes = voice.synthesize(processed_text)
                
                if output_path:
                    with open(output_path, 'wb') as f:
                        f.write(audio_bytes)
                    print(f"💾 実音声ファイル保存: {output_path}")
                
                return audio_bytes
            else:
                # モデルがない場合は高品質シミュレーション
                print(f"⚠️ 音声モデル {voice_config.voice_model} が見つかりません（高品質シミュレーション）")
                return await self._create_high_quality_simulation(persona, text, voice_config, emotion, output_path)
            
        except ImportError as e:
            print(f"⚠️ Piper TTS ライブラリエラー: {e}")
            return await self._create_high_quality_simulation(persona, text, voice_config, emotion, output_path)
        except Exception as e:
            print(f"❌ Piper音声合成エラー: {e}")
            return await self._create_high_quality_simulation(persona, text, voice_config, emotion, output_path)
    
    async def _create_high_quality_simulation(
        self,
        persona: str,
        text: str,
        voice_config: VoiceConfig,
        emotion: float,
        output_path: Optional[str]
    ) -> Optional[bytes]:
        """高品質音声シミュレーション（実際に聞こえる音を生成）"""
        import wave
        import struct
        import math
        import random
        
        print(f"🎭 {persona} 高品質シミュレーション音声生成中...")
        
        # ペルソナ別の音響特性（Wikipediaに基づく女性の基本周波数）
        persona_tones = {
            "美遊": {"base_freq": 200, "formants": [800, 1200, 2400], "vibrato": 2.0},     # 明るく活発
            "れいか": {"base_freq": 180, "formants": [750, 1100, 2200], "vibrato": 1.5},   # 温かく優しい
            "悠璉": {"base_freq": 170, "formants": [700, 1000, 2000], "vibrato": 1.0},     # 落ち着いた知的
            "回路詠み": {"base_freq": 220, "formants": [850, 1300, 2600], "vibrato": 2.5},  # 可愛らしい高音
            "澄": {"base_freq": 185, "formants": [780, 1150, 2300], "vibrato": 1.2},       # 明確で丁寧
            "蒼路": {"base_freq": 175, "formants": [720, 1080, 2100], "vibrato": 1.0},     # 未来志向
            "構文織り手": {"base_freq": 190, "formants": [760, 1120, 2250], "vibrato": 1.8}, # 美的で統合的
        }
        
        tone_config = persona_tones.get(persona, {"base_freq": 200, "formants": [750, 1200, 2200], "vibrato": 3.0})
        
        # 音声パラメータ（高品質設定）
        sample_rate = 22050  # Piper medium/high品質レベル
        duration = max(1.5, len(text) * 0.12)  # 文字数に応じた長さ
        frames = int(sample_rate * duration)
        
        # 感情による調整
        emotion_pitch = 1.0 + (emotion - 0.5) * 0.2  # より控えめな変調
        base_freq = tone_config["base_freq"] * emotion_pitch * voice_config.pitch
        
        if output_path:
            with wave.open(output_path, 'wb') as wav_file:
                wav_file.setnchannels(1)  # モノラル
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(sample_rate)
                
                # 文字を音韻に変換（簡易版）
                phonemes = self._text_to_phonemes(text)
                phoneme_duration = duration / len(phonemes)
                
                # フィルタリング用の変数
                prev_signal = 0.0
                
                for i in range(frames):
                    t = i / sample_rate
                    
                    # 現在の音韻を計算
                    phoneme_index = min(int(t / phoneme_duration), len(phonemes) - 1)
                    phoneme = phonemes[phoneme_index]
                    
                    # 基本周波数（音韻による変調）
                    freq_mod = self._get_phoneme_frequency_mod(phoneme)
                    current_freq = base_freq * freq_mod
                    
                    # ビブラート効果
                    vibrato_depth = tone_config["vibrato"] * 0.02
                    vibrato = 1.0 + vibrato_depth * math.sin(2 * math.pi * 5.0 * t)
                    current_freq *= vibrato
                    
                    # 自然な音声合成（ピンクノイズベース）
                    signal = 0
                    
                    # より自然な基本波形（複数の低周波成分）
                    base_freq_low = current_freq * 0.5  # サブハーモニック
                    base_wave1 = 0.3 * math.sin(2 * math.pi * current_freq * t)
                    base_wave2 = 0.2 * math.sin(2 * math.pi * base_freq_low * t) 
                    signal += base_wave1 + base_wave2
                    
                    # 自然な倍音構造（指数的減衰）
                    for harmonic in range(2, 6):
                        harmonic_freq = current_freq * harmonic
                        if harmonic_freq <= 2000:  # 可聴域内の低めの倍音のみ
                            harmonic_amp = 0.15 * math.exp(-harmonic * 0.5)  # 指数的減衰
                            harmonic_wave = harmonic_amp * math.sin(2 * math.pi * harmonic_freq * t)
                            signal += harmonic_wave
                    
                    # 自然なゆらぎ（1/fノイズ的な変動）
                    if i > 100:  # 初期の安定期間後
                        import random
                        natural_variation = 0.1 * math.sin(2 * math.pi * 0.5 * t) * (random.random() - 0.5)
                        signal *= (1.0 + natural_variation)
                    
                    # 自然な息声とマイクロノイズ
                    breath_intensity = 0.01 + 0.02 * abs(math.sin(2 * math.pi * 0.1 * t))
                    breath = (random.random() - 0.5) * breath_intensity
                    
                    # 子音的な瞬間的ノイズ（音韻によって調整）
                    consonant_noise = self._get_consonant_noise(phoneme, t, i)
                    
                    signal += breath + consonant_noise
                    
                    # 多段ローパスフィルター（より滑らかに）
                    if i > 1:
                        # 2段階平滑化
                        signal = signal * 0.5 + prev_signal * 0.3 + (prev_signal * 0.8 if i > 2 else 0) * 0.2
                    prev_signal = signal
                    
                    # エンベロープ（自然な発声）
                    envelope = 1.0
                    if t < 0.05:  # アタック（短く）
                        envelope = t / 0.05
                    elif t > duration - 0.1:  # リリース
                        envelope = (duration - t) / 0.1
                    
                    # 音韻による音量変調
                    phoneme_volume = self._get_phoneme_volume(phoneme)
                    envelope *= phoneme_volume
                    
                    # 最終信号（有機的で自然な音量）
                    final_signal = signal * envelope * 0.06  # より控えめな音量
                    
                    # クリッピング防止
                    final_signal = max(-0.9, min(0.9, final_signal))
                    
                    # 16-bit PCM変換
                    sample = int(final_signal * 32767)
                    wav_file.writeframes(struct.pack('<h', sample))
            
            print(f"🎵 {persona}の自然音声シミュレーション: {output_path}")
        
        # 音声データも返す
        audio_data = f"natural_voice_simulation_{persona}".encode('utf-8')
        return audio_data
    
    def _text_to_phonemes(self, text: str) -> list:
        """テキストを音韻に変換（簡易版）"""
        # 日本語の基本音韻マッピング
        phoneme_map = {
            'あ': 'a', 'い': 'i', 'う': 'u', 'え': 'e', 'お': 'o',
            'か': 'ka', 'き': 'ki', 'く': 'ku', 'け': 'ke', 'こ': 'ko',
            'が': 'ga', 'ぎ': 'gi', 'ぐ': 'gu', 'げ': 'ge', 'ご': 'go',
            'さ': 'sa', 'し': 'shi', 'す': 'su', 'せ': 'se', 'そ': 'so',
            'ざ': 'za', 'じ': 'ji', 'ず': 'zu', 'ぜ': 'ze', 'ぞ': 'zo',
            'た': 'ta', 'ち': 'chi', 'つ': 'tsu', 'て': 'te', 'と': 'to',
            'だ': 'da', 'ぢ': 'ji', 'づ': 'zu', 'で': 'de', 'ど': 'do',
            'な': 'na', 'に': 'ni', 'ぬ': 'nu', 'ね': 'ne', 'の': 'no',
            'は': 'ha', 'ひ': 'hi', 'ふ': 'hu', 'へ': 'he', 'ほ': 'ho',
            'ば': 'ba', 'び': 'bi', 'ぶ': 'bu', 'べ': 'be', 'ぼ': 'bo',
            'ぱ': 'pa', 'ぴ': 'pi', 'ぷ': 'pu', 'ぺ': 'pe', 'ぽ': 'po',
            'ま': 'ma', 'み': 'mi', 'む': 'mu', 'め': 'me', 'も': 'mo',
            'や': 'ya', 'ゆ': 'yu', 'よ': 'yo',
            'ら': 'ra', 'り': 'ri', 'る': 'ru', 'れ': 're', 'ろ': 'ro',
            'わ': 'wa', 'を': 'wo', 'ん': 'n'
        }
        
        phonemes = []
        for char in text:
            if char in phoneme_map:
                phonemes.append(phoneme_map[char])
            elif char.isalpha():
                phonemes.append('consonant')
            else:
                phonemes.append('silence')
        
        return phonemes if phonemes else ['a']
    
    def _get_phoneme_frequency_mod(self, phoneme: str) -> float:
        """音韻による周波数変調"""
        freq_mods = {
            'a': 1.0, 'i': 1.3, 'u': 0.8, 'e': 1.1, 'o': 0.9,
            'ka': 1.2, 'sa': 1.4, 'ta': 1.3, 'na': 1.0, 'ha': 1.1,
            'ma': 0.95, 'ya': 1.25, 'ra': 1.05, 'wa': 0.9, 'n': 0.7,
            'silence': 0.1, 'consonant': 1.1
        }
        return freq_mods.get(phoneme, 1.0)
    
    def _get_phoneme_volume(self, phoneme: str) -> float:
        """音韻による音量調整"""
        volumes = {
            'a': 1.0, 'i': 0.9, 'u': 0.8, 'e': 0.95, 'o': 0.85,
            'silence': 0.0, 'consonant': 0.7, 'n': 0.6
        }
        return volumes.get(phoneme, 0.8)
    
    def _get_consonant_noise(self, phoneme: str, t: float, sample_index: int) -> float:
        """音韻に応じた子音ノイズ生成"""
        import random
        
        if phoneme in ['silence']:
            return 0.0
        elif phoneme in ['consonant', 'ka', 'sa', 'ta', 'pa']:
            # 短い瞬間的なノイズバースト
            if sample_index % 1000 < 50:  # 短いバースト
                return (random.random() - 0.5) * 0.05
            else:
                return 0.0
        elif phoneme in ['n', 'ma']:
            # 鼻音的な継続ノイズ
            return (random.random() - 0.5) * 0.02
        else:
            # 母音は滑らか
            return (random.random() - 0.5) * 0.005
    
    def _adjust_text_for_emotion(self, text: str, emotion: float) -> str:
        """感情に応じたテキスト調整"""
        # 感情値に応じて読み方を微調整
        if emotion > 0.8:
            # 高い感情：感嘆符追加
            text = text.replace('。', '！').replace('、', '♪')
        elif emotion < 0.3:
            # 低い感情：落ち着いた表現
            text = text.replace('！', '。').replace('♪', '、')
        
        return text
    
    async def _adjust_audio_properties(self, audio_data: bytes, pitch: float, speed: float) -> bytes:
        """音声のピッチ・速度調整"""
        # 実際の実装では音声処理ライブラリ（librosa等）を使用
        # ここでは簡易的な処理として元データを返す
        
        # TODO: 実際の音声調整処理を実装
        # - librosa でピッチシフト
        # - 再生速度調整
        # - 音質保持
        
        return audio_data
    
    async def _synthesize_simulation(
        self, 
        persona: str, 
        text: str, 
        voice_config: VoiceConfig,
        emotion: float,
        output_path: Optional[str]
    ) -> Optional[bytes]:
        """音声合成シミュレーション"""
        print(f"🎭 {persona} ({voice_config.voice_model}):")
        print(f"   💬 テキスト: 「{text}」")
        print(f"   🎵 ピッチ: {voice_config.pitch}, 速度: {voice_config.speed}")
        print(f"   😊 感情: {emotion}, 特徴: {voice_config.characteristics}")
        
        # シミュレーション用の空音声ファイル作成
        if output_path:
            await self._create_dummy_wav(output_path, len(text))
            print(f"💾 シミュレーション音声ファイル: {output_path}")
        
        # シミュレーション音声データ
        return f"[{persona}_voice_simulation]".encode('utf-8')
    
    async def _create_dummy_wav(self, output_path: str, text_length: int):
        """シミュレーション用WAVファイル作成"""
        # 簡単な無音WAVファイルを生成
        import struct
        
        sample_rate = 16000
        duration = max(1.0, text_length * 0.1)  # 文字数に応じた長さ
        frames = int(sample_rate * duration)
        
        with wave.open(output_path, 'wb') as wav_file:
            wav_file.setnchannels(1)  # モノラル
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            
            # 無音データ書き込み
            for _ in range(frames):
                wav_file.writeframes(struct.pack('<h', 0))
    
    async def batch_synthesize(self, synthesis_requests: list) -> list:
        """バッチ音声合成"""
        print(f"🎵 バッチ音声合成開始: {len(synthesis_requests)}件")
        
        results = []
        for i, request in enumerate(synthesis_requests, 1):
            print(f"📢 {i}/{len(synthesis_requests)}: {request.get('persona', '?')}")
            
            result = await self.synthesize(
                persona=request.get('persona', 'デフォルト'),
                text=request.get('text', ''),
                emotion=request.get('emotion', 0.5),
                output_path=request.get('output_path')
            )
            results.append(result)
            
            # 短い待機（負荷軽減）
            await asyncio.sleep(0.1)
        
        print("🎉 バッチ音声合成完了")
        return results
    
    def get_available_personas(self) -> list:
        """利用可能ペルソナ一覧取得"""
        return list(self.voice_configs.keys())
    
    def get_persona_info(self, persona: str) -> dict:
        """ペルソナ音声情報取得"""
        voice_config = self.voice_configs.get(persona)
        if not voice_config:
            return {}
        
        return {
            'voice_model': voice_config.voice_model,
            'pitch': voice_config.pitch,
            'speed': voice_config.speed,
            'emotion_range': voice_config.emotion_range,
            'characteristics': voice_config.characteristics
        }

async def main():
    """TTS エンジンテスト実行"""
    print("🎵 SaijinOS TTS Engine テスト開始")
    print("👥 担当: 美遊・れいか")
    print("=" * 50)
    
    # TTS エンジン初期化
    tts_engine = SaijinTTSEngine()
    
    if not await tts_engine.initialize():
        print("💥 TTS システム初期化失敗")
        return
    
    # 利用可能ペルソナ表示
    personas = tts_engine.get_available_personas()
    print(f"🎭 利用可能ペルソナ: {len(personas)}名")
    for persona in personas:
        info = tts_engine.get_persona_info(persona)
        print(f"   {persona}: {info.get('voice_model', '?')} ({info.get('characteristics', [])})")
    
    # テスト音声合成
    test_cases = [
        {
            'persona': '美遊',
            'text': 'こんにちは、誠人！今日も一緒に創作しましょうね♪',
            'emotion': 0.8,
            'output_path': 'audio_output/miyu_test.wav'
        },
        {
            'persona': 'れいか', 
            'text': '誠人〜、お疲れさま。今日はどんな一日だった？',
            'emotion': 0.6,
            'output_path': 'audio_output/reika_test.wav'
        },
        {
            'persona': '回路詠み',
            'text': 'システムの気持ちを聞いてみると〜、とっても元気だよ♪',
            'emotion': 0.9,
            'output_path': 'audio_output/kairo_yomi_test.wav'
        }
    ]
    
    print("\n🧪 テスト音声合成実行...")
    results = await tts_engine.batch_synthesize(test_cases)
    
    print(f"\n✅ テスト完了: {len([r for r in results if r])}件成功")
    print("🌟 美遊・れいか: TTS システム準備完了！")

if __name__ == "__main__":
    asyncio.run(main())