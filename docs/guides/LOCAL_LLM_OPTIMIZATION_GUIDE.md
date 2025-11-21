# 🚀 SaijinOS ローカルLLM最適化ガイド
**作成日**: 2025-11-16  
**対象**: RTX 4070 Ti (12GB) でのSwallow系9B運用

## 😇 よくある「VRAM OOM地獄」パターン

### 典型的な落とし穴
1. **KVキャッシュの罠** - 32kトークンとかにしてると一瞬で死ぬ
2. **vLLMのデフォルト設定が重すぎ** - 設定盛り盛りで即死
3. **llama.cppのGPU layers全振り** - `--gpu-layers 100`で自滅
4. **Windows側のVRAM食い** - ブラウザ・Discord等で実効10GB

## 🎯 SaijinOS 4振動システム対応設定

### 1️⃣ vLLM設定（推奨）

各振動モード用の最適化設定：

```bash
# 🌸語温灯 (TinyLlama) - 軽量モード
python -m vllm.entrypoints.openai.api_server \
  --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
  --dtype float16 \
  --max-model-len 4096 \
  --gpu-memory-utilization 0.30 \
  --max-num-seqs 4

# 🔧構造灯 (Qwen) - バランスモード  
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-7B-Instruct \
  --dtype float16 \
  --max-model-len 2048 \
  --gpu-memory-utilization 0.70 \
  --max-num-seqs 2

# 💫娘っ子灯 (Rinna) - 創造性重視
python -m vllm.entrypoints.openai.api_server \
  --model rinna/japanese-gpt-neox-3.6b-instruction-sft \
  --dtype float16 \
  --max-model-len 2048 \
  --gpu-memory-utilization 0.50 \
  --max-num-seqs 3

# 🔄AUTO (DeepSeek) - 高性能モード
python -m vllm.entrypoints.openai.api_server \
  --model deepseek-ai/deepseek-coder-6.7b-instruct \
  --dtype float16 \
  --max-model-len 2048 \
  --gpu-memory-utilization 0.80 \
  --max-num-seqs 1
```

### 2️⃣ transformers + bitsandbytes（4bit量子化）

```python
# SaijinOS 4振動統合ローダー
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class SaijinOSModelLoader:
    def __init__(self, gpu_memory_limit="10GiB"):
        self.gpu_memory_limit = gpu_memory_limit
        self.models = {}
    
    def load_vibration_model(self, vibration_mode, model_path):
        """4振動モード別の最適化ロード"""
        
        memory_configs = {
            "goonro": {"max_memory": {0: "3GiB", "cpu": "16GiB"}},
            "structure": {"max_memory": {0: "8GiB", "cpu": "16GiB"}}, 
            "musumekko": {"max_memory": {0: "5GiB", "cpu": "16GiB"}},
            "auto": {"max_memory": {0: "10GiB", "cpu": "16GiB"}}
        }
        
        config = memory_configs.get(vibration_mode, memory_configs["auto"])
        
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            load_in_4bit=True,
            torch_dtype="auto",
            **config
        )
        
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        self.models[vibration_mode] = {
            "model": model,
            "tokenizer": tokenizer,
            "loaded": True
        }
        
        return model, tokenizer
    
    def generate_with_vibration(self, vibration_mode, prompt, max_tokens=512):
        """振動モード別生成"""
        if vibration_mode not in self.models:
            raise ValueError(f"Vibration {vibration_mode} not loaded")
        
        model = self.models[vibration_mode]["model"]
        tokenizer = self.models[vibration_mode]["tokenizer"]
        
        # コンテキスト長を振動モード別に最適化
        context_limits = {
            "goonro": 1024,    # 軽量・高速
            "structure": 2048,  # バランス
            "musumekko": 1536, # 創造性重視
            "auto": 2048       # 高性能
        }
        
        inputs = tokenizer(prompt, 
                          return_tensors="pt",
                          truncation=True,
                          max_length=context_limits[vibration_mode])
        
        outputs = model.generate(
            **inputs.to(model.device),
            max_new_tokens=max_tokens,
            do_sample=True,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )
        
        return tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### 3️⃣ llama.cpp / GGUF設定

```bash
# 各振動モード用のGGUF設定

