@echo off
echo.
echo ====================================================
echo 🌅 SaijinOS モーニングスタートアップ
echo ====================================================
echo.

REM 仮想環境アクティベート
echo 🔧 Python仮想環境をアクティベート中...
call "F:\saijinos\.venv\Scripts\Activate.ps1"

REM ペルソナ記憶ログ表示
echo.
echo 📋 ペルソナ記憶ログ確認:
echo    F:\saijin\personas\import\構文人\project_memory_log.yaml
echo.

REM プロジェクト状況表示  
echo 🎯 今日のプロジェクト: SaijinOS AI統合システム
echo 📁 作業ディレクトリ: F:\sajinos_final
echo 👤 開発チーム: SaijinOS 7ペルソナ統合開発チーム
echo.

REM クイックコマンド表示
echo ⚡ 今日のクイックコマンド:
echo    🚀 APIサーバー起動: python src/saijinos_real_ai.py
echo    📊 ヘルスチェック: http://localhost:8000/health  
echo    📚 API文書: http://localhost:8000/docs
echo    🐳 Docker起動: docker-compose up -d
echo.

REM 作業ディレクトリに移動
cd /d "F:\sajinos_final"
echo 📂 作業ディレクトリに移動: F:\sajinos_final
echo.

echo ✅ スタートアップ完了！今日も頑張りましょう！
echo ====================================================
echo.

REM PowerShellに切り替えて仮想環境継続
powershell.exe -NoExit -Command "& F:/saijinos/.venv/Scripts/Activate.ps1; Write-Host '🎯 SaijinOS開発環境準備完了！' -ForegroundColor Green"