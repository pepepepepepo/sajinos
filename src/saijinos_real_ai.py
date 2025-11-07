#!/usr/bin/env python3
"""
SaijinOS Real Local AI Integration System
10-model coordination with actual Swallow-9B model
Real model integration with fallback to mock processing
"""

import os
import yaml
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class RealLocalAICoordinator:
    """Real AI model coordination system with Swallow-9B integration"""
    
    def __init__(self, config_path: str = "f:/saijinos/config/multi_ai_config.yaml"):
        self.config = self.load_config(config_path)
        self.active_models = {}
        self.model_stats = {}
        self.conversation_history = []
        
        # Initialize available models
        self.initialize_real_models()
        
    def load_config(self, config_path: str) -> dict:
        """Load AI model configuration"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"⚠️ Config loading error: {e}")
            return self.get_default_config()
    
    def get_default_config(self) -> dict:
        """Fallback configuration"""
        return {
            "models": {
                "swallow_9b": {
                    "model_path": "E:/AI_Models/saijin-swallow/swallow_models/swallow/",
                    "status": "AVAILABLE",
                    "backend": "vLLM"
                }
            }
        }
    
    def initialize_real_models(self):
        """Initialize available real AI models"""
        print("🤖 SaijinOS Real AI Coordinator - Initializing...")
        
        available_models = []
        
        # Check Swallow-9B availability
        swallow_path = self.config["models"]["swallow_9b"]["model_path"]
        if self.check_model_exists(swallow_path):
            try:
                self.load_swallow_model(swallow_path)
                available_models.append("swallow_9b")
                print("✅ Swallow-9B model loaded successfully")
            except Exception as e:
                print(f"❌ Swallow-9B loading failed: {e}")
                print("🔄 Falling back to mock processing")
        else:
            print("⚠️ Swallow-9B model files not found, using mock mode")
        
        print(f"📊 Available models: {len(available_models)}")
        return available_models
    
    def check_model_exists(self, model_path: str) -> bool:
        """Check if model files exist"""
        path = Path(model_path)
        if not path.exists():
            return False
        
        # Check for essential model files
        required_files = ["config.json", "tokenizer_config.json"]
        safetensor_files = list(path.glob("*.safetensors"))
        
        has_required = all((path / file).exists() for file in required_files)
        has_model_weights = len(safetensor_files) > 0
        
        return has_required and has_model_weights
    
    def load_swallow_model(self, model_path: str):
        """Load Swallow-9B model with vLLM backend"""
        try:
            # Try to import and initialize vLLM
            try:
                from vllm import LLM, SamplingParams
                
                # Initialize Swallow model with 4-bit quantization
                self.swallow_model = LLM(
                    model=model_path,
                    quantization="awq",  # 4-bit quantization
                    gpu_memory_utilization=0.8,
                    max_model_len=2048
                )
                
                self.swallow_sampling = SamplingParams(
                    temperature=0.7,
                    top_p=0.9,
                    max_tokens=512
                )
                
                self.active_models["swallow_9b"] = {
                    "model": self.swallow_model,
                    "sampling": self.swallow_sampling,
                    "backend": "vLLM",
                    "status": "loaded"
                }
                
                return True
                
            except ImportError:
                print("📦 vLLM not available, trying Transformers backend...")
                return self.load_swallow_transformers(model_path)
                
        except Exception as e:
            print(f"⚠️ Model loading error: {e}")
            return False
    
    def load_swallow_transformers(self, model_path: str):
        """Fallback: Load with Transformers library"""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
            
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16,
                device_map="auto",
                load_in_4bit=True  # 4-bit quantization
            )
            
            self.active_models["swallow_9b"] = {
                "model": model,
                "tokenizer": tokenizer,
                "backend": "Transformers", 
                "status": "loaded"
            }
            
            print("✅ Swallow-9B loaded with Transformers backend")
            return True
            
        except ImportError as e:
            print(f"📦 Transformers not available: {e}")
            return False
        except Exception as e:
            print(f"⚠️ Transformers loading failed: {e}")
            return False
    
    def process_with_real_model(self, prompt: str, model_name: str = "swallow_9b") -> str:
        """Process prompt with real AI model"""
        if model_name not in self.active_models:
            return self.mock_process(prompt, model_name)
        
        model_info = self.active_models[model_name]
        
        try:
            if model_info["backend"] == "vLLM":
                return self.process_vllm(prompt, model_info)
            elif model_info["backend"] == "Transformers":
                return self.process_transformers(prompt, model_info)
            else:
                return self.mock_process(prompt, model_name)
                
        except Exception as e:
            print(f"⚠️ Real model processing error: {e}")
            return self.mock_process(prompt, model_name)
    
    def process_vllm(self, prompt: str, model_info: dict) -> str:
        """Process with vLLM backend"""
        model = model_info["model"]
        sampling = model_info["sampling"]
        
        # Generate response
        outputs = model.generate([prompt], sampling)
        response = outputs[0].outputs[0].text
        
        return response.strip()
    
    def process_transformers(self, prompt: str, model_info: dict) -> str:
        """Process with Transformers backend"""
        model = model_info["model"]
        tokenizer = model_info["tokenizer"]
        
        # Tokenize and generate
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                max_length=inputs.shape[1] + 512,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        # Decode response
        response = tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
        return response.strip()
    
    def mock_process(self, prompt: str, model_name: str) -> str:
        """Mock processing for unavailable models"""
        responses = {
            "swallow_9b": f"🤖 [Swallow-9B Mock] {prompt}への応答：実際のモデルが利用可能になったらより詳細な回答を提供します。",
            "tinyllama": f"💬 [TinyLlama Mock] Quick response to: {prompt[:50]}...",
            "codegen_model": f"💻 [CodeGen Mock] # Code for: {prompt}\n# Real implementation pending",
            "default": f"🔄 [AI Mock] Processing: {prompt[:30]}..."
        }
        
        return responses.get(model_name, responses["default"])
    
    def analyze_task_type(self, content: str) -> str:
        """Analyze content to determine appropriate AI model"""
        content_lower = content.lower()
        
        # Task analysis with routing rules
        if any(keyword in content_lower for keyword in self.config.get("routing", {}).get("code_keywords", [])):
            return "codegen_model"
        elif any(keyword in content_lower for keyword in self.config.get("routing", {}).get("music_keywords", [])):
            return "music_ai"
        elif any(keyword in content_lower for keyword in self.config.get("routing", {}).get("math_keywords", [])):
            return "math_ai"
        elif len(content) < 50:
            return "tinyllama"  # Short queries
        else:
            return "swallow_9b"  # Main dialogue
    
    def coordinate_response(self, user_input: str, persona: str = "主AI") -> Dict[str, Any]:
        """Coordinate AI response with real model integration"""
        start_time = time.time()
        
        # Determine model from persona
        model_name = self.config.get("personas", {}).get(persona, "swallow_9b")
        
        # Task analysis
        analyzed_task = self.analyze_task_type(user_input)
        
        # Use task-specific model if more appropriate
        if analyzed_task != model_name and analyzed_task in self.config["models"]:
            model_name = analyzed_task
        
        # Process with real or mock model
        response = self.process_with_real_model(user_input, model_name)
        
        # Response metadata
        processing_time = time.time() - start_time
        
        result = {
            "response": response,
            "model_used": model_name,
            "persona": persona,
            "task_type": analyzed_task,
            "processing_time": f"{processing_time:.2f}s",
            "timestamp": datetime.now().isoformat(),
            "backend": self.active_models.get(model_name, {}).get("backend", "Mock"),
            "real_model": model_name in self.active_models
        }
        
        # Update conversation history
        self.conversation_history.append({
            "input": user_input,
            "output": result,
            "timestamp": result["timestamp"]
        })
        
        return result
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        total_models = len(self.config["models"])
        active_models = len(self.active_models) 
        
        return {
            "total_configured_models": total_models,
            "active_real_models": active_models,
            "mock_models": total_models - active_models,
            "available_personas": len(self.config.get("personas", {})),
            "conversation_turns": len(self.conversation_history),
            "active_model_list": list(self.active_models.keys()),
            "system_ready": active_models > 0
        }
    
    def interactive_test(self):
        """Interactive testing interface"""
        print("🌟 SaijinOS Real AI Coordinator - Interactive Test")
        print("=" * 60)
        
        # Show status
        status = self.get_system_status()
        print(f"📊 System Status:")
        print(f"   Real Models: {status['active_real_models']}/{status['total_configured_models']}")
        print(f"   Available Personas: {status['available_personas']}")
        print(f"   System Ready: {'✅' if status['system_ready'] else '❌'}")
        print()
        
        while True:
            try:
                user_input = input("💬 You: ").strip()
                
                if not user_input:
                    continue
                    
                if user_input.lower() in ['exit', 'quit', '終了']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'status':
                    print(json.dumps(self.get_system_status(), indent=2, ensure_ascii=False))
                    continue
                
                # Process with AI coordinator
                result = self.coordinate_response(user_input)
                
                print(f"\n🤖 {result['persona']}: {result['response']}")
                print(f"📱 Model: {result['model_used']} ({result['backend']}) | Time: {result['processing_time']}")
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function"""
    # Initialize real AI coordinator
    coordinator = RealLocalAICoordinator()
    
    # Run interactive test
    coordinator.interactive_test()

if __name__ == "__main__":
    main()