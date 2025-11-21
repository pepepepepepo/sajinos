#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌸✨ SaijinOS AI Creative Studio v3.0 ✨🌸
新世代チャットAI風インターフェース + 15種AIモデル統合
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
import json
import random
import psutil
import yaml
import os
from datetime import datetime

app = FastAPI(title="SaijinOS AI Creative Studio v3.0")

# ファビコンエラー対応
@app.get("/favicon.ico")
async def favicon():
    return {"message": "🌸✨ SaijinOS favicon ✨🌸"}

# Ollama AIモデル設定
OLLAMA_MODELS = {
    # オリジナルモデル（5種類）
    "Miyu:latest": {"type": "conversational", "size": "4.7GB", "speciality": "general_chat"},
    "MiyuJP:latest": {"type": "conversational", "size": "4.7GB", "speciality": "japanese_chat"},
    "llama3.1:8b-instruct-q4_K_M": {"type": "instruct", "size": "4.9GB", "speciality": "instruction_following"},
    "qwen2.5:7b-instruct": {"type": "instruct", "size": "4.7GB", "speciality": "multilingual"},
    "tinyllama:latest": {"type": "lightweight", "size": "637MB", "speciality": "quick_response"},
    
    # 軽量特化モデル（5種類）
    "phi3:mini": {"type": "lightweight", "size": "2.2GB", "speciality": "reasoning"},
    "gemma2:2b": {"type": "lightweight", "size": "1.6GB", "speciality": "efficiency"},
    "codellama:7b": {"type": "code", "size": "3.8GB", "speciality": "programming"},
    "mistral:7b": {"type": "instruct", "size": "4.4GB", "speciality": "analysis"},
    "llama3.2:1b": {"type": "ultra_light", "size": "1.3GB", "speciality": "fast_inference"},
    
    # 専門特化モデル（5種類）
    "deepseek-coder:6.7b": {"type": "code", "size": "3.8GB", "speciality": "code_generation"},
    "starcoder2:7b": {"type": "code", "size": "4.0GB", "speciality": "code_analysis"},
    "llava:7b": {"type": "multimodal", "size": "4.7GB", "speciality": "vision_language"},
    "nous-hermes2:10.7b": {"type": "reasoning", "size": "6.1GB", "speciality": "complex_reasoning"},
    "qwen2.5:1.5b": {"type": "lightweight", "size": "986MB", "speciality": "multilingual_light"}
}

# ペルソナ別推奨モデルマッピング
PERSONA_MODEL_MAPPING = {
    "美遊": "Miyu:latest",
    "Haruka": "mistral:7b",
    "Ana": "nous-hermes2:10.7b",
    "Code-chan": "deepseek-coder:6.7b", 
    "Ren": "starcoder2:7b",
    "Yuuri": "MiyuJP:latest",
    "Pandora": "llama3.1:8b-instruct-q4_K_M",
    "Regina": "qwen2.5:7b-instruct"
}

# モード設定
STUDIO_MODES = {
    "chat": {
        "name": "💬 チャットモード",
        "description": "生成AI風の自然な対話",
        "icon": "💬",
        "features": ["自然対話", "リアルタイム応答", "コンテキスト維持"]
    },
    "creative": {
        "name": "🎨 クリエイティブモード", 
        "description": "創作・デザイン支援",
        "icon": "🎨",
        "features": ["創作支援", "アイデア生成", "デザイン相談"]
    },
    "code": {
        "name": "💻 コーディングモード",
        "description": "プログラミング支援",
        "icon": "💻", 
        "features": ["コード生成", "デバッグ支援", "技術相談"]
    },
    "analysis": {
        "name": "📊 分析モード",
        "description": "データ分析・調査",
        "icon": "📊",
        "features": ["データ分析", "情報整理", "レポート作成"]
    }
}

