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

## **6. ハイブリッドAIシステム設計 – Phase 20.3**

### **AIモデル最終構成（17個、総容量約54GB）**

SaijinOS は**クラウド会話システム**と**専門ローカルモデル**を組み合わせたハイブリッドAI構成を採用しています：

#### **☁️ クラウド会話レイヤー**
- **Gemini 1.5 Flash** + Google検索統合
- 主要用途：日常会話、Web検索統合Q&A、作業分析・統合
- コスト効率：無料枠（1日1500リクエスト）、有料版（入力$0.075/1M、出力$0.30/1M）
- パフォーマンス：応答1-2秒、高品質（Pro版の80%）

#### **🏠 ローカル専門モデル（用途別完全分離稼働）**

**画像処理（1個 - 4.7GB）**
- `llava:7b` - マルチモーダルAI、画像解析・生成

**統計分析（1個 - 4.7GB）**
- `qwen2.5:7b-instruct` - データ分析、統計処理

**音楽・詩的表現（2個 - 3GB）**
- `llama3.2:1b-instruct-q4_k_m` (807MB) - 軽量詩的表現
- `phi3.5:3.8b-mini-instruct-q4_0` (2.2GB) - 高品質音楽生成

**会話用（5個 - 約25GB）**
- `Miyu:7b` - 美遊（感情表現豊か）
- `MiyuJP:7b` - 美遊JP（日本語最適化）
- `llama3.1:8b-instruct` - 高度会話
- `nous-hermes2:latest` - 汎用会話
- `mistral:7b-instruct` - 効率的対話

**コード開発（3個 - 約15GB）**
- `starcoder2:7b` - プログラミング専門
- `deepseek-coder:6.7b` - コード生成特化
- `codellama:7b-instruct` - コード解説

**感情サポート（5個 - 約6GB）**
- `phi3:mini` - 感情理解
- `gemma2:2b-instruct` - 軽量感情
- `qwen2.5:1.5b-instruct` - 小型汎用
- `llama3.2:1b-instruct` - 軽量詩的
- `tinyllama:1.1b` - 超軽量補助

### **🔄 理想的ワークフロー設計**

**完全分離作業モード**（12GB VRAM環境最適化）：

```
1. コード開発作業 → starcoder2:7b（単独稼働）
   ↓ 結果保存
2. 画像生成作業 → llava:7b（単独稼働）
   ↓ 結果保存
3. 音楽創作 → phi3.5 + llama3.2（軽量並列可）
   ↓ 結果保存
4. 統合分析 → Gemini Flash + Google検索
   ↓ YAML作業履歴参照 + Web最新情報
5. 次タスク計画立案
```

### **開発継続性システム**

**YAML形式のセッションログ**：
- `docs/logs/SESSION_LOG_*.yaml` - 機械可読作業履歴
- `docs/logs/SYSTEM_STATE.yaml` - リアルタイムプロジェクト状態追跡
- AIエージェント間の完全な継続性を確保

**プロジェクト管理ツール**：
- `tools/dev/log_manager.py` - Git統合自動ログ管理
- `tools/dev/project_manager.py` - プロジェクト構造完全追跡

---

## **7. ロードマップ**

### **今後の予定（Phase 20.3 - ハイブリッドAI実装）**

* **Gemini API統合**（最優先）
  - Google APIキー設定
  - Gemini Flash + 検索機能統合
  - 会話APIエンドポイント作成
  
* **作業モード切り替えシステム**（高優先）
  - Ollamaモデル動的起動/停止
  - VRAM使用量監視システム
  - FastAPIモード切り替えエンドポイント

* **作業履歴統合**（中優先）
  - YAMLセッション履歴検索機能
  - 会話モードからの履歴参照統合
  - 作業結果の自動保存

* **Flutter UI更新**（中優先）
  - モード切り替えインターフェース
  - 作業履歴ビューアパネル
  - リアルタイムVRAM表示

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

**SaijinOS Universe v20.3.HybridAI**  
*「可能性と現実が出会い、希望が真実を安定化させる場所」*  
*Last Updated: 2025-11-23*  
*Repository: https://github.com/pepepepepepo/sajinos.git*