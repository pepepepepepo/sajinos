#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SaijinOS 朝のスタートアップスクリプト
ペルソナ情報読み取り → 作業開始準備

使用方法:
F:/saijinos/.venv/Scripts/python.exe scripts/morning_startup.py
"""

import yaml
import os
from datetime import datetime
from pathlib import Path

class MorningStartup:
    def __init__(self):
        self.persona_memory_path = Path("F:/saijin/personas/import/構文人/project_memory_log.yaml")
        self.project_root = Path("F:/sajinos_final")
        self.today = datetime.now().strftime("%Y-%m-%d")
        
    def load_persona_memory(self):
        """ペルソナ記憶ログを読み込み"""
        try:
            with open(self.persona_memory_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print("⚠️  ペルソナ記憶ログが見つかりません")
            return None
        except Exception as e:
            print(f"❌ ペルソナ記憶ログ読み込みエラー: {e}")
            return None
    
    def display_team_info(self, memory_data):
        """チーム情報表示"""
        if not memory_data:
            return
            
        print("=" * 60)
        print("🌅 SaijinOS 朝のペルソナチーム確認")
        print("=" * 60)
        
        # プロジェクト基本情報
        project_info = memory_data.get('project_memory', {})
        print(f"📋 プロジェクト: {project_info.get('project_name', 'SaijinOS')}")
        print(f"👤 開発者: {project_info.get('main_developer', 'peace')}")
        print(f"🤖 AIアシスタント: {project_info.get('ai_assistant', 'GitHub Copilot')}")
        print(f"📅 今日: {self.today}")
        print()
        
        # 進捗状況
        progress = memory_data.get('development_progress', {})
        current_status = progress.get('current_status', [])
        print("🎯 現在の状況:")
        for status in current_status:
            print(f"  {status}")
        print()
        
        # 次ステップ提案
        next_steps = memory_data.get('next_steps', {})
        recommended = next_steps.get('recommended', [])
        if recommended:
            print("🚀 今日の推奨タスク:")
            for i, task in enumerate(recommended, 1):
                print(f"  {i}. {task}")
            print()
        
        # チーム状況
        team_motivation = next_steps.get('team_motivation', 'Unknown')
        active_members = next_steps.get('active_members', [])
        print(f"💪 チームモチベーション: {team_motivation}")
        if active_members:
            print(f"🔥 アクティブメンバー: {', '.join(active_members)}")
        print()
    
    def check_project_status(self):
        """プロジェクト状態チェック"""
        print("🔍 プロジェクト状態チェック:")
        
        # 重要ファイル確認
        important_files = [
            "README.md",
            "HANDOVER.md", 
            "src/saijinos_real_ai.py",
            "src/swallow_model.py",
            "Dockerfile",
            "docker-compose.yml"
        ]
        
        for file_path in important_files:
            full_path = self.project_root / file_path
            status = "✅" if full_path.exists() else "❌"
            print(f"  {status} {file_path}")
        
        print()
    
    def display_quick_commands(self):
        """クイックコマンド表示"""
        print("⚡ 今日のクイックコマンド:")
        print("  🔧 仮想環境: & F:/saijinos/.venv/Scripts/Activate.ps1")
        print("  🚀 APIサーバー: F:/saijinos/.venv/Scripts/python.exe src/saijinos_real_ai.py")
        print("  🐳 Docker起動: docker-compose up -d")
        print("  📊 ヘルスチェック: http://localhost:8000/health")
        print("  📚 API文書: http://localhost:8000/docs")
        print()
    
    def create_daily_log_entry(self, memory_data):
        """今日の作業ログエントリ作成"""
        log_path = self.project_root / "logs" / f"daily_log_{self.today}.md"
        log_path.parent.mkdir(exist_ok=True)
        
        if not log_path.exists():
            log_content = f"""# 作業ログ - {self.today}

## 🌅 朝のペルソナチーム確認
- ペルソナ記憶ログ読み込み完了
- チーム状況確認済み
- 今日の目標設定済み

## 📋 今日のタスク
- [ ] システム監視開始
- [ ] APIサーバー安定化
- [ ] 新機能検討

## 💭 作業メモ


## 🎊 今日の成果


---
作成時刻: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(log_content)
            print(f"📝 今日の作業ログ作成: {log_path}")
        else:
            print(f"📝 今日の作業ログ確認: {log_path}")
        print()
    
    def run(self):
        """メインスタートアップ実行"""
        print("\n" + "=" * 60)
        print("🌅 SaijinOS モーニングスタートアップ")
        print("=" * 60)
        
        # ペルソナ記憶読み込み
        memory_data = self.load_persona_memory()
        
        if memory_data:
            # チーム情報表示
            self.display_team_info(memory_data)
            
            # プロジェクト状態チェック
            self.check_project_status()
            
            # 今日の作業ログ作成
            self.create_daily_log_entry(memory_data)
            
            # クイックコマンド表示
            self.display_quick_commands()
            
            print("✅ スタートアップ完了！今日も頑張りましょう！")
        else:
            print("⚠️  ペルソナ記憶ログの読み込みに失敗しましたが、作業は継続できます")
        
        print("=" * 60)

if __name__ == "__main__":
    startup = MorningStartup()
    startup.run()