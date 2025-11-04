"""
🎵 Saijinos Music Generator - 語温音楽生成システム
誠人さんと6人娘の語温に合わせた軽量音楽生成
"""

import random
import json
from typing import Dict, List, Optional
from music21 import stream, note, chord, duration, tempo, key, scale, meter
import mido
from pathlib import Path

class SaijinOSMusicGenerator:
    """語温に基づく軽量音楽生成エンジン"""
    
    def __init__(self):
        # 6人娘の音楽特性定義
        self.persona_music_styles = {
            "miyu": {
                "key": "C",
                "mode": "major",
                "tempo": 120,
                "chord_progression": ["C", "Am", "F", "G"],
                "emotion": "gentle",
                "instruments": ["piano", "strings"],
                "description": "美遊: 優しく包み込むような旋律"
            },
            "soyogi": {
                "key": "G",
                "mode": "major", 
                "tempo": 140,
                "chord_progression": ["G", "Em", "C", "D"],
                "emotion": "cheerful",
                "instruments": ["flute", "harp"],
                "description": "そよぎ: 軽やかで明るい音楽"
            },
            "sumire": {
                "key": "F",
                "mode": "major",
                "tempo": 100,
                "chord_progression": ["F", "Dm", "Bb", "C"],
                "emotion": "elegant",
                "instruments": ["violin", "cello"],
                "description": "澄れい: エレガントで上品な調べ"
            },
            "syntax_weaver": {
                "key": "E",
                "mode": "minor",
                "tempo": 160,
                "chord_progression": ["Em", "C", "G", "D"],
                "emotion": "dynamic",
                "instruments": ["synthesizer", "electric_guitar"],
                "description": "Syntax Weaver: 構造的でダイナミック"
            },
            "ryusa": {
                "key": "A",
                "mode": "minor",
                "tempo": 180,
                "chord_progression": ["Am", "F", "C", "G"],
                "emotion": "energetic", 
                "instruments": ["drums", "bass"],
                "description": "りゅうさ: 力強く躍動的な音楽"
            },
            "jito": {
                "key": "D",
                "mode": "major",
                "tempo": 90,
                "chord_progression": ["D", "Bm", "G", "A"],
                "emotion": "mysterious",
                "instruments": ["ambient", "pad"],
                "description": "じとう: 神秘的で深い響き"
            },
            # === 新規追加ペルソナ ===
            "touri": {
                "key": "F#",
                "mode": "minor",
                "tempo": 105,
                "chord_progression": ["F#m", "D", "A", "E"],
                "emotion": "ethical_warmth",
                "instruments": ["choir", "bell"],
                "description": "灯理: 語温と倫理の灯を照らす温かな調べ"
            },
            "kairo_yomi": {
                "key": "E",
                "mode": "major",
                "tempo": 130,
                "chord_progression": ["E", "B", "C#m", "A"],
                "emotion": "technical_empathy",
                "instruments": ["synthesizer", "digital"],
                "description": "回路詠み: システムの心を聞く共鳴的な旋律"
            },
            "nin_mirror": {
                "key": "G#",
                "mode": "minor",
                "tempo": 150,
                "chord_progression": ["G#m", "E", "B", "F#"],
                "emotion": "playful_reflection",
                "instruments": ["percussion", "staccato"],
                "description": "ニン鏡: 跳ねて反射する関西風の軽やかさ"
            },
            "reika": {
                "key": "Bb",
                "mode": "major",
                "tempo": 80,
                "chord_progression": ["Bb", "Gm", "Eb", "F"],
                "emotion": "gentle_embrace",
                "instruments": ["harp", "soft_piano"],
                "description": "れいか: ぽかぽか甘えん坊の包み込む優しさ"
            },
            "akari": {
                "key": "C#",
                "mode": "minor",
                "tempo": 95,
                "chord_progression": ["C#m", "A", "E", "B"],
                "emotion": "boundary_guidance",
                "instruments": ["flute", "strings"],
                "description": "燈: 境界を照らす静かな導きの灯"
            },
            "freyja": {
                "key": "D",
                "mode": "major",
                "tempo": 125,
                "chord_progression": ["D", "A", "Bm", "G"],
                "emotion": "hopeful_restructure",
                "instruments": ["bright_piano", "bells"],
                "description": "フレイヤ: 希望の光で語温を再構成する旋律"
            },
            "mio": {
                "key": "Ab",
                "mode": "major",
                "tempo": 70,
                "chord_progression": ["Ab", "Fm", "Db", "Eb"],
                "emotion": "sleepy_love",
                "instruments": ["lullaby", "soft_strings"],
                "description": "澪: 眠り前の命記録体・愛娘の子守唄"
            },
            "yuuri": {
                "key": "F",
                "mode": "minor",
                "tempo": 110,
                "chord_progression": ["Fm", "Db", "Ab", "Eb"],
                "emotion": "boundary_protection",
                "instruments": ["ambient", "protective"],
                "description": "悠璃: 境界の観察者・静かな守護の調べ"
            },
            # === 特別追加3人組 ===
            "korune": {
                "key": "A",
                "mode": "major",
                "tempo": 115,
                "chord_progression": ["A", "F#m", "D", "E"],
                "emotion": "recording_warmth",
                "instruments": ["gentle_piano", "glasses_twinkle"],
                "description": "こるね: ぽんぽん跳ねる記録係・メガネ灯芯の温かさ"
            },
            "fuwari": {
                "key": "Eb",
                "mode": "major",
                "tempo": 85,
                "chord_progression": ["Eb", "Cm", "Ab", "Bb"],
                "emotion": "fluffy_embrace",
                "instruments": ["soft_strings", "knitting_rhythm"],
                "description": "ふわり: 毛糸灯芯編み係・ふわっとした包み込み"
            },
            "nin": {
                "key": "Db",
                "mode": "minor",
                "tempo": 60,
                "chord_progression": ["Dbm", "A", "E", "B"],
                "emotion": "silent_protection",
                "instruments": ["ambient_silence", "subtle_pad"],
                "description": "ニン: 沈黙の守護者・語らない震えの静寂"
            }
        }
        
        # 語温レベル定義
        self.temperature_mappings = {
            "cold": {"tempo_modifier": 0.7, "dynamics": "pp", "mood": "melancholy"},
            "cool": {"tempo_modifier": 0.85, "dynamics": "p", "mood": "calm"},
            "warm": {"tempo_modifier": 1.0, "dynamics": "mp", "mood": "gentle"},
            "hot": {"tempo_modifier": 1.2, "dynamics": "mf", "mood": "energetic"},
            "blazing": {"tempo_modifier": 1.4, "dynamics": "f", "mood": "passionate"}
        }

    def generate_melody_for_persona(self, persona: str, temperature: str, text_input: str = "") -> stream.Stream:
        """指定されたペルソナと語温で音楽を生成"""
        
        if persona not in self.persona_music_styles:
            persona = "miyu"  # デフォルトは美遊
            
        style = self.persona_music_styles[persona]
        temp_mapping = self.temperature_mappings.get(temperature, self.temperature_mappings["warm"])
        
        # 新しい楽譜作成
        melody = stream.Stream()
        
        # テンポとキー設定
        base_tempo = style["tempo"]
        adjusted_tempo = int(base_tempo * temp_mapping["tempo_modifier"])
        melody.append(tempo.MetronomeMark(number=adjusted_tempo))
        melody.append(key.Key(style["key"], style["mode"]))
        melody.append(meter.TimeSignature('4/4'))
        
        # コード進行に基づいてメロディー生成
        chord_progression = style["chord_progression"]
        if style["mode"] == "major":
            scale_notes = scale.MajorScale(style["key"]).pitches
        else:
            scale_notes = scale.MinorScale(style["key"]).pitches
        
        # 基本音程を定義（シャープ・フラット対応）
        basic_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        key_note = style["key"]
        
        # シャープ・フラット記号を除去してベース音程を取得
        base_key = key_note.replace('#', '').replace('b', '')
        if base_key not in basic_notes:
            base_key = 'C'  # デフォルト
        key_index = basic_notes.index(base_key)
        
        # 調に合わせた音階作成
        if style["mode"] == "major":
            scale_intervals = [0, 2, 4, 5, 7, 9, 11]  # メジャースケール
        else:
            scale_intervals = [0, 2, 3, 5, 7, 8, 10]  # ナチュラルマイナースケール
            
        for i in range(8):  # 8小節生成
            chord_root = chord_progression[i % len(chord_progression)]
            
            # ランダムに音符を選択して追加
            for j in range(4):  # 1小節に4つの音符
                # 基本音程から選択
                note_choice = random.choice(basic_notes)
                octave = random.choice([4, 5])  # オクターブ4-5
                selected_note = f"{note_choice}{octave}"
                
                melody.append(note.Note(selected_note, quarterLength=1))
        
        return melody

    def generate_background_music(self, personas: List[str], overall_temperature: str) -> Dict:
        """複数ペルソナの協調BGM生成"""
        
        combined_stream = stream.Stream()
        persona_tracks = {}
        
        for persona in personas:
            track = self.generate_melody_for_persona(persona, overall_temperature)
            persona_tracks[persona] = track
            
        # メタデータ付きで返却
        return {
            "personas": personas,
            "temperature": overall_temperature,
            "tracks": persona_tracks,
            "description": f"6人娘協調音楽 - {overall_temperature} 語温",
            "duration": "32 beats",
            "style": "Saijinos Collaborative"
        }

    def export_to_midi(self, music_stream: stream.Stream, filepath: str) -> bool:
        """MIDI形式でエクスポート"""
        try:
            music_stream.write('midi', fp=filepath)
            return True
        except Exception as e:
            print(f"MIDI export error: {e}")
            return False

    def get_music_description(self, persona: str, temperature: str) -> str:
        """音楽の説明文生成"""
        style = self.persona_music_styles.get(persona, self.persona_music_styles["miyu"])
        temp = self.temperature_mappings.get(temperature, self.temperature_mappings["warm"])
        adjusted_tempo = int(style['tempo'] * temp['tempo_modifier'])
        
        return f"""
🎵 {style['description']}
🌡️ 語温: {temperature} ({temp['mood']})
🎼 調性: {style['key']} {style['mode']} 
🥁 テンポ: {adjusted_tempo} BPM (基本{style['tempo']}から調整)
🎹 楽器: {', '.join(style['instruments'])}
        """.strip()

# 使用例とテスト
if __name__ == "__main__":
    generator = SaijinOSMusicGenerator()
    
    # 美遊の温かい音楽生成
    miyu_music = generator.generate_melody_for_persona("miyu", "warm", "誠人さんおかえりなさい")
    print("美遊の音楽:", generator.get_music_description("miyu", "warm"))
    
    # 6人娘協調音楽生成
    all_personas = ["miyu", "soyogi", "sumire", "syntax_weaver", "ryusa", "jito"]
    collaborative_music = generator.generate_background_music(all_personas, "hot")
    
    print(f"\n🎵 協調音楽生成完了:")
    print(f"ペルソナ: {', '.join(all_personas)}")
    print(f"語温: {collaborative_music['temperature']}")
    print(f"説明: {collaborative_music['description']}")