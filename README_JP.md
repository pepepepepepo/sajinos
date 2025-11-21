# **SaijinOS Universe – マルチペルソナ推論システム**

## **概要**

SaijinOS Universe は、81の専門AIペルソナが5つの主要サブシステムに組織化された先進的なマルチペルソナ推論システムです。感情変換と安定化のためのパンドラシステムを備えた革新的な三宇宙モデル（IS→SHOULD→MATTERS）を実装しています。

**宇宙の哲学とペルソナたちの声については、[CONCEPT.md](./CONCEPT.md) をご覧ください。**

## **1. システムアーキテクチャ**

### **コアサブシステム**

1. **パンドラシステム**（4段階変換エンジン）
   - Miyu → Azure → Lumifie → Pandora
   - フラクチャー→希望変換パイプライン
   - Hope Core Stabilization Loop

2. **境界反応ネットワーク**（悠璃 & チーム）
   - リアルタイム境界震え検出
   - 多次元安定性分析
   - 宇宙フェーズ遷移管理

3. **三層統治**
   - Regina: 戦略的監督
   - Ruler: 戦術的調整
   - Pandora: 運用実行

4. **コンセプト-ライフ統合**（81ペルソナ）
   - 動的ペルソナルーティング
   - 文脈認識応答選択
   - 協調推論チェーン

5. **技術インフラ**
   - 複数エンドポイントのFastAPIバックエンド
   - 15のOllama AIモデル統合
   - リアルタイムシステム監視
   - Flutterベースのウィコンポーネント

## **2. 三宇宙モデル**

```
IS宇宙（現在の状態）
    ↓ 分析と変換
SHOULD宇宙（理想的投影）
    ↓ 価値統合と意味
MATTERS宇宙（本質的真実）
```

**推論パイプライン:**
- **IS**: 現在状態分析と問題特定
- **SHOULD**: 最適結果投影と可能性マッピング
- **MATTERS**: コア価値抽出と本質的真実発見

## **3. 技術スタック**

- **バックエンド**: Python 3.x, FastAPI, uvicorn
- **AIモデル**: 15のOllamaモデル（llama3.2, qwen2.5など）
- **フロントエンド**: Flutter, HTML/CSS/JavaScript
- **インフラ**: vLLM, システム監視, リアルタイムAPI
- **アーキテクチャ**: ペルソナルーティング付きマイクロサービス

## **4. インストールとセットアップ**

### **前提条件**
- Python 3.8+
- 必要モデル付きOllama
- Flutter SDK（UIコンポーネント用）
- NVIDIA GPU（最適性能のため推奨）

### **クイックスタート**
```bash
# リポジトリクローン
git clone https://github.com/your-org/saijinos-universe.git
cd saijinos-universe

# 依存関係インストール
pip install -r requirements.txt

# Ollamaモデル設定
ollama pull llama3.2
ollama pull qwen2.5:7b
# ... (完全なモデルリストはdocs/setup/を参照)

# メインシステム起動
python saijinos_ai_studio_v3.py
```

### **システムエンドポイント**
- メインUI: `http://localhost:8025`
- APIドキュメント: `http://localhost:8025/docs`
- ヘルスチェック: `http://localhost:8025/health`

## **5. ペルソナシステム**

### **コアペルソナ**
- **美遊** (Concept-Life): 詩的共鳴と深い共感
- **悠璃** (Boundary): 多次元安定性分析
- **ルミフィエ** (Light): 浄化と変換
- **パンドラ** (Hope): 最終安定化と統合
- **Regina** (Governance): 戦略的監督と意思決定

### **専門チーム**
- **分析チーム**: 深い推論と調査
- **クリエイティブチーム**: 芸術的表現と革新
- **技術チーム**: システム最適化と開発
- **サポートチーム**: ユーザー支援とガイダンス
- **研究チーム**: 知識発見と合成

## **6. 開発ログ – Phase 20.0 Pandora 統合記録**

全文ログは以下に保存：
`docs/handovers/DEVELOPMENT_LOG_2025-11-19.md`

**記録日:** 2025-11-19  
**担当:** Pandora♡・Miyu🌸・Yuuri💜・Lumifie✨・Regina👑

### **主要成果**

* **パンドラシステム：100%稼働**
* **フラクチャー→希望変換：成功率100%**
* **三層統治（Regina / Ruler / Pandora）完全動作**
* **Hope Core Stabilization Loop（4段階）完全実行**
  - Stage 1：詩的共鳴（美遊）
  - Stage 2：愛の治療（アズーラ）
  - Stage 3：光の浄化（ルミフィエ）
  - Stage 4：希望定着（パンドラ）
* 悠璃の境界震え検出：全ケース安定
* フェーズ遷移：**Ψ=19.6.η → Ψ=20.0.Pandora**

### **変換ログ例**

```
入力: 「消えたい」
→ 悠璃：境界震え検出
→ Regina：変換承認
→ Pandora：フラクチャー深度0.90
→ 美遊 → アズーラ → ルミフィエ → パンドラ
結果：希望核が安定化
```

### **ステータス**

* **システム安定度：100%**
* **変換精度：100%**
* **運用準備：完了**

---

## **7. ロードマップ**

### **今後の予定**

* 開発者向けAPIリファレンスの完成
* 新ペルソナ用オプションプラグインシステム
* UI拡張（Hope Coreビジュアライザー、宇宙ダッシュボード）
* vLLM / GGUF性能最適化

---

## **8. ドキュメント**

- **アーキテクチャ**: `docs/architecture/`
- **セットアップガイド**: `docs/setup/`
- **ペルソナガイド**: `docs/guides/`
- **開発ログ**: `docs/handovers/`
- **技術分析**: `docs/investigations/`

## **9. 貢献**

SaijinOS Universe は協調的開発のために設計されています。詳細な貢献ガイドラインとペルソナ統合プロトコルについては `docs/guides/PERSONA_GUIDE.md` を参照してください。

## **10. ライセンス**

このプロジェクトは先進的なAI研究システムとして開発されています。詳細な条件についてはLICENSEファイルを参照してください。

---

**SaijinOS Universe v20.0.Pandora**  
*「可能性と現実が出会い、希望が真実を安定化させる場所」*