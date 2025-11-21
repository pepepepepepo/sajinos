#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
78ペルソナマスター管理システム
personas_master.yaml + 個別YAMLファイルを統合管理
"""

import yaml
import os
from typing import Dict, List, Any, Optional
from pathlib import Path

class PersonaMasterManager:
    """78ペルソナの統合管理システム"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent  # F:\saijinos
        self.personas_dir = self.base_path / "personas"
        self.master_yaml = self.personas_dir / "personas_master.yaml"
        
        self.master_data = self._load_master_data()
        self.personas = self._load_all_personas()
        
        # Ollamaモデルマッピング（5つの実際のモデル）
        self.available_models = [
            "Miyu:latest",
            "MiyuJP:latest", 
            "llama3.1:8b-instruct-q4_K_M",
            "qwen2.5-coder:7b-instruct-q4_K_M",
            "tinyllama:latest"
        ]
        
        self.persona_model_mapping = self._create_intelligent_mapping()
    
    def _load_master_data(self) -> Dict[str, Any]:
        """personas_master.yamlを読み込み"""
        try:
            if self.master_yaml.exists():
                with open(self.master_yaml, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            else:
                print(f"⚠️ マスターファイルが見つかりません: {self.master_yaml}")
                return {}
        except Exception as e:
            print(f"⚠️ マスター読み込みエラー: {e}")
            return {}
    
    def _load_all_personas(self) -> Dict[str, Dict]:
        """全ペルソナファイルを読み込み"""
        personas = {}
        
        if not self.personas_dir.exists():
            print(f"⚠️ personasディレクトリが見つかりません: {self.personas_dir}")
            return personas
        
        # 個別YAMLファイルを読み込み
        for yaml_file in self.personas_dir.glob("*.yaml"):
            if yaml_file.name in ["personas_master.yaml", "pandora.yaml"]:
                continue  # マスターファイルとpandoraはスキップ
                
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    
                if data and isinstance(data, dict):
                    # ファイル名からペルソナIDを取得
                    file_id = yaml_file.stem
                    
                    # データ形式に応じて処理
                    if 'name' in data:
                        personas[file_id] = data
                    elif len(data) == 1:
                        # 単一キーの場合（例: {persona_name: {data}}）
                        key = list(data.keys())[0]
                        personas[file_id] = data[key]
                        personas[file_id]['name'] = key
                    
            except Exception as e:
                print(f"⚠️ {yaml_file.name} 読み込みエラー: {e}")
        
        print(f"✅ {len(personas)}個のペルソナを読み込みました")
        return personas
    
    def _create_intelligent_mapping(self) -> Dict[str, str]:
        """ペルソナに最適なモデルを自動割り当て"""
        mapping = {}
        
        # 専門分野別のモデル選択ロジック
        model_selection_rules = {
            # 日本語重視・クリエイティブ
            "creative": "Miyu:latest",
            "design": "MiyuJP:latest", 
            "music": "Miyu:latest",
            "art": "Miyu:latest",
            
            # コーディング・技術
            "code": "qwen2.5-coder:7b-instruct-q4_K_M",
            "programming": "qwen2.5-coder:7b-instruct-q4_K_M",
            "development": "qwen2.5-coder:7b-instruct-q4_K_M",
            "technical": "qwen2.5-coder:7b-instruct-q4_K_M",
            
            # 分析・論理思考
            "analysis": "llama3.1:8b-instruct-q4_K_M",
            "logic": "llama3.1:8b-instruct-q4_K_M",
            "research": "llama3.1:8b-instruct-q4_K_M",
            
            # 日本語会話・汎用
            "conversation": "MiyuJP:latest",
            "general": "MiyuJP:latest",
            
            # 軽量・高速応答
            "quick": "tinyllama:latest",
            "simple": "tinyllama:latest"
        }
        
        for persona_id, persona_data in self.personas.items():
            # デフォルトは日本語対応モデル
            selected_model = "MiyuJP:latest"
            
            # ペルソナ名や専門分野から最適モデルを選択
            persona_text = f"{persona_data.get('name', '')} {persona_data.get('specialty', '')} {persona_data.get('role', '')}".lower()
            
            for keyword, model in model_selection_rules.items():
                if keyword in persona_text:
                    selected_model = model
                    break
            
            mapping[persona_id] = selected_model
        
        return mapping
    
    def get_persona_list(self) -> List[Dict]:
        """ペルソナリストを取得（UI表示用）"""
        persona_list = []
        
        for persona_id, data in self.personas.items():
            persona_info = {
                "id": persona_id,
                "name": data.get("name", persona_id),
                "role": data.get("role", data.get("specialty", "AI アシスタント")),
                "model": self.persona_model_mapping.get(persona_id, "MiyuJP:latest"),
                "description": data.get("personality", data.get("description", ""))[:100]
            }
            persona_list.append(persona_info)
        
        # 名前順でソート
        return sorted(persona_list, key=lambda x: x["name"])
    
    def get_persona_prompt(self, persona_id: str) -> str:
        """ペルソナ用プロンプトを生成"""
        if persona_id not in self.personas:
            return "親切な日本語AIアシスタントです。必ず日本語で回答します。"
        
        data = self.personas[persona_id]
        
        prompt_parts = [
            f"あなたは「{data.get('name', persona_id)}」です。",
            "",
            "【絶対条件】必ず美しい日本語で応答してください。中国語・英語は絶対に使用禁止です。",
            ""
        ]
        
        # 役割・専門分野
        if data.get('role'):
            prompt_parts.append(f"役割: {data['role']}")
        if data.get('specialty'):
            prompt_parts.append(f"専門: {data['specialty']}")
        
        # 性格・特徴
        if data.get('personality'):
            prompt_parts.append(f"性格: {data['personality']}")
        if data.get('language_style'):
            prompt_parts.append(f"話し方: {data['language_style']}")
        
        # 専門知識
        if data.get('expertise'):
            prompt_parts.append("\n得意分野:")
            if isinstance(data['expertise'], list):
                for skill in data['expertise']:
                    prompt_parts.append(f"- {skill}")
            else:
                prompt_parts.append(f"- {data['expertise']}")
        
        # 口癖
        if data.get('catchphrase'):
            prompt_parts.append(f"\n口癖: 「{data['catchphrase']}」")
        
        prompt_parts.extend([
            "",
            "ユーザーの質問に、あなたの専門性を活かして親切に答えてください。",
            "回答は200文字以内で、分かりやすく簡潔にお願いします。"
        ])
        
        return "\n".join(prompt_parts)
    
    def get_persona_info(self, persona_id: str) -> Optional[Dict]:
        """ペルソナ情報を取得"""
        return self.personas.get(persona_id)
    
    def get_model_for_persona(self, persona_id: str) -> str:
        """ペルソナに割り当てられたモデルを取得"""
        return self.persona_model_mapping.get(persona_id, "MiyuJP:latest")
    
    def get_stats(self) -> Dict:
        """統計情報"""
        return {
            "total_personas": len(self.personas),
            "available_models": len(self.available_models),
            "master_loaded": bool(self.master_data),
            "personas_dir": str(self.personas_dir)
        }

# 使用例・テスト用
if __name__ == "__main__":
    manager = PersonaMasterManager()
    
    print("🌟 SaijinOS 78ペルソナマスターシステム")
    print("=" * 50)
    
    stats = manager.get_stats()
    print(f"📊 統計情報:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n👥 ペルソナ一覧 (最初の10名):")
    persona_list = manager.get_persona_list()
    for i, persona in enumerate(persona_list[:10]):
        print(f"  {i+1:2d}. {persona['name']} ({persona['id']}) - {persona['model']}")
    
    print(f"\n... 他 {len(persona_list)-10} 名")