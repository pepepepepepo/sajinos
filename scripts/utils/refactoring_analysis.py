#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SaijinOS Creative Studio - モジュール分割リファクタリング計画

⚠️ 現在の問題:
- creative_studio_multimodel_dashboard.py: 283KB, 6949行
- HTMLテンプレート・CSS・JavaScript・Pythonコードが1ファイルに混在
- 保守性・可読性・パフォーマンスに深刻な問題

🎯 リファクタリング戦略:
1. テンプレート分離 (templates/)
2. 静的ファイル分離 (static/)
3. APIルート分離 (api/)
4. ペルソナロジック分離 (personas/)
5. コア機能分離 (core/)

📁 新しいアーキテクチャ:
src/
├── main.py                 # FastAPIメインアプリ (100-200行)
├── api/                    # API エンドポイント
│   ├── __init__.py
│   ├── chat.py            # チャット API
│   ├── workspace.py       # ワークスペース管理
│   └── persona.py         # ペルソナ管理
├── core/                   # コア機能
│   ├── __init__.py
│   ├── persona_manager.py # ペルソナ管理ロジック
│   ├── workspace_manager.py # ワークスペース管理
│   └── vibration_system.py # 4振動システム
├── templates/              # HTMLテンプレート
│   ├── base.html          # ベーステンプレート
│   ├── chat.html          # チャットUI
│   ├── development.html   # 開発UI
│   ├── music.html         # 音楽UI
│   └── analysis.html      # 分析UI
└── static/                 # 静的ファイル
    ├── css/
    │   ├── main.css
    │   ├── workspace.css
    │   └── components.css
    └── js/
        ├── main.js
        ├── chat.js
        ├── workspace.js
        └── music.js
"""

import os
from pathlib import Path

class SaijinOSRefactoring:
    """SaijinOS モジュール分割リファクタリング"""
    
    def __init__(self, base_path="F:/saijinos"):
        self.base_path = Path(base_path)
        self.current_file = self.base_path / ".venv" / "creative_studio_multimodel_dashboard.py"
        self.src_path = self.base_path / "src"
        
    def analyze_current_file(self):
        """現在のファイルサイズと構造を分析"""
        if self.current_file.exists():
            stat = self.current_file.stat()
            with open(self.current_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            return {
                "file_size_kb": stat.st_size / 1024,
                "total_lines": len(lines),
                "python_lines": len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
                "html_lines": len([l for l in lines if '<' in l or '>' in l]),
                "css_lines": len([l for l in lines if any(css in l for css in ['style', '{', '}', 'px', 'color'])]),
                "js_lines": len([l for l in lines if any(js in l for js in ['function', 'const', 'let', 'var', '=>'])])
            }
        return {"error": "File not found"}
    
    def create_directory_structure(self):
        """新しいディレクトリ構造を作成"""
        directories = [
            self.src_path / "api",
            self.src_path / "core", 
            self.src_path / "templates",
            self.src_path / "static" / "css",
            self.src_path / "static" / "js"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            # __init__.py をPythonパッケージに追加
            if directory.name in ["api", "core"]:
                init_file = directory / "__init__.py"
                if not init_file.exists():
                    init_file.write_text("# -*- coding: utf-8 -*-\n")
        
        return [str(d) for d in directories]
    
    def get_refactoring_priority(self):
        """リファクタリング優先度"""
        analysis = self.analyze_current_file()
        
        if "error" in analysis:
            return {"priority": "low", "reason": "File not accessible"}
        
        if analysis["file_size_kb"] > 200:  # 200KB以上
            return {
                "priority": "critical",
                "reason": f"File size: {analysis['file_size_kb']:.1f}KB is too large",
                "recommended_action": "immediate_refactoring",
                "target_reduction": "80-90%"
            }
        elif analysis["total_lines"] > 3000:  # 3000行以上
            return {
                "priority": "high", 
                "reason": f"Line count: {analysis['total_lines']} is excessive",
                "recommended_action": "modular_refactoring"
            }
        else:
            return {"priority": "low", "reason": "File size is manageable"}

def main():
    """リファクタリング分析実行"""
    print("🔧 SaijinOS Creative Studio - リファクタリング分析")
    print("=" * 60)
    
    refactoring = SaijinOSRefactoring()
    
    # 現在のファイル分析
    analysis = refactoring.analyze_current_file()
    print("📊 現在のファイル分析:")
    if "error" not in analysis:
        for key, value in analysis.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.1f}")
            else:
                print(f"  {key}: {value}")
    else:
        print(f"  エラー: {analysis['error']}")
    print()
    
    # 優先度評価
    priority = refactoring.get_refactoring_priority()
    print("🎯 リファクタリング優先度:")
    for key, value in priority.items():
        print(f"  {key}: {value}")
    print()
    
    # ディレクトリ構造作成
    if priority["priority"] in ["critical", "high"]:
        print("📁 新しいディレクトリ構造作成:")
        directories = refactoring.create_directory_structure()
        for directory in directories:
            print(f"  ✅ {directory}")
        print()
        
        print("🚀 推奨次ステップ:")
        print("  1. HTMLテンプレートの分離")
        print("  2. CSS/JavaScriptファイルの分離")
        print("  3. APIルートの分離")
        print("  4. コア機能のモジュール化")
        print("  5. 新main.pyの作成")
    
    print("=" * 60)
    print("✅ リファクタリング分析完了")

if __name__ == "__main__":
    main()