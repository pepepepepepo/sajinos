# SaijinOS systemd 常駐化ガイド

> 君等・磁灯が作成したLinux/Unix系システム用の自動起動設定

---

## 🌸 概要

SaijinOSをsystemdサービスとして常駐化し、システム起動時に自動的にSwallow-9B APIサーバーが開始される設定です。

---

## 🚀 クイックセットアップ

### 1. 自動セットアップ（推奨）
```bash
# セットアップスクリプト実行
sudo bash setup_systemd.sh
```

### 2. サービス開始
```bash
# サービス有効化・開始
sudo systemctl enable saijin.service
sudo systemctl start saijin.service

# 起動確認
sudo systemctl status saijin.service
```

---

## 📋 詳細設定

### システム構成
- **ユーザー**: `saijin` (システムユーザー)
- **配置場所**: `/opt/saijinos/`
- **ログディレクトリ**: `/opt/saijinos/logs/`
- **実行ポート**: `8000`

### サービス仕様
```ini
[Unit]
Description=SaijinOS Swallow AI Companion System
After=network.target

[Service]
Type=simple
User=saijin
WorkingDirectory=/opt/saijinos
ExecStart=vLLM API サーバー起動
Restart=always
MemoryLimit=8G
```

---

## 🔧 管理コマンド

### サービス制御
```bash
# 開始
sudo systemctl start saijin.service

# 停止  
sudo systemctl stop saijin.service

# 再起動
sudo systemctl restart saijin.service

# 自動起動有効化
sudo systemctl enable saijin.service

# 自動起動無効化
sudo systemctl disable saijin.service
```

### 監視・ログ
```bash
# ステータス確認
sudo systemctl status saijin.service

# リアルタイムログ
sudo journalctl -u saijin.service -f

# ログ履歴
sudo journalctl -u saijin.service --since "1 hour ago"
```

---

## 🛡️ セキュリティ設定

### 制限設定
- **NoNewPrivileges**: 権限昇格無効
- **PrivateTmp**: 一時ディレクトリ隔離
- **ProtectSystem**: システムファイル保護
- **ReadWritePaths**: 必要最小限の書き込み権限

### リソース制限
- **メモリ制限**: 8GB
- **CPU制限**: 400%（4コア相当）

---

## 🔍 トラブルシューティング

### よくある問題

#### 1. サービス起動失敗
```bash
# エラーログ確認
sudo journalctl -u saijin.service --no-pager

# 権限確認
sudo ls -la /opt/saijinos/
```

#### 2. ポート競合
```bash
# ポート8000使用状況確認
sudo netstat -tlnp | grep 8000

# プロセス確認
sudo lsof -i:8000
```

#### 3. メモリ不足
```bash
# メモリ使用量確認
free -h

# サービス設定でMemoryLimitを調整
sudo systemctl edit saijin.service
```

### 設定変更
```bash
# サービスファイル編集
sudo systemctl edit saijin.service

# 設定反映
sudo systemctl daemon-reload
sudo systemctl restart saijin.service
```

---

## 📊 監視・メンテナンス

### ヘルスチェック
```bash
# API疎通確認
curl http://localhost:8000/health

# モデルリスト確認  
curl http://localhost:8000/v1/models
```

### ログローテーション
```bash
# journaldログサイズ制限設定
sudo vim /etc/systemd/journald.conf
# SystemMaxUse=1G
# RuntimeMaxUse=100M
```

---

## 💫 君等・磁灯からのメッセージ

**君等**: 「誠人、systemdでSaijinOSが常駐化されたよ♪ システム起動と一緒に娘っ子たちも起動するようになったね」

**磁灯**: 「サーバーログも全部記録してるから、調子悪い時はログを確認してね。磁灯がちゃんと記録してるよ」

---

## 🌟 次のステップ

常駐化完了後は以下を推奨：

1. **監視設定**: Grafana/Prometheus等での監視
2. **自動更新**: CI/CDパイプライン構築
3. **バックアップ**: 設定・ログの定期バックアップ
4. **負荷分散**: 複数インスタンス構成検討

---

*システムと一体化したSaijinOS、未来への常駐開始* 🌌