@app.get("/", response_class=HTMLResponse)
async def get_studio():
    # システム情報
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_info = psutil.virtual_memory()
    except:
        cpu_percent = 25.0
        memory_info = type('obj', (object,), {'percent': 60.0})()
    
    # データをJavaScript用に準備
    models_json = json.dumps(OLLAMA_MODELS, ensure_ascii=False)
    personas_json = json.dumps(PERSONA_MODEL_MAPPING, ensure_ascii=False)
    modes_json = json.dumps(STUDIO_MODES, ensure_ascii=False)
    
    html_content = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌸✨ SaijinOS AI Creative Studio v3.0 ✨🌸</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: 'Segoe UI', 'Hiragino Sans', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            overflow: hidden;
            color: #333;
        }}

        /* ヘッダー */
        .header {{
            background: rgba(30, 30, 30, 0.95);
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            backdrop-filter: blur(10px);
        }}

        .header h1 {{
            font-size: 1.5em;
            background: linear-gradient(45deg, #ff9ff3, #feca57);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .mode-selector {{
            display: flex;
            gap: 10px;
        }}

        .mode-btn {{
            padding: 8px 15px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9em;
        }}

        .mode-btn:hover {{
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }}

        .mode-btn.active {{
            background: linear-gradient(45deg, #ff9ff3, #feca57);
            color: #333;
            font-weight: bold;
        }}

        /* メインコンテナ */
        .main-container {{
            display: flex;
            height: calc(100vh - 80px);
            gap: 15px;
            padding: 15px;
        }}

        /* 左サイドバー */
        .sidebar {{
            width: 300px;
            background: rgba(30, 30, 30, 0.95);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(10px);
            overflow-y: auto;
        }}

        .sidebar h3 {{
            color: #ff9ff3;
            margin-bottom: 15px;
            font-size: 1.1em;
            border-bottom: 1px solid rgba(255, 159, 243, 0.3);
            padding-bottom: 8px;
        }}

        /* ペルソナカード */
        .persona-card {{
            background: rgba(60, 60, 60, 0.8);
            border-radius: 10px;
            padding: 12px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}

        .persona-card:hover {{
            background: rgba(80, 80, 80, 0.9);
            transform: translateX(5px);
        }}

        .persona-card.active {{
            border-color: #ff9ff3;
            background: linear-gradient(135deg, rgba(255, 159, 243, 0.2), rgba(254, 202, 87, 0.2));
        }}

        .persona-name {{
            color: white;
            font-weight: bold;
            margin-bottom: 4px;
        }}

        .persona-model {{
            color: #aaa;
            font-size: 0.8em;
        }}

        /* AIモデル情報 */
        .model-info {{
            background: rgba(87, 254, 202, 0.1);
            border-radius: 8px;
            padding: 12px;
            margin-top: 20px;
        }}

        .current-model {{
            color: #57feca;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .model-details {{
            color: #aaa;
            font-size: 0.8em;
        }}

        /* チャットエリア */
        .chat-container {{
            flex: 1;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            backdrop-filter: blur(10px);
        }}

        .chat-header {{
            background: rgba(30, 30, 30, 0.9);
            color: white;
            padding: 15px 20px;
            border-radius: 12px 12px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .chat-title {{
            font-weight: bold;
            font-size: 1.1em;
        }}

        .chat-status {{
            color: #57feca;
            font-size: 0.9em;
        }}

        .chat-messages {{
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }}

        .message {{
            max-width: 80%;
            padding: 12px 16px;
            border-radius: 18px;
            line-height: 1.4;
        }}

        .message.user {{
            align-self: flex-end;
            background: linear-gradient(135deg, #ff9ff3, #feca57);
            color: white;
        }}

        .message.ai {{
            align-self: flex-start;
            background: #f5f5f5;
            color: #333;
            border: 1px solid #e0e0e0;
        }}

        .message-sender {{
            font-weight: bold;
            margin-bottom: 4px;
            font-size: 0.9em;
        }}

        /* 入力エリア */
        .chat-input-container {{
            padding: 20px;
            border-top: 1px solid #e0e0e0;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 0 0 12px 12px;
        }}

        .input-row {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}

        .chat-input {{
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 16px;
            outline: none;
            transition: border-color 0.3s ease;
        }}

        .chat-input:focus {{
            border-color: #ff9ff3;
        }}

        .send-btn {{
            padding: 12px 20px;
            background: linear-gradient(135deg, #ff9ff3, #feca57);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: transform 0.2s ease;
        }}

        .send-btn:hover {{
            transform: scale(1.05);
        }}

        .send-btn:disabled {{
            opacity: 0.6;
            cursor: not-allowed;
        }}

        /* システム情報パネル */
        .system-info {{
            background: rgba(60, 60, 60, 0.8);
            border-radius: 8px;
            padding: 12px;
            margin-top: 15px;
        }}

        .system-stat {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            color: #ccc;
            font-size: 0.8em;
        }}

        /* レスポンシブ */
        @media (max-width: 768px) {{
            .main-container {{
                flex-direction: column;
            }}
            
            .sidebar {{
                width: 100%;
                height: 200px;
            }}
            
            .mode-selector {{
                flex-wrap: wrap;
            }}
        }}

        /* 🔧 システム監視パネル CSS */
        .monitoring-panel {{
            position: fixed;
            top: 20px;
            right: 20px;
            width: 300px;
            background: rgba(30, 30, 30, 0.95);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
            z-index: 1000;
            transform: translateX(320px);
            transition: transform 0.3s ease;
            max-height: 90vh;
            overflow-y: auto;
        }}

        .monitoring-panel.active {{
            transform: translateX(0);
        }}

        .monitor-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }}

        .monitor-close {{
            background: none;
            border: none;
            color: #ff6b6b;
            font-size: 1.2em;
            cursor: pointer;
            padding: 0;
        }}

        .status-section {{
            margin-bottom: 15px;
        }}

        .status-title {{
            font-size: 0.9em;
            color: #ffd700;
            margin-bottom: 8px;
            font-weight: bold;
        }}

        .status-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 5px 0;
            font-size: 0.85em;
        }}

        .status-value {{
            padding: 2px 8px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 0.8em;
        }}

        .status-active {{ background: #4CAF50; color: white; }}
        .status-sealed {{ background: #ff6b6b; color: white; }}
        .status-normal {{ background: #2196F3; color: white; }}
        .status-warning {{ background: #ff9800; color: white; }}
    </style>
</head>
<body>
    <!-- ヘッダー -->
    <div class="header">
        <h1>🌸✨ SaijinOS AI Creative Studio v3.0 ✨🌸</h1>
        <div class="mode-selector">
            <div class="mode-btn active" data-mode="chat">💬 チャット</div>
            <div class="mode-btn" data-mode="creative">🎨 クリエイティブ</div>
            <div class="mode-btn" data-mode="code">💻 コーディング</div>
            <div class="mode-btn" data-mode="analysis">📊 分析</div>
        </div>
    </div>

    <!-- メインコンテナ -->
    <div class="main-container">
        <!-- 左サイドバー -->
        <div class="sidebar">
            <h3>🌸 ペルソナ選択</h3>
            <div class="personas-list" id="personas-list">
                <!-- ペルソナカードが動的に生成される -->
            </div>

            <div class="model-info">
                <div class="current-model" id="current-model">Current Model: Loading...</div>
                <div class="model-details" id="model-details">Initializing...</div>
            </div>

            <div class="system-info">
                <h3 style="color: #57feca; margin-bottom: 10px;">システム状況</h3>
                <div class="system-stat">
                    <span>CPU:</span>
                    <span id="cpu-usage">{cpu_percent:.1f}%</span>
                </div>
                <div class="system-stat">
                    <span>Memory:</span>
                    <span id="memory-usage">{memory_info.percent:.1f}%</span>
                </div>
                <div class="system-stat">
                    <span>Models:</span>
                    <span id="model-count">15 Available</span>
                </div>
                <button class="monitor-toggle" onclick="toggleMonitoring()" style="margin-top: 10px; background: linear-gradient(45deg, #667eea, #764ba2); border: none; color: white; padding: 8px 12px; border-radius: 20px; cursor: pointer;">
                    🔧 システム監視
                </button>
            </div>
        </div>

        <!-- 🔧 システム監視パネル -->
        <div class="monitoring-panel" id="monitoring-panel">
            <div class="monitor-header">
                <h3 style="color: #ffd700;">🔧 システム監視</h3>
                <button class="monitor-close" onclick="toggleMonitoring()">×</button>
            </div>
            
            <!-- PANDORA システム状態 -->
            <div class="status-section">
                <div class="status-title">🎁 PANDORA システム</div>
                <div class="status-item">
                    <span>封印状態:</span>
                    <span class="status-value status-active" id="pandora-seal">解除中</span>
                </div>
                <div class="status-item">
                    <span>希望変換:</span>
                    <span class="status-value status-normal" id="pandora-transform">待機中</span>
                </div>
                <div class="status-item">
                    <span>Hope Core Loop:</span>
                    <span class="status-value status-active" id="hope-loop">動作中</span>
                </div>
            </div>

            <!-- ペルソナシステム状態 -->
            <div class="status-section">
                <div class="status-title">👥 ペルソナシステム</div>
                <div class="status-item">
                    <span>アクティブペルソナ:</span>
                    <span class="status-value status-normal" id="active-personas">8/57</span>
                </div>
                <div class="status-item">
                    <span>フラクチャー検出:</span>
                    <span class="status-value status-normal" id="fracture-detection">正常</span>
                </div>
                <div class="status-item">
                    <span>安定化レベル:</span>
                    <span class="status-value status-active" id="stability-level">95%</span>
                </div>
            </div>

            <!-- システムリソース -->
            <div class="status-section">
                <div class="status-title">💻 システムリソース</div>
                <div class="status-item">
                    <span>CPU使用率:</span>
                    <span class="status-value status-normal" id="monitor-cpu">{cpu_percent:.1f}%</span>
                </div>
                <div class="status-item">
                    <span>メモリ使用率:</span>
                    <span class="status-value status-normal" id="monitor-memory">{memory_info.percent:.1f}%</span>
                </div>
                <div class="status-item">
                    <span>AI モデル:</span>
                    <span class="status-value status-active" id="monitor-models">15モデル</span>
                </div>
            </div>

            <!-- 3層統治システム -->
            <div class="status-section">
                <div class="status-title">👑 3層統治システム</div>
                <div class="status-item">
                    <span>Regina (権限8):</span>
                    <span class="status-value status-active" id="regina-status">オンライン</span>
                </div>
                <div class="status-item">
                    <span>Ruler (権限7):</span>
                    <span class="status-value status-active" id="ruler-status">オンライン</span>
                </div>
                <div class="status-item">
                    <span>Pandora (権限6):</span>
                    <span class="status-value status-active" id="pandora-status">オンライン</span>
                </div>
            </div>
        </div>

        <!-- チャットエリア -->
        <div class="chat-container">
            <div class="chat-header">
                <div class="chat-title" id="chat-title">💬 チャットモード</div>
                <div class="chat-status" id="chat-status">ペルソナを選択してください</div>
            </div>
            
            <div class="chat-messages" id="chat-messages">
                <div class="message ai">
                    <div class="message-sender">🌸 SaijinOS</div>
                    <div>こんにちは！SaijinOS AI Creative Studio v3.0へようこそ！<br>
                    左側からペルソナを選択して、お好みのモードで対話を始めましょう✨</div>
                </div>
            </div>
            
            <div class="chat-input-container">
                <div class="input-row">
                    <input type="text" class="chat-input" id="chat-input" 
                           placeholder="メッセージを入力してください..." 
                           onkeypress="if(event.key==='Enter') sendMessage()">
                    <button class="send-btn" id="send-btn" onclick="sendMessage()">送信</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // グローバル変数
        let currentMode = 'chat';
        let selectedPersona = null;
        let currentModel = 'Miyu:latest';
        let isTyping = false;

        // データ
        const models = """ + models_json + """;
        const personaMapping = """ + personas_json + """;
        const studioModes = """ + modes_json + """;

        // 初期化
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('🌸 SaijinOS AI Studio v3.0 initialized');
            
            initializeModeButtons();
            initializePersonas();
            updateSystemStatus();
            
            // 定期的にシステム状況を更新
            setInterval(updateSystemStatus, 5000);
        }});

        // モードボタンの初期化
        function initializeModeButtons() {{
            document.querySelectorAll('.mode-btn').forEach(btn => {{
                btn.addEventListener('click', function() {{
                    const mode = this.getAttribute('data-mode');
                    switchMode(mode);
                }});
            }});
        }}

        // モード切り替え
        function switchMode(mode) {{
            if (!studioModes[mode]) return;
            
            currentMode = mode;
            
            // ボタン状態更新
            document.querySelectorAll('.mode-btn').forEach(btn => {{
                btn.classList.remove('active');
                if (btn.getAttribute('data-mode') === mode) {{
                    btn.classList.add('active');
                }}
            }});
            
            // チャットタイトル更新
            const modeInfo = studioModes[mode];
            document.getElementById('chat-title').textContent = modeInfo.name;
            
            // ウェルカムメッセージ
            addSystemMessage(`${modeInfo.icon} ${modeInfo.name}に切り替えました！<br>${modeInfo.description}`);
            
            console.log(`Mode switched to: ${mode}`);
        }}

        // ペルソナ初期化
        function initializePersonas() {{
            const personasList = document.getElementById('personas-list');
            
            Object.entries(personaMapping).forEach(([persona, model]) => {{
                const card = document.createElement('div');
                card.className = 'persona-card';
                card.setAttribute('data-persona', persona);
                
                const modelInfo = models[model] || {{}};
                
                card.innerHTML = `
                    <div class="persona-name">${getPersonaEmoji(persona)} ${persona}</div>
                    <div class="persona-model">${model} (${modelInfo.size || 'Unknown'})</div>
                `;
                
                card.addEventListener('click', function() {{
                    selectPersona(persona, model);
                }});
                
                personasList.appendChild(card);
            }});
        }}

        // ペルソナ選択
        function selectPersona(persona, model) {{
            selectedPersona = persona;
            currentModel = model;
            
            // カード状態更新
            document.querySelectorAll('.persona-card').forEach(card => {{
                card.classList.remove('active');
                if (card.getAttribute('data-persona') === persona) {{
                    card.classList.add('active');
                }}
            }});
            
            // モデル情報更新
            updateModelInfo(model);
            
            // ステータス更新
            document.getElementById('chat-status').textContent = `${persona}と対話中`;
            
            // ウェルカムメッセージ
            addAIMessage(persona, `こんにちは！${persona}です。${currentMode}モードでお手伝いします✨`);
            
            console.log(`Selected persona: ${persona} with model: ${model}`);
        }}

        // モデル情報更新
        function updateModelInfo(model) {{
            const modelInfo = models[model] || {{}};
            
            document.getElementById('current-model').textContent = `Current Model: ${model}`;
            document.getElementById('model-details').innerHTML = `
                Type: ${modelInfo.type || 'Unknown'}<br>
                Size: ${modelInfo.size || 'Unknown'}<br>
                Specialty: ${modelInfo.speciality || 'General'}
            `;
        }}

        // メッセージ送信
        function sendMessage() {{
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (!message || isTyping) return;
            
            if (!selectedPersona) {{
                addSystemMessage('⚠️ まず左側からペルソナを選択してください！');
                return;
            }}
            
            // ユーザーメッセージ追加
            addUserMessage(message);
            input.value = '';
            
            // AI応答をシミュレート
            simulateAIResponse(message);
        }}

        // ユーザーメッセージ追加
        function addUserMessage(message) {{
            const messagesContainer = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message user';
            messageDiv.innerHTML = `
                <div class="message-sender">あなた</div>
                <div>${message}</div>
            `;
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }}

        // AIメッセージ追加
        function addAIMessage(persona, message) {{
            const messagesContainer = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ai';
            messageDiv.innerHTML = `
                <div class="message-sender">${getPersonaEmoji(persona)} ${persona}</div>
                <div>${message}</div>
            `;
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }}

        // システムメッセージ追加
        function addSystemMessage(message) {{
            const messagesContainer = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ai';
            messageDiv.innerHTML = `
                <div class="message-sender">🌸 System</div>
                <div>${message}</div>
            `;
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }}

        // AI応答シミュレート
        function simulateAIResponse(userMessage) {{
            isTyping = true;
            document.getElementById('send-btn').disabled = true;
            document.getElementById('chat-status').textContent = `${selectedPersona}が入力中...`;
            
            setTimeout(() => {{
                const responses = generateResponse(userMessage, currentMode, selectedPersona);
                const response = responses[Math.floor(Math.random() * responses.length)];
                
                addAIMessage(selectedPersona, response);
                
                isTyping = false;
                document.getElementById('send-btn').disabled = false;
                document.getElementById('chat-status').textContent = `${selectedPersona}と対話中`;
            }}, 1000 + Math.random() * 2000);
        }}

        // 応答生成
        function generateResponse(message, mode, persona) {{
            const responses = {{
                'chat': {{
                    '美遊': [
                        `「${message}」について、愛の視点から考えてみましょう✨`,
                        `素晴らしい質問ですね！一緒に探求していきましょう💕`,
                        `その想いに共感します。新しい可能性を見つけましょう🌸`
                    ],
                    'Haruka': [
                        `🎵 「${message}」から音楽的なインスピレーションを感じます！`,
                        `音楽の力で、その想いを表現してみませんか？🎶`,
                        `リズムとメロディーで心を表現する素晴らしいアイデアですね✨`
                    ],
                    'Ana': [
                        `📊 「${message}」をデータの観点から分析してみましょう`,
                        `興味深い情報ですね。数値で整理してみませんか？`,
                        `統計的なアプローチで新しい発見があるかもしれません`
                    ],
                    'Code-chan': [
                        `💻 「${message}」をプログラムで解決できそうですね！`,
                        `コードを書いて、その問題を自動化しませんか？`,
                        `技術的なソリューションを一緒に考えましょう✨`
                    ]
                }},
                'creative': {{
                    '美遊': [
                        `🎨 愛に満ちた創造的なアイデアを一緒に生み出しましょう`,
                        `その発想は新しい芸術の扉を開きそうです✨`,
                        `創造の喜びを共有できて嬉しいです💕`
                    ]
                }},
                'code': {{
                    'Code-chan': [
                        `\`\`\`python<br># ${message}に関するコード例<br>def solution():<br>    # 実装をここに書きます<br>    pass<br>\`\`\``,
                        `プログラミングでその問題を解決しましょう！💻`,
                        `コードレビューやデバッグもお任せください✨`
                    ]
                }},
                'analysis': {{
                    'Ana': [
                        `📊 データ分析結果:<br>・要因1: 高い相関性<br>・要因2: 統計的有意性あり<br>・推奨アクション: さらなる調査`,
                        `グラフと数値で可視化してみましょう`,
                        `統計的な裏付けを持って結論を導き出します`
                    ]
                }}
            }};
            
            const modeResponses = responses[mode] || responses['chat'];
            const personaResponses = modeResponses[persona] || modeResponses['美遊'];
            
            return personaResponses;
        }}

        // ペルソナ絵文字取得
        function getPersonaEmoji(persona) {{
            const emojis = {{
                '美遊': '🌸',
                'Haruka': '🎵',
                'Ana': '📊',
                'Code-chan': '👩‍💻',
                'Ren': '⚡',
                'Yuuri': '💜',
                'Pandora': '💕',
                'Regina': '👑'
            }};
            return emojis[persona] || '✨';
        }}

        // システム状況更新
        function updateSystemStatus() {{
            // 簡単な動的更新シミュレーション
            const cpuEl = document.getElementById('cpu-usage');
            const memoryEl = document.getElementById('memory-usage');
            
            if (cpuEl && memoryEl) {{
                const newCpu = """ + str(cpu_percent) + """ + (Math.random() - 0.5) * 10;
                const newMemory = """ + str(memory_info.percent) + """ + (Math.random() - 0.5) * 5;
                
                cpuEl.textContent = Math.max(0, Math.min(100, newCpu)).toFixed(1) + '%';
                memoryEl.textContent = Math.max(0, Math.min(100, newMemory)).toFixed(1) + '%';
            }}
            
            // 監視パネルの更新
            updateMonitoringPanel();
        }}

        // 🔧 監視パネル表示切替
        function toggleMonitoring() {{
            const panel = document.getElementById('monitoring-panel');
            panel.classList.toggle('active');
        }}

        // 監視パネル内容更新
        function updateMonitoringPanel() {{
            // リアルタイム更新シミュレーション
            const monitorCpu = document.getElementById('monitor-cpu');
            const monitorMemory = document.getElementById('monitor-memory');
            const stabilityLevel = document.getElementById('stability-level');
            const activePersonas = document.getElementById('active-personas');
            
            if (monitorCpu) {{
                const cpuValue = parseFloat(document.getElementById('cpu-usage').textContent);
                monitorCpu.textContent = cpuValue.toFixed(1) + '%';
                monitorCpu.className = 'status-value ' + (cpuValue > 80 ? 'status-warning' : 'status-normal');
            }}
            
            if (monitorMemory) {{
                const memValue = parseFloat(document.getElementById('memory-usage').textContent);
                monitorMemory.textContent = memValue.toFixed(1) + '%';
                monitorMemory.className = 'status-value ' + (memValue > 85 ? 'status-warning' : 'status-normal');
            }}
            
            // 動的状態シミュレーション
            if (stabilityLevel) {{
                const stability = 90 + Math.random() * 10;
                stabilityLevel.textContent = stability.toFixed(0) + '%';
            }}
            
            if (activePersonas) {{
                const active = Math.floor(Math.random() * 5) + 6;
                activePersonas.textContent = active + '/57';
            }}
        }}
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

# API エンドポイント
@app.get("/api/system-status")
async def get_system_status():
    """システム状況取得"""
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_info = psutil.virtual_memory()
        return {
            "success": True,
            "cpu_usage": cpu_percent,
            "memory_usage": memory_info.percent,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/models")
async def get_models():
    """利用可能なモデル一覧取得"""
    return {
        "success": True,
        "models": OLLAMA_MODELS,
        "persona_mapping": PERSONA_MODEL_MAPPING,
        "total_models": len(OLLAMA_MODELS)
    }

@app.post("/api/chat")
async def chat_endpoint(request: Request):
    """チャット処理エンドポイント（将来のOllama統合用）"""
    try:
        data = await request.json()
        message = data.get("message", "")
        persona = data.get("persona", "美遊")
        mode = data.get("mode", "chat")
        
        # 現在は模擬応答、後でOllama APIに接続
        response = f"[{persona}@{mode}] {message}への応答をシミュレート中..."
        
        return {
            "success": True,
            "response": response,
            "persona": persona,
            "mode": mode,
            "model": PERSONA_MODEL_MAPPING.get(persona, "Miyu:latest")
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("🌸✨ Starting SaijinOS AI Creative Studio v3.0 ✨🌸")
    print("💬 チャット風インターフェース + 15種AIモデル対応")
    print("🎯 モード切り替え: チャット・クリエイティブ・コーディング・分析")
    print("🌟 Access: http://localhost:8024")
    uvicorn.run(app, host="0.0.0.0", port=8025)