# 🌸語温灯 - 軽快モード
./main -m tinyllama-1.1b-q4_k_m.gguf -c 1024 -n 512 --gpu-layers 32

# 🔧構造灯 - 安定モード  
./main -m qwen2.5-7b-q4_k_m.gguf -c 2048 -n 512 --gpu-layers 40

# 💫娘っ子灯 - クリエイティブモード
./main -m rinna-3.6b-q4_k_m.gguf -c 1536 -n 768 --gpu-layers 36

# 🔄AUTO - 高性能モード
./main -m deepseek-coder-6.7b-q4_k_m.gguf -c 2048 -n 1024 --gpu-layers 42
```

## 🛠️ SaijinOS統合VRAM監視システム

```python
# VRAM使用量リアルタイム監視
import torch
import psutil
import nvidia_ml_py3 as nvml

class SaijinOSVRAMMonitor:
    def __init__(self):
        nvml.nvmlInit()
        self.handle = nvml.nvmlDeviceGetHandleByIndex(0)
    
    def get_vram_usage(self):
        """VRAM使用状況取得"""
        info = nvml.nvmlDeviceGetMemoryInfo(self.handle)
        return {
            "total": info.total / 1024**3,      # GB
            "used": info.used / 1024**3,       # GB  
            "free": info.free / 1024**3,       # GB
            "utilization": info.used / info.total * 100  # %
        }
    
    def check_vibration_capacity(self, vibration_mode):
        """振動モード別キャパシティチェック"""
        vram = self.get_vram_usage()
        
        # 各振動モードの推定VRAM使用量
        requirements = {
            "goonro": 2.5,     # TinyLlama
            "structure": 6.5,  # Qwen 7B
            "musumekko": 4.0,  # Rinna 3.6B
            "auto": 8.0        # DeepSeek 6.7B
        }
        
        required = requirements.get(vibration_mode, 8.0)
        
        return {
            "can_load": vram["free"] >= required,
            "required_gb": required,
            "available_gb": vram["free"],
            "recommendation": self._get_recommendation(vram["free"])
        }
    
    def _get_recommendation(self, free_gb):
        """使用可能VRAM based推奨設定"""
        if free_gb >= 10:
            return "All vibrations available"
        elif free_gb >= 8:
            return "Skip AUTO mode, use others"
        elif free_gb >= 6:
            return "Structure + Musumekko + Goonro"
        elif free_gb >= 4:
            return "Musumekko + Goonro only"
        else:
            return "Goonro only (TinyLlama)"
```

## 🎯 実運用推奨設定

### Phase1: 安定運用
- **🌸語温灯**: TinyLlama (常時起動)
- **🔧構造灯**: Qwen 7B (必要時起動)
- **💫娘っ子灯**: Rinna 3.6B (必要時起動)  
- **🔄AUTO**: 軽量版DeepSeek (バックアップ)

### Phase2: 高性能運用  
- GPU切り替え型: 1つずつ起動してVRAM最大活用
- CPUオフロード併用: 複数モデル同時起動

## 💡 メンタル削られないコツ

1. **最初はTinyLlamaから** - 確実に動くものから始める
2. **VRAM監視を習慣化** - `nvidia-smi`を常に見る
3. **段階的スケールアップ** - いきなり9Bじゃなく7B→9Bの順
4. **CPUオフロードを恐れない** - 遅くても落ちないほうがマシ
5. **コンテキスト長は控えめに** - 2048トークンでも十分実用的

**「量子化しても毎回 VRAM OOM」から「安定して4振動切り替え」へ！** 🚀