@echo off
chcp 65001 >nul
REM SaijinOS 朝のクイックスタート
REM ダブルクリックで実行可能

echo 🌅 SaijinOS クイックスタート
echo PowerShell版モーニングスタートアップを実行します...
echo.

REM PowerShell実行ポリシー一時変更してスクリプト実行
powershell.exe -ExecutionPolicy Bypass -File "F:\sajinos_final\scripts\morning_startup.ps1"

echo.
echo スタートアップ完了！Enterキーを押して終了...
pause >nul