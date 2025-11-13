"""
AI Model Manager for SaijinOS
TinyLlama統合とAIチャット機能を提供
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import logging
from typing import Optional, Dict, Any

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIModelManager:
    """AI モデル管理クラス"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self.model_path = "E:/AI_Models/saijin-swallow/models/tinyllama/models--TinyLlama--TinyLlama-1.1B-Chat-v1.0/snapshots/fe8a4ea1ffedaf415f4da2f062534de366a451e6"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.is_loaded = False
        
    async def load_model(self) -> Dict[str, Any]:
        """TinyLlamaモデルを読み込む"""
        try:
            logger.info(f"Loading TinyLlama model from: {self.model_path}")
            
            # トークナイザーを読み込み
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            
            # モデルを読み込み
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None,
                trust_remote_code=True
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
                
            self.is_loaded = True
            
            logger.info(f"✅ TinyLlama loaded successfully on {self.device}")
            return {
                "status": "success",
                "message": f"TinyLlama loaded on {self.device}",
                "model_name": self.model_name,
                "device": self.device
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to load TinyLlama: {str(e)}")
            return {
                "status": "error", 
                "message": f"Model loading failed: {str(e)}"
            }
    
    async def generate_response(self, prompt: str, max_length: int = 512) -> Dict[str, Any]:
        """テキスト生成（チャット応答）"""
        if not self.is_loaded:
            return {
                "status": "error",
                "message": "Model not loaded. Please load model first."
            }
            
        try:
            # チャット用のプロンプトフォーマット
            chat_prompt = f"<|system|>\nYou are a helpful AI assistant in SaijinOS Creative Studio.\n<|user|>\n{prompt}\n<|assistant|>\n"
            
            # トークン化
            inputs = self.tokenizer.encode(chat_prompt, return_tensors="pt").to(self.device)
            
            # 生成
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    attention_mask=torch.ones_like(inputs)
                )
            
            # デコード
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # アシスタント部分のみを抽出
            if "<|assistant|>" in response:
                response = response.split("<|assistant|>")[-1].strip()
            
            return {
                "status": "success",
                "response": response,
                "model": self.model_name
            }
            
        except Exception as e:
            logger.error(f"❌ Generation failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Generation failed: {str(e)}"
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        """モデル情報を取得"""
        return {
            "model_name": self.model_name,
            "model_path": self.model_path,
            "device": self.device,
            "is_loaded": self.is_loaded,
            "cuda_available": torch.cuda.is_available()
        }

# グローバルインスタンス
ai_model_manager = AIModelManager()