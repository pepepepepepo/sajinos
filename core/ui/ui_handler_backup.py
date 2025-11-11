"""
SaijinOS UI Handler
HTML ファイル管理とレスポンス生成
"""
import os
from typing import Optional

class UIHandler:
    """UIファイル管理クラス"""
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    def get_ide_content(self) -> str:
        """IDEインターフェースを提供"""
        try:
            html_path = os.path.join(self.base_dir, "saijinos_ide.html")
            with open(html_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError as e:
            return f"<h1>Error: saijinos_ide.html not found</h1><p>Looking for: {html_path}</p><p>Error: {e}</p>"
    
    def get_control_panel_content(self) -> str:
        """コントロールパネルを提供"""
        try:
            current_dir = self.base_dir
            possible_paths = [
                os.path.join(current_dir, "control_panel_v2.html"),
                "F:/sajinos_final/src/static/control_panel_v2.html",
                os.path.join(current_dir, "static", "control_panel_v2.html")
            ]
            
            for html_path in possible_paths:
                if os.path.exists(html_path):
                    with open(html_path, "r", encoding="utf-8") as f:
                        return f.read()
            
            return f"<h1>Error: control_panel_v2.html not found</h1><p>Checked paths: {possible_paths}</p>"
        except Exception as e:
            return f"<h1>Error loading control panel</h1><p>Error: {e}</p>"

# グローバルインスタンス
ui_handler = UIHandler()