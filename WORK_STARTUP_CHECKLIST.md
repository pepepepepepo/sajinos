# 🚀 Saijin開発 作業開始前チェックリスト

## 📋 作業前必須チェック

### ⚡ クイックステータス確認
- [ ] 前回の引継書を確認（`docs/handovers/` 最新日付）
- [ ] 未解決の技術課題を把握
- [ ] 今日の目標を明確化
- [ ] 開発環境の状態確認

### 🔧 環境チェック
- [ ] Python仮想環境アクティブ化: `F:/saijinos/.venv/Scripts/Activate.ps1`
- [ ] Git作業ディレクトリ: `F:/saijinos/github_sajinos`
- [ ] ローカル統合システム: `F:/saijinos/saijinos_main_integration`
- [ ] AIモデル: `E:\AI_Models\saijin-swallow\models\`

### 📊 システム状態確認
- [ ] APIサーバー状態: `python F:/saijinos/saijinos_main_integration/start_api_server.py`
- [ ] データベース: `integration.db` 存在確認
- [ ] モデルファイル: TinyLlama正常配置確認
- [ ] 前回エラー: ログファイル確認

## 🎯 現在の最重要課題（引継書より）

### 🚨 優先度：緊急
1. **APIサーバー起動エラー修正**
   - 状況: `start_api_server.py` で断続的エラー
   - 原因候補: モデルパス・メモリ・依存関係
   - 対処: 段階的デバッグ実施

### ⚡ 優先度：高
1. **統合テスト実施**
   - ツール: `routing_test.py`
   - 目的: 全エンドポイント動作確認
   - 期待: 80%以上のテスト成功率

2. **システム監視強化**
   - ツール: `system_health.py`
   - 目的: リアルタイム監視開始
   - 期待: 24時間稼働監視

### 🎵 優先度：中
1. **音声システム拡張**
   - 機能: BPM同期実装
   - 設定: `voice_config.yaml`, `bpm_config.yaml`
   - 目標: ペルソナ別音楽的表現

## 📚 前回からの継続項目

### ✅ 完成済み項目
- [x] 完全ドキュメントシステム構築
- [x] 6ペルソナシステム詳細設計
- [x] GitHub公開リポジトリ完成
- [x] BPM同期設定ファイル作成
- [x] 包括的テスト・監視ツール作成

### 🔄 進行中項目
- [ ] APIサーバー安定化
- [ ] 統合テスト実施・改善
- [ ] 音声品質向上
- [ ] パフォーマンス最適化

### 📝 未着手項目
- [ ] Web UI開発
- [ ] モバイルアプリ検討
- [ ] クラウド展開準備
- [ ] セキュリティ強化

## 🛠️ よく使うコマンド集

### 開発環境
```powershell
# 仮想環境アクティブ化
& F:/saijinos/.venv/Scripts/Activate.ps1

# APIサーバー起動
cd F:/saijinos/saijinos_main_integration
python start_api_server.py

# データベース初期化
python setup_database.py

# 統合テスト実行
python F:/saijinos/.venv/routing_test.py

# システム監視開始
python F:/saijinos/.venv/system_health.py --mode continuous
```

### Git操作
```powershell
cd F:/saijinos/github_sajinos
git status
git add .
git commit -m "✨ [作業内容]"
git push origin main
```

### デバッグ用
```powershell
# モデルパス確認
Get-ChildItem "E:\AI_Models\saijin-swallow\models\" -Recurse -Name

# ログ確認
Get-Content F:/saijinos/saijinos_main_integration/logs/error.log -Tail 50

# プロセス監視
Get-Process python*
```

## 💡 成功パターン（過去の学び）

### 🎯 効果的な開発手順
1. **小さく始める**: 一度に多機能実装せず段階的に
2. **テスト優先**: 実装と同時にテスト作成
3. **詳細ログ**: 問題解決に不可欠
4. **ドキュメント同時**: 後回しにしない

### ⚠️ 回避すべきパターン
1. **大規模変更**: 一度に多くを変更すると原因特定困難
2. **テスト後回し**: バグの早期発見が困難
3. **エラー無視**: 小さなエラーが大きな問題に発展
4. **環境依存**: 絶対パス使用・Windows依存の注意

## 🔍 デバッグチェックポイント

### APIサーバーエラー時
- [ ] Python環境: 仮想環境正しくアクティブか
- [ ] 依存関係: `pip list` で必要パッケージ確認
- [ ] モデルパス: TinyLlamaファイル存在確認
- [ ] メモリ: 4GB以上の空きメモリ確認
- [ ] ポート: 8000番ポート占有状況確認

### 音声システムエラー時
- [ ] Windows環境: SAPI音声エンジン利用可能か
- [ ] 音声設定: `voice_config.yaml` 正しく読み込まれているか
- [ ] ファイル権限: 音声出力ディレクトリ書き込み可能か
- [ ] ペルソナ設定: 選択されたペルソナが存在するか

## 📈 パフォーマンス目標

### 応答時間目標
- チャット応答: < 2秒
- 音声生成: < 5秒
- 統合処理: < 8秒
- ヘルスチェック: < 1秒

### 品質目標
- API稼働率: > 99%
- テスト成功率: > 90%
- ユーザー満足度: > 8.5/10
- ペルソナ識別率: > 95%

## 🎉 作業完了時チェック

### 💾 保存・記録
- [ ] 変更内容をGitコミット
- [ ] 重要な発見を引継書に記録
- [ ] エラーと解決方法を文書化
- [ ] 次回作業予定を明確化

### 🧪 テスト確認
- [ ] 変更箇所の動作テスト
- [ ] 回帰テスト（既存機能破損なし）
- [ ] パフォーマンス測定
- [ ] エラーハンドリング確認

### 📋 引継準備
- [ ] 今日の成果を引継書に記録
- [ ] 未解決課題の整理
- [ ] 次回優先事項の設定
- [ ] 環境・設定変更の記録

---

## 📚 関連リソース

### ドキュメント
- [システム設計書](docs/ARCHITECTURE.md)
- [ペルソナガイド](docs/PERSONA_GUIDE.md)
- [最新引継書](docs/handovers/) - 日付順
- [プロジェクト概要](README.md)

### 設定ファイル
- [音声設定](voice_config.yaml)
- [BPM設定](bpm_config.yaml)
- [リポジトリ構造](repo_structure.yaml)

### ツール
- [APIテスト](routing_test.py)
- [システム監視](system_health.py)
- [ヘルスチェック](http://127.0.0.1:8000/health)
- [API文書](http://127.0.0.1:8000/docs)

---

**💡 このチェックリストを毎回の作業開始時に確認することで、効率的で品質の高い開発を継続できます！**

**最終更新**: 2025年11月6日  
**次回更新**: 重要な発見・変更時に随時