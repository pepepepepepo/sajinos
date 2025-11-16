# -*- coding: utf-8 -*-
"""
ワークスペース管理システム
5つの統合ワークスペースを管理
"""

from typing import Dict, List, Any

class WorkspaceManager:
    """ワークスペース管理システム"""
    
    def __init__(self):
        self.workspaces = {
            "chat": {
                "name": "💬 チャット",
                "description": "基本的な会話・相談用インターフェース",
                "features": ["自然対話", "相談応答", "質問回答", "創作支援"],
                "tools": ["チャット履歴", "ペルソナ切替", "感情分析", "話題提案"],
                "template": "chat.html"
            },
            "development": {
                "name": "🖥️ 開発",
                "description": "統合開発環境（IDE）・プログラミング支援",
                "features": ["コードエディタ", "デバッグ支援", "技術解説", "実行環境"],
                "tools": ["Monaco Editor", "ファイル管理", "ターミナル", "Git統合"],
                "template": "development.html"
            },
            "design": {
                "name": "🎨 デザイン",
                "description": "UIデザイン・グラフィック制作・プロトタイピング",
                "features": ["デザイン制作", "プロトタイピング", "カラーパレット", "UI/UX分析"],
                "tools": ["デザインツール", "カラーピッカー", "フォント管理", "レイアウトグリッド"],
                "template": "design.html"
            },
            "analysis": {
                "name": "📊 分析",
                "description": "データ分析・統計・レポート生成",
                "features": ["データ解析", "統計分析", "レポート生成", "トレンド分析"],
                "tools": ["チャート作成", "データ可視化", "統計計算", "レポート出力"],
                "template": "analysis.html"
            },
            "music": {
                "name": "🎵 音楽",
                "description": "音楽制作・作曲・音声合成",
                "features": ["音楽制作", "作曲支援", "音声合成", "楽曲分析"],
                "tools": ["シーケンサー", "音声合成", "エフェクト", "BPM制御"],
                "template": "music.html"
            }
        }
    
    def get_available_workspaces(self) -> List[str]:
        """利用可能なワークスペース一覧"""
        return list(self.workspaces.keys())
    
    def is_valid_workspace(self, workspace_name: str) -> bool:
        """ワークスペース名の妥当性確認"""
        return workspace_name in self.workspaces
    
    def get_workspace_config(self, workspace_name: str) -> Dict[str, Any]:
        """ワークスペース設定取得"""
        return self.workspaces.get(workspace_name, {})
    
    def get_workspace_tools(self, workspace_name: str) -> List[str]:
        """ワークスペース専用ツール取得"""
        workspace = self.workspaces.get(workspace_name, {})
        return workspace.get("tools", [])
    
    def get_workspace_features(self, workspace_name: str) -> List[str]:
        """ワークスペース機能一覧"""
        workspace = self.workspaces.get(workspace_name, {})
        return workspace.get("features", [])