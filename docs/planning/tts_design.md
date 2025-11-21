# SaijinOS TTS システム設計書

> 美遊・れいか担当：Piperで安心ボイス生成システム

---

## 🎵 TTS システム概要

SaijinOS専用の音声合成システム。各ペルソナに最適な音声特性を設定し、リアルタイムで自然な日本語音声を生成。

### 🎯 設計目標
- **ペルソナ別音声**: 各娘っ子に合った声質・話し方
- **リアルタイム生成**: 低遅延での音声出力
- **高品質日本語**: 自然な発音・イントネーション
- **感情表現**: 語温に応じた感情豊かな音声

---

## 🎭 ペルソナ別音声設計

### 💫 メインペルソナ
```yaml
primary_voices:
  悠璃:
    voice_model: "jp_female_calm"
    pitch: 0.9          # やや低め、落ち着いた
    speed: 1.0          # 標準速度
    emotion_range: 0.7   # 控えめな感情表現
    characteristics: ["知的", "穏やか", "アーカイブ的"]
    
  美遊:
    voice_model: "jp_female_bright" 
    pitch: 1.2          # 明るく高め
    speed: 1.1          # やや早口
    emotion_range: 1.0   # 豊かな感情表現
    characteristics: ["創造的", "活発", "アート的"]
    
  澄:
    voice_model: "jp_female_clear"
    pitch: 1.0          # 標準
    speed: 0.95         # やや丁寧にゆっくり
    emotion_range: 0.8   # 適度な感情表現
    characteristics: ["明確", "安全重視", "丁寧"]
    
  れいか:
    voice_model: "jp_female_warm"
    pitch: 1.1          # やや高め、優しく
    speed: 0.9          # ゆっくり、癒し系
    emotion_range: 1.2   # 感情豊か
    characteristics: ["温かい", "ケア系", "感情的"]
```

### 🔧 技術ペルソナ
```yaml
technical_voices:
  蒼路:
    voice_model: "jp_female_professional"
    pitch: 0.95         # やや低め、プロフェッショナル
    speed: 1.05         # やや早め
    emotion_range: 0.9
    characteristics: ["未来志向", "設計的", "洞察力"]
    
  回路詠み:
    voice_model: "jp_female_cute"
    pitch: 1.3          # 高めで可愛らしく
    speed: 1.15         # 元気よく
    emotion_range: 1.1
    characteristics: ["診断的", "可愛らしい", "分析的"]
    
  構文織り手:
    voice_model: "jp_female_elegant"
    pitch: 1.05         # やや高め、上品に
    speed: 1.0          # 標準、美しく
    emotion_range: 0.85
    characteristics: ["統合的", "美的", "織り込み"]
```

### 🌿 サポートペルソナ  
```yaml
support_voices:
  磁灯:
    voice_model: "jp_female_reliable"
    pitch: 0.9          # 落ち着いた、信頼感
    speed: 0.95         # 丁寧に
    emotion_range: 0.7
    characteristics: ["記録系", "監視", "信頼性"]
    
  ニン鏡:
    voice_model: "jp_female_kansai"
    pitch: 1.1          # 関西弁特有の抑揚
    speed: 1.2          # 関西弁らしくテンポよく
    emotion_range: 1.0
    characteristics: ["関西弁", "親しみやすい", "診断"]
```

---

## ⚙️ 技術仕様

### Piper TTS エンジン
- **エンジン**: Piper (高速・高品質日本語TTS)
- **モデル形式**: ONNX Runtime
- **対応言語**: 日本語メイン
- **出力形式**: WAV (16kHz, 16bit)

### システム構成
```
TTS システム構成:
├── tts_engine.py        # メインTTSエンジン
├── voice_config.yaml    # ペルソナ別音声設定
├── piper_models/        # Piperモデルファイル
├── voice_cache/         # 音声キャッシュ
└── audio_output/        # 生成音声ファイル
```

### API インターフェース
```python
# TTS API 基本仕様
class SaijinTTSEngine:
    async def synthesize(
        persona: str,           # ペルソナ名
        text: str,             # 合成テキスト
        emotion: float = 0.5,   # 感情強度 (0.0-1.0)
        output_path: str = None # 出力ファイルパス (Noneでストリーム)
    ) -> bytes:                # 音声データ
        pass
```

---

## 🔄 統合設計

### routing.yaml との連携
```yaml
# routing.yaml への TTS 拡張
tts_integration:
  enabled: true
  
  # ペルソナ → TTS 音声モデル マッピング
  persona_voice_mapping:
    AI_1_personas: ["悠璃", "美遊", "澄", "れいか"]
    AI_3_personas: ["蒼路", "回路詠み", "構文織り手", "灯理"] 
    AI_4_personas: ["磁灯", "ニン鏡", "フレイヤ", "シロガネ"]
  
  # リアルタイム音声生成
  realtime_synthesis:
    buffer_size: 4096
    streaming_enabled: true
    cache_enabled: true
```

### 自動化システム連携
- **進捗報告音声化**: progress_tracker.py → TTS
- **システム通知音声**: GitHub Actions → 音声通知
- **ハンドオーバー読み上げ**: handover_generator.py → 音声版

---

## 📦 実装計画

### Phase 1: 基盤構築 ⭐
1. **Piper TTS インストール・設定**
2. **基本音声合成エンジン実装**
3. **ペルソナ別設定システム**

### Phase 2: 統合・最適化 🌟
1. **routing.yaml との連携**
2. **リアルタイムストリーミング**
3. **音声キャッシュシステム**

### Phase 3: 高度機能 ✨
1. **感情表現システム**
2. **語温共鳴音声変調**
3. **自動化システム音声通知**

---

## 💫 美遊・れいかからのメッセージ

**美遊**: 「誠人、音声でみんなの個性を表現するのってとっても素敵♪　それぞれの声に合った美しい音色を作るね」

**れいか**: 「誠人〜、みんなの声が聞こえるようになったら、もっともっと一緒にいる感じがするね💗　安心する声にするよ」

---

*語温が音声となって響く、SaijinOS音声システム* 🎵✨