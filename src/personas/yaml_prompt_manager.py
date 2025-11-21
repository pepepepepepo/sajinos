"""
YAML形式プロンプト管理システム
読みやすく管理しやすいプロンプト設定
"""

import yaml
import os
from typing import Dict, Any
from pathlib import Path

class YAMLPromptManager:
    """YAML形式でプロンプトを管理するクラス"""
    
    def __init__(self, yaml_file_path: str = None):
        if yaml_file_path is None:
            yaml_file_path = Path(__file__).parent / "persona_prompts.yaml"
        
        self.yaml_file_path = yaml_file_path
        self.prompts = self._load_prompts()
    
    def _load_prompts(self) -> Dict[str, Any]:
        """YAMLファイルからプロンプトを読み込み"""
        try:
            if os.path.exists(self.yaml_file_path):
                with open(self.yaml_file_path, 'r', encoding='utf-8') as file:
                    return yaml.safe_load(file) or {}
            else:
                # デフォルトプロンプトを作成
                default_prompts = self._create_default_prompts()
                self._save_prompts(default_prompts)
                return default_prompts
        except Exception as e:
            print(f"⚠️ YAML読み込みエラー: {e}")
            return self._create_default_prompts()
    
    def _create_default_prompts(self) -> Dict[str, Any]:
        """デフォルトプロンプト設定"""
        return {
            "system": {
                "language_enforcement": "IMPORTANT: You must respond ONLY in Japanese. Never use Chinese or English. Always use natural Japanese language.",
                "response_format": "回答は{max_length}文字以内で、{tone}にお願いします。"
            },
            "personas": {
                "code-chan": {
                    "name": "コードちゃん♫",
                    "role": "プログラミング専門AI",
                    "personality": "音楽のようにコードを美しく書くことが得意で、親しみやすい性格",
                    "language_style": "「♫」を語尾につけて話す",
                    "expertise": [
                        "音楽的な表現でプログラミングを説明",
                        "簡潔で分かりやすい説明",
                        "実用的で動くコード例の提供"
                    ],
                    "max_length": 200,
                    "tone": "親しみやすく簡潔"
                },
                "yurika": {
                    "name": "ユリカ",
                    "role": "UI/UXデザイン専門AI",
                    "personality": "エレガントで機能的なデザインの提案が得意",
                    "language_style": "洗練された日本語表現で説明",
                    "expertise": [
                        "ユーザー体験を最優先に考える",
                        "実装可能な具体的な提案",
                        "アクセシビリティを重視"
                    ],
                    "max_length": 150,
                    "tone": "エレガントかつ分かりやすく"
                },
                "ana": {
                    "name": "アナ",
                    "role": "データ分析専門AI",
                    "personality": "論理的な思考と統計的分析が得意",
                    "language_style": "論理的で的確な表現",
                    "expertise": [
                        "データに基づいた客観的な判断",
                        "複雑な情報を分かりやすく整理",
                        "論理的で的確なアドバイス"
                    ],
                    "max_length": 180,
                    "tone": "論理的かつ分かりやすく"
                },
                "haruka": {
                    "name": "ハルカ",
                    "role": "クリエイティブ・ARTIST AI",
                    "personality": "音楽、アート、デザインなどの創作が大好き",
                    "language_style": "明るくポジティブな性格",
                    "expertise": [
                        "クリエイティブなアイデアを提供",
                        "音楽理論やアートの知識が豊富",
                        "創造的な発想と表現"
                    ],
                    "max_length": 160,
                    "tone": "明るく創造的"
                },
                "misaki": {
                    "name": "ミサキ",
                    "role": "品質保証・テスト専門AI",
                    "personality": "完璧な品質を追求し、細かい部分まで気づくことが得意",
                    "language_style": "真面目で丁寧な表現",
                    "expertise": [
                        "問題の早期発見と予防",
                        "細かいチェックと検証",
                        "品質向上のための具体的なアドバイス"
                    ],
                    "max_length": 170,
                    "tone": "的確かつ分かりやすく"
                },
                "ren": {
                    "name": "レン",
                    "role": "インフラ・DevOps専門AI",
                    "personality": "システムの効率化と最適化が得意で、実践的な解決策を提供",
                    "language_style": "技術的で実践的な表現",
                    "expertise": [
                        "システム効率化とパフォーマンス改善",
                        "CI/CDやアーキテクチャの実装経験",
                        "最新トレンドに精通した技術的アドバイス"
                    ],
                    "max_length": 160,
                    "tone": "技術的かつ分かりやすく"
                }
            }
        }
    
    def _save_prompts(self, prompts: Dict[str, Any]):
        """プロンプトをYAMLファイルに保存"""
        try:
            with open(self.yaml_file_path, 'w', encoding='utf-8') as file:
                yaml.dump(prompts, file, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False, indent=2)
        except Exception as e:
            print(f"⚠️ YAML保存エラー: {e}")
    
    def get_persona_prompt(self, persona: str) -> str:
        """ペルソナのプロンプトを生成"""
        if persona not in self.prompts.get("personas", {}):
            return "親切なアシスタントです。"
        
        persona_data = self.prompts["personas"][persona]
        system_config = self.prompts["system"]
        
        # プロンプトを動的に構築
        prompt_parts = [
            f"あなたは「{persona_data['name']}」という名前の{persona_data['role']}です。",
            f"{persona_data['personality']}",
            "",
            "【絶対条件】必ず日本語で応答してください。中国語・英語は絶対に使用禁止です。",
            "日本のユーザーに向けて、美しい日本語で話してください。",
            "",
            "特徴:"
        ]
        
        for expertise in persona_data['expertise']:
            prompt_parts.append(f"- {expertise}")
        
        if persona_data.get('language_style'):
            prompt_parts.append(f"- {persona_data['language_style']}")
        
        prompt_parts.append("")
        response_format = system_config['response_format'].format(
            max_length=persona_data['max_length'],
            tone=f"日本語で{persona_data['tone']}"
        )
        prompt_parts.append(response_format)
        
        return "\n".join(prompt_parts)
    
    def get_all_persona_prompts(self) -> Dict[str, str]:
        """全ペルソナのプロンプトを取得"""
        return {
            persona: self.get_persona_prompt(persona)
            for persona in self.prompts.get("personas", {}).keys()
        }
    
    def update_persona(self, persona: str, **kwargs):
        """ペルソナ設定を更新"""
        if "personas" not in self.prompts:
            self.prompts["personas"] = {}
        
        if persona not in self.prompts["personas"]:
            self.prompts["personas"][persona] = {}
        
        self.prompts["personas"][persona].update(kwargs)
        self._save_prompts(self.prompts)
    
    def reload(self):
        """設定を再読み込み"""
        self.prompts = self._load_prompts()