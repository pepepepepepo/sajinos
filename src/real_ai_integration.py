#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SaijinOS Real AI Integration
実際のローカルAI統合システム - 既存モデル活用版

🎯 インストール済みモデル活用:
- Miyu (カスタム日本語モデル)
- MiyuJP (日本語特化版)  
- Llama3.1 8B (高性能汎用)
- Qwen2.5 7B (コーディング特化)
- TinyLlama (軽量高速)
"""

import requests
import json
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from yaml_prompt_manager import YAMLPromptManager
from persona_master_manager import PersonaMasterManager

class RealAIIntegration:
    """実際のローカルAI統合システム - 78ペルソナ対応"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.prompt_manager = YAMLPromptManager()
        self.persona_master = PersonaMasterManager()
        
        # 78ペルソナの自動マッピング使用
        self.persona_model_mapping = self.persona_master.persona_model_mapping
        
        # フォールバック用の基本ペルソナ（後方互換性）
        basic_personas = {
            "code-chan": "qwen2.5-coder:7b-instruct-q4_K_M",
            "yurika": "MiyuJP:latest",
            "ana": "llama3.1:8b-instruct-q4_K_M", 
            "haruka": "Miyu:latest",
            "misaki": "MiyuJP:latest",
            "ren": "llama3.1:8b-instruct-q4_K_M",
            "serena": "MiyuJP:latest",
            "organ": "llama3.1:8b-instruct-q4_K_M",
            "ignis": "qwen2.5-coder:7b-instruct-q4_K_M"
        }
        
        # 基本ペルソナを統合
        self.persona_model_mapping.update(basic_personas)
        
        print(f"🌟 {len(self.persona_model_mapping)}ペルソナを読み込みました")

    
    async def test_connection(self) -> bool:
        """Ollama接続テスト"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_available_personas(self) -> List[Dict]:
        """利用可能なペルソナリストを取得"""
        return self.persona_master.get_persona_list()
    
    def get_persona_prompt(self, persona: str) -> str:
        """ペルソナプロンプトを取得（78ペルソナ + 基本ペルソナ対応）"""
        # まず78ペルソナから探す
        if persona in self.persona_master.personas:
            return self.persona_master.get_persona_prompt(persona)
        
        # 基本ペルソナから探す
        if persona in self.prompt_manager.prompts.get("personas", {}):
            return self.prompt_manager.get_persona_prompt(persona)
        
        # デフォルトプロンプト
        return "親切な日本語AIアシスタントです。必ず日本語で回答します。"
    
    async def chat_with_persona(self, persona: str, message: str) -> Dict:
        """ペルソナとの実際のAIチャット"""
        model = self.persona_model_mapping.get(persona, "MiyuJP:latest")
        system_prompt = self.get_persona_prompt(persona)
        
        try:
            # 日本語強制のための追加システムメッセージ
            japanese_enforcement = "IMPORTANT: You must respond ONLY in Japanese. Never use Chinese or English. Always use natural Japanese language."
            
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": f"{japanese_enforcement}\n\n{system_prompt}"},
                    {"role": "user", "content": f"日本語で回答してください: {message}"}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 1024
                }
            }
            
            print(f"🤖 {persona} ({model}) にリクエスト送信中...")
            
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                content = data["message"]["content"].strip()
                # 応答の長さを制限して読みやすくする
                if len(content) > 500:
                    content = content[:500] + "..."
                
                return {
                    "status": "success",
                    "persona": persona,
                    "model": model,
                    "response": content,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "persona": persona,
                    "error": f"HTTP {response.status_code}",
                    "message": "API call failed"
                }
                
        except requests.exceptions.Timeout:
            return {
                "status": "timeout",
                "persona": persona,
                "message": "リクエストがタイムアウトしました"
            }
        except Exception as e:
            return {
                "status": "error", 
                "persona": persona,
                "message": str(e)
            }
    
    async def multi_persona_chat(self, personas: List[str], message: str) -> List[Dict]:
        """複数ペルソナとの同時チャット"""
        tasks = []
        for persona in personas:
            task = self.chat_with_persona(persona, message)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 例外をエラー辞書に変換
        formatted_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                formatted_results.append({
                    "status": "exception",
                    "persona": personas[i],
                    "message": str(result)
                })
            else:
                formatted_results.append(result)
        
        return formatted_results
    
    def get_model_info(self) -> Dict:
        """モデル情報取得"""
        return {
            "persona_mapping": self.persona_model_mapping,
            "available_personas": list(self.persona_prompts.keys()),
            "total_models": len(set(self.persona_model_mapping.values()))
        }

# グローバルインスタンス
real_ai = RealAIIntegration()

# テスト実行
async def test_real_ai():
    print("🌸 SaijinOS Real AI Integration Test")
    print("=" * 50)
    
    # 接続テスト
    connected = await real_ai.test_connection()
    print(f"Ollama Connection: {'✅ OK' if connected else '❌ Failed'}")
    
    if not connected:
        print("Ollamaサーバーが起動していません")
        return
    
    # モデル情報表示
    info = real_ai.get_model_info()
    print(f"\n📊 統合済みペルソナ: {len(info['available_personas'])}人")
    print(f"使用モデル: {info['total_models']}種類")
    
    # 単一ペルソナテスト
    print(f"\n🎵 コードちゃん♫とテストチャット...")
    result = await real_ai.chat_with_persona("code-chan", "こんにちは！PythonでHello Worldを書いて")
    
    if result["status"] == "success":
        print(f"✅ 成功!")
        print(f"Response: {result['response'][:100]}...")
    else:
        print(f"❌ エラー: {result.get('message', 'Unknown error')}")

if __name__ == "__main__":
    asyncio.run(test_real_ai())