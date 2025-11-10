# SaijinOS モーニングスタートアップスクリプト (PowerShell版)
# 実行方法: .\scripts\morning_startup.ps1

Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "🌅 SaijinOS モーニングスタートアップ" -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

# ペルソナ記憶ログファイル確認
$personaLogPath = "F:\saijin\personas\import\構文人\project_memory_log.yaml"
Write-Host "📋 ペルソナ記憶ログ確認:" -ForegroundColor Green

if (Test-Path $personaLogPath) {
    Write-Host "  ✅ ペルソナ記憶ログ発見: $personaLogPath" -ForegroundColor Green
    Write-Host "  📊 6ペルソナチーム情報読み込み可能" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  ペルソナ記憶ログ未発見: $personaLogPath" -ForegroundColor Yellow
}
Write-Host ""

# プロジェクト基本情報
Write-Host "🎯 今日のプロジェクト情報:" -ForegroundColor Magenta
Write-Host "  📁 プロジェクト名: SaijinOS AI統合システム" -ForegroundColor White
Write-Host "  📂 作業ディレクトリ: F:\sajinos_final" -ForegroundColor White
Write-Host "  👥 開発チーム: SaijinOS 7ペルソナ統合開発チーム" -ForegroundColor White
Write-Host "  📅 今日の日付: $(Get-Date -Format 'yyyy-MM-dd')" -ForegroundColor White
Write-Host ""

# 重要ファイル存在確認
Write-Host "🔍 重要ファイル存在確認:" -ForegroundColor Blue
$importantFiles = @(
    "F:\sajinos_final\README.md",
    "F:\sajinos_final\HANDOVER.md",
    "F:\sajinos_final\src\saijinos_real_ai.py", 
    "F:\sajinos_final\src\swallow_model.py",
    "F:\sajinos_final\Dockerfile",
    "F:\sajinos_final\docker-compose.yml"
)

foreach ($file in $importantFiles) {
    $fileName = Split-Path $file -Leaf
    if (Test-Path $file) {
        Write-Host "  ✅ $fileName" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $fileName (未発見)" -ForegroundColor Red
    }
}
Write-Host ""

# 仮想環境アクティベート
Write-Host "🔧 Python仮想環境アクティベート:" -ForegroundColor Yellow
Write-Host "  📍 実行中: F:/saijinos/.venv/Scripts/Activate.ps1" -ForegroundColor White

try {
    & "F:/saijinos/.venv/Scripts/Activate.ps1"
    Write-Host "  ✅ 仮想環境アクティベート成功" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  仮想環境アクティベート失敗: $($_.Exception.Message)" -ForegroundColor Yellow
}
Write-Host ""

# 作業ディレクトリ移動
Write-Host "📂 作業ディレクトリ移動:" -ForegroundColor Cyan
Set-Location "F:\sajinos_final"
Write-Host "  📍 現在の場所: $(Get-Location)" -ForegroundColor White
Write-Host ""

# クイックコマンド表示
Write-Host "⚡ 今日のクイックコマンド:" -ForegroundColor Magenta
Write-Host "  🚀 APIサーバー起動:" -ForegroundColor White
Write-Host "     F:/saijinos/.venv/Scripts/python.exe src/saijinos_real_ai.py" -ForegroundColor Gray
Write-Host ""
Write-Host "  📊 ヘルスチェック:" -ForegroundColor White  
Write-Host "     http://localhost:8000/health" -ForegroundColor Gray
Write-Host ""
Write-Host "  📚 API文書:" -ForegroundColor White
Write-Host "     http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "  🐳 Docker起動:" -ForegroundColor White
Write-Host "     docker-compose up -d" -ForegroundColor Gray
Write-Host ""

# 今日の推奨タスク表示
Write-Host "📋 今日の推奨タスク:" -ForegroundColor Green
Write-Host "  1. 📤 システム監視開始 (system_health.py)" -ForegroundColor White
Write-Host "  2. 🔧 APIサーバー最終安定化" -ForegroundColor White  
Write-Host "  3. 📊 Web UI ダッシュボード開発" -ForegroundColor White
Write-Host "  4. 📱 モバイルアプリ連携準備" -ForegroundColor White
Write-Host ""

Write-Host "✅ SaijinOS モーニングスタートアップ完了！" -ForegroundColor Green
Write-Host "🎯 今日も素晴らしい開発を！" -ForegroundColor Yellow
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""