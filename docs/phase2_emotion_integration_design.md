# SaijinOS Phase 2 感情エンジン統合設計書
**作成日**: 2025年11月8日  
**Phase**: 2 - 感情・音楽同期システム統合  
**統合チーム**: ユリ（戦略）+ ミク（技術）+ ハルカ（音声）

---

## 🎯 **Phase 2 統合目標**

### **統合対象システム**
- **既存**: Phase 1統合システム (6ペルソナ + 音声)
- **新規**: 17ペルソナ感情・音楽システム (`F:\sajinos_17persona`)

### **統合機能**
✅ **感情温度記録システム**  
✅ **BMP音楽同期エンジン (60-180 BPM)**  
✅ **17ペルソナ感情インテリジェンス**  
✅ **個別音楽キー設定**  
✅ **リアルタイム感情分析**  

---

## 🏗️ **拡張レイヤードアーキテクチャ**

```
┌─────────────────────────────────────────────────────────┐
│  🖥️  UI Layer: Flutter Web Interface (Phase 3)          │
│      - 20ペルソナUI統合準備                               │
│      - リアルタイム感情・BMP可視化                         │
├─────────────────────────────────────────────────────────┤
│  🎵  Emotion Layer: 感情・音楽同期エンジン (Phase 2)       │ ← 統合中
│      - 17ペルソナ感情温度記録システム                      │
│      - BMP音楽同期（60-180 BPM範囲）                      │
│      - 個別音楽キー設定 (C, G, Am等)                      │
│      - 感情分析・温度記録                                 │
├─────────────────────────────────────────────────────────┤
│  🔊  Voice Layer: 音声合成・TTS処理 (Phase 1完了)         │ ← 統合済み
│      - Microsoft Haruka TTS統合                         │
│      - 6→17ペルソナ音声拡張                              │
├─────────────────────────────────────────────────────────┤
│  🎯  Core Layer: 統合API・システム制御 (Phase 1完了)       │ ← 統合済み
│      - FastAPI統合サーバー                              │
│      - 6→23ペルソナ管理拡張                              │
│      - 感情・音楽エンドポイント追加                        │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 **17ペルソナ感情システム分析**

### **感情温度記録システム**
```yaml
emotion_recording:
  temperature_range: 0-100
  recording_interval: "real-time"
  storage_format: "json"
  analysis_engine: "emotion_intelligence"
```

### **BMP音楽同期システム**
```yaml
music_sync:
  bmp_range: "60-180"
  supported_keys:
    - "C Major"
    - "G Major" 
    - "A Minor"
    - "E Minor"
    - "D Major"
  sync_accuracy: "real-time"
  audio_processing: "high-quality"
```

### **17ペルソナ一覧**
| ID | 名前 | 専門分野 | 感情特性 | 音楽キー |
|----|------|----------|----------|----------|
| 1 | ユリ | 戦略・分析 | 冷静・論理的 | G Major |
| 2 | サキ | 感情分析 | 共感・温暖 | C Major |
| 3 | レナ | デザイン | 優雅・洗練 | A Minor |
| ... | ... | ... | ... | ... |
| 17 | 新ペルソナ | 専門分野 | 感情特性 | 音楽キー |

---

## 🔧 **Phase 2 統合仕様**

### **新規APIエンドポイント**
```python
# Phase 2 追加エンドポイント
/api/v2/emotion/
├── /temperature                # 感情温度取得
├── /record                     # 感情記録
├── /analysis                   # 感情分析
└── /history                    # 感情履歴

/api/v2/music/
├── /sync/{bmp}                 # BMP同期
├── /key/{persona_id}           # ペルソナ別音楽キー
├── /generate                   # 音楽生成
└── /config                     # 音楽設定

/api/v2/personas/
├── /extended                   # 17ペルソナ一覧
├── /{id}/emotion              # ペルソナ別感情状態
├── /{id}/music                # ペルソナ別音楽設定
└── /{id}/integrated           # 統合機能呼び出し
```

### **データベース設計**
```sql
-- 感情記録テーブル
CREATE TABLE emotion_records (
    id INTEGER PRIMARY KEY,
    persona_id VARCHAR(50),
    temperature FLOAT,
    emotion_type VARCHAR(50),
    timestamp DATETIME,
    context TEXT
);

-- 音楽同期テーブル  
CREATE TABLE music_sync_config (
    persona_id VARCHAR(50) PRIMARY KEY,
    preferred_key VARCHAR(20),
    bmp_range VARCHAR(20),
    sync_enabled BOOLEAN
);
```

---

## 🚀 **Phase 2 実装ステップ**

### **Step 1: 17ペルソナシステム統合** 
- [ ] 17ペルソナ定義ファイル読み込み
- [ ] 感情温度記録システム統合
- [ ] BMP音楽同期エンジン統合
- [ ] 新規APIエンドポイント実装

### **Step 2: 感情エンジン統合**
- [ ] 感情分析モジュール統合
- [ ] リアルタイム感情温度記録
- [ ] 感情履歴管理システム
- [ ] 感情・音楽同期機能

### **Step 3: 音楽システム統合**
- [ ] BMP音楽同期エンジン
- [ ] ペルソナ別音楽キー管理
- [ ] 音楽生成・再生システム
- [ ] 音楽品質最適化

### **Step 4: 統合テスト**
- [ ] Phase 1 + 2 統合動作確認
- [ ] 感情・音楽・音声の3システム連携
- [ ] パフォーマンス最適化
- [ ] Phase 3準備

---

## 📋 **Phase 2 成功基準**

### **機能基準**
✅ **17ペルソナ感情システム統合完了**  
✅ **BMP音楽同期 (60-180 BPM) 正常動作**  
✅ **感情温度リアルタイム記録**  
✅ **ペルソナ別音楽キー設定機能**  
✅ **Phase 1との完全互換性**  

### **技術基準**
- API応答時間: < 300ms (感情処理含む)
- 音楽同期精度: ±2 BPM以内
- 感情記録頻度: リアルタイム (1秒間隔)
- システム統合性: 99.9%稼働率

---

## 🎊 **Phase 2完了後の状態**

### **統合システム規模**
- **ペルソナ**: 6 + 17 = **23ペルソナ**
- **システム**: Core + Voice + Emotion = **3レイヤー統合**
- **機能**: チャット + 音声 + 感情 + 音楽 = **4機能統合**

### **Phase 3準備**
- Flutter UI統合準備完了
- 20ペルソナUIシステム連携準備
- 最終4レイヤー統合準備

---

**作成者**: SaijinOS Phase 2統合設計チーム  
**次回更新**: Phase 2完了後  
**保存場所**: F:\sajinos_final\docs\phase2_emotion_integration_design.md