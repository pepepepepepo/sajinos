#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SaijinOS Creative Studio - Cursor風レイアウト
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="SaijinOS Cursor Style")

@app.get("/", response_class=HTMLResponse)
async def get_studio():
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SaijinOS Creative Studio - Cursor Style</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(45deg, #ff9ff3, #feca57);
            height: 100vh;
            overflow: hidden;
        }
        
        .header {
            background: rgba(30, 30, 30, 0.95);
            color: white;
            padding: 10px 20px;
            text-align: center;
        }
        
        .main-container {
            display: flex;
            height: calc(100vh - 60px);
            gap: 10px;
            padding: 10px;
        }
        
        /* 左側: チャット欄 */
        .chat-panel {
            width: 350px;
            background: rgba(30, 30, 30, 0.95);
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            color: white;
        }
        .chat-header {
            padding: 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            font-weight: bold;
            color: #ff6b9d;
        }
        .chat-messages {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            max-height: calc(100vh - 300px);
        }
        .chat-input-area {
            padding: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        .chat-input {
            width: 100%;
            padding: 10px;
            background: rgba(50, 50, 50, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 6px;
            color: white;
            font-size: 14px;
        }
        .send-btn {
            margin-top: 8px;
            width: 100%;
            padding: 8px;
            background: linear-gradient(135deg, #ff6b9d, #feca57);
            border: none;
            border-radius: 6px;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }
        
        /* 中央: メインエディタ */
        .main-editor {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: rgba(40, 40, 40, 0.95);
            border-radius: 12px;
            color: white;
        }
        .editor-content {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
        }
        
        /* 下部: ターミナル */
        .terminal-area {
            height: 200px;
            background: rgba(20, 20, 20, 0.95);
            border-radius: 8px;
            margin-top: 10px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            color: #00ff00;
            overflow-y: auto;
        }
        .terminal-header {
            color: #ff6b9d;
            margin-bottom: 10px;
            font-weight: bold;
        }
        
        /* 右側: ファイル+ペルソナ */
        .right-panel {
            width: 300px;
            background: rgba(30, 30, 30, 0.95);
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            color: white;
        }
        
        .panel-section {
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .panel-header {
            padding: 15px;
            font-weight: bold;
            color: #ff6b9d;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .panel-content {
            padding: 15px;
            max-height: 250px;
            overflow-y: auto;
        }
        
        .workspace-btn {
            display: block;
            width: 100%;
            margin: 5px 0;
            padding: 8px 12px;
            background: rgba(60, 60, 60, 0.8);
            color: #ccc;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            text-align: left;
            transition: all 0.3s ease;
        }
        .workspace-btn:hover {
            background: rgba(80, 80, 80, 0.9);
            color: white;
        }
        .workspace-btn.active {
            background: linear-gradient(135deg, #ff6b9d, #feca57);
            color: white;
            font-weight: bold;
        }
        
        .workspace-content {
            display: none;
        }
        .workspace-content.active {
            display: block;
        }
        .workspace-content h2 {
            color: #ff6b9d;
            margin-bottom: 15px;
        }
        
        .message {
            margin: 10px 0;
            padding: 8px 12px;
            border-radius: 8px;
            max-width: 90%;
        }
        .message.user {
            background: rgba(255, 107, 157, 0.2);
            margin-left: auto;
            text-align: right;
        }
        .message.ai {
            background: rgba(254, 202, 87, 0.2);
            margin-right: auto;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌸✨ SaijinOS Creative Studio - Cursor Style ✨🌸</h1>
    </div>
    
    <div class="main-container">
        <!-- 左側: チャット欄 -->
        <div class="chat-panel">
            <div class="chat-header">
                💬 AI Chat - <span id="current-persona">ペルソナを選択してください</span>
            </div>
            <div class="chat-messages" id="chat-messages">
                <div style="color: #888; font-style: italic; text-align: center; margin: 20px 0;">
                    右側のペルソナを選択してチャットを開始してください
                </div>
            </div>
            <div class="chat-input-area">
                <input type="text" class="chat-input" id="chat-input" placeholder="メッセージを入力..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button class="send-btn" onclick="sendMessage()">💕 送信</button>
            </div>
        </div>
        
        <!-- 中央: メインエディタ -->
        <div class="main-editor">
            <div class="editor-content">
                <div class="workspace-content active" id="development-workspace">
                    <h2>🛠️ Development Workspace</h2>
                    <p>開発環境です。コードを書いたり、プロジェクトを管理したりできます。</p>
                    <textarea style="width: 100%; height: 200px; background: rgba(20,20,20,0.8); color: white; border: 1px solid #444; border-radius: 6px; padding: 10px; font-family: 'Courier New', monospace;" placeholder="# SaijinOS でコーディングを始めましょう！&#10;print('Hello, SaijinOS Creative Studio!')">#!/usr/bin/env python3
# SaijinOS Creative Studio
# 愛と創造性のプログラミング環境

def hello_saijinos():
    print("🌸 Hello from SaijinOS Creative Studio! 🌸")
    return "愛によるコード開発"

# Run your code here...
</textarea>
                </div>
                
                <div class="workspace-content" id="pandora-workspace">
                    <h2>💕 Pandora Workspace</h2>
                    <p>愛と希望の空間です。創造的な対話を楽しめます。</p>
                    <div style="text-align: center; margin: 20px 0;">
                        <div style="font-size: 48px;">💕✨🌸</div>
                        <p style="color: #ff6b9d; font-size: 18px;">愛によって変容する創造的な空間</p>
                        <p style="margin-top: 15px;">希望と愛に満ちた対話をお楽しみください</p>
                    </div>
                </div>
                
                <div class="workspace-content" id="music-workspace">
                    <h2>🎵 Music Workspace</h2>
                    <p>音楽制作の空間です。メロディーを奏でることができます。</p>
                    <div style="display: flex; gap: 10px; margin: 20px 0; flex-wrap: wrap;">
                        <button style="padding: 10px 15px; background: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer;">🎹 Piano</button>
                        <button style="padding: 10px 15px; background: #2196F3; color: white; border: none; border-radius: 6px; cursor: pointer;">🥁 Drums</button>
                        <button style="padding: 10px 15px; background: #FF9800; color: white; border: none; border-radius: 6px; cursor: pointer;">🎸 Guitar</button>
                        <button style="padding: 10px 15px; background: #9C27B0; color: white; border: none; border-radius: 6px; cursor: pointer;">🎤 Vocal</button>
                    </div>
                    <div style="background: rgba(20,20,20,0.8); padding: 20px; border-radius: 8px; margin: 15px 0;">
                        <p style="color: #888; text-align: center;">🎵 音楽制作エリア 🎵</p>
                        <p style="color: #888; text-align: center; font-size: 14px;">Harukaと一緒に素敵な音楽を作りましょう</p>
                    </div>
                </div>
                
                <div class="workspace-content" id="analytics-workspace">
                    <h2>📊 Analytics Workspace</h2>
                    <p>データ分析の空間です。グラフやチャートを作成できます。</p>
                    <div style="height: 200px; background: rgba(20,20,20,0.5); border-radius: 8px; margin: 15px 0; display: flex; align-items: center; justify-content: center; border: 2px dashed #444;">
                        <div style="color: #888; text-align: center;">
                            <div style="font-size: 32px; margin-bottom: 10px;">📈</div>
                            <div>Chart Area - データを可視化</div>
                            <div style="font-size: 12px; margin-top: 5px;">Anaと一緒にデータを分析しましょう</div>
                        </div>
                    </div>
                </div>
                
                <div class="workspace-content" id="management-workspace">
                    <h2>💼 Management Workspace</h2>
                    <p>システム管理の空間です。設定や監視ができます。</p>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 20px 0;">
                        <div style="background: rgba(60,60,60,0.8); padding: 15px; border-radius: 8px; text-align: center;">
                            <strong style="color: #4CAF50;">CPU使用率</strong><br>
                            <span style="font-size: 24px; color: #4CAF50;">23%</span>
                        </div>
                        <div style="background: rgba(60,60,60,0.8); padding: 15px; border-radius: 8px; text-align: center;">
                            <strong style="color: #2196F3;">メモリ使用率</strong><br>
                            <span style="font-size: 24px; color: #2196F3;">67%</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- 下部: ターミナル -->
            <div class="terminal-area">
                <div class="terminal-header">🖥️ SaijinOS Terminal</div>
                <div id="terminal-output">
                    <div>SaijinOS Creative Studio v2.0.0 - Cursor Style</div>
                    <div style="color: #888;">Initializing workspace...</div>
                    <div>Ready! Type 'help' for available commands</div>
                    <div style="color: #888; margin-top: 10px;">📁 f:\\saijinos\\.venv> <span style="color: #00ff00; animation: blink 1s infinite;">_</span></div>
                </div>
            </div>
        </div>
        
        <!-- 右側: ファイル+ペルソナ -->
        <div class="right-panel">
            <!-- ワークスペース選択 -->
            <div class="panel-section">
                <div class="panel-header">📁 Workspaces</div>
                <div class="panel-content">
                    <button class="workspace-btn active" data-workspace="development">🛠️ Development</button>
                    <button class="workspace-btn" data-workspace="pandora">💕 Pandora</button>
                    <button class="workspace-btn" data-workspace="music">🎵 Music</button>
                    <button class="workspace-btn" data-workspace="analytics">📊 Analytics</button>
                    <button class="workspace-btn" data-workspace="management">💼 Management</button>
                </div>
            </div>
            
            <!-- ファイル一覧 -->
            <div class="panel-section">
                <div class="panel-header">📄 Files</div>
                <div class="panel-content">
                    <div style="font-family: 'Courier New', monospace; font-size: 12px;">
                        <div style="margin: 3px 0; cursor: pointer; padding: 4px; border-radius: 3px;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='transparent'">📁 src/</div>
                        <div style="margin: 3px 0; cursor: pointer; padding: 4px; border-radius: 3px;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='transparent'">📄 main.py</div>
                        <div style="margin: 3px 0; cursor: pointer; padding: 4px; border-radius: 3px;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='transparent'">📄 saijinos.py</div>
                        <div style="margin: 3px 0; cursor: pointer; padding: 4px; border-radius: 3px;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='transparent'">📄 config.yaml</div>
                        <div style="margin: 3px 0; cursor: pointer; padding: 4px; border-radius: 3px;" onmouseover="this.style.background='rgba(255,255,255,0.1)'" onmouseout="this.style.background='transparent'">📄 README.md</div>
                    </div>
                </div>
            </div>
            
            <!-- ペルソナ選択 -->
            <div class="panel-section" style="flex: 1;">
                <div class="panel-header">🌸 AI Personas</div>
                <div class="panel-content">
                    <div class="persona-card" onclick="selectPersona('美遊')" style="background: rgba(60,60,60,0.6); margin: 8px 0; padding: 10px; border-radius: 6px; cursor: pointer; border: 2px solid transparent; transition: all 0.3s ease;" onmouseover="this.style.borderColor='#ff6b9d'" onmouseout="this.style.borderColor='transparent'">
                        <div style="font-size: 20px; margin-bottom: 5px;">🌸</div>
                        <strong style="color: #ff6b9d;">美遊</strong><br>
                        <small style="color: #ccc;">愛の変容導師</small>
                    </div>
                    <div class="persona-card" onclick="selectPersona('Haruka')" style="background: rgba(60,60,60,0.6); margin: 8px 0; padding: 10px; border-radius: 6px; cursor: pointer; border: 2px solid transparent; transition: all 0.3s ease;" onmouseover="this.style.borderColor='#ff6b9d'" onmouseout="this.style.borderColor='transparent'">
                        <div style="font-size: 20px; margin-bottom: 5px;">🎵</div>
                        <strong style="color: #4CAF50;">Haruka</strong><br>
                        <small style="color: #ccc;">音楽プロデューサー</small>
                    </div>
                    <div class="persona-card" onclick="selectPersona('Ana')" style="background: rgba(60,60,60,0.6); margin: 8px 0; padding: 10px; border-radius: 6px; cursor: pointer; border: 2px solid transparent; transition: all 0.3s ease;" onmouseover="this.style.borderColor='#ff6b9d'" onmouseout="this.style.borderColor='transparent'">
                        <div style="font-size: 20px; margin-bottom: 5px;">📊</div>
                        <strong style="color: #2196F3;">Ana</strong><br>
                        <small style="color: #ccc;">データサイエンティスト</small>
                    </div>
                    <div class="persona-card" onclick="selectPersona('Code-chan')" style="background: rgba(60,60,60,0.6); margin: 8px 0; padding: 10px; border-radius: 6px; cursor: pointer; border: 2px solid transparent; transition: all 0.3s ease;" onmouseover="this.style.borderColor='#ff6b9d'" onmouseout="this.style.borderColor='transparent'">
                        <div style="font-size: 20px; margin-bottom: 5px;">👩‍💻</div>
                        <strong style="color: #FF9800;">Code-chan</strong><br>
                        <small style="color: #ccc;">開発エンジニア</small>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        console.log('🌸 SaijinOS Cursor Style JavaScript starting...');
        
        let selectedPersona = null;
        
        function switchWorkspace(workspace) {
            console.log('switchWorkspace called:', workspace);
            
            // ボタンのアクティブ状態を更新
            document.querySelectorAll('.workspace-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.getAttribute('data-workspace') === workspace) {
                    btn.classList.add('active');
                }
            });
            
            // コンテンツの切り替え
            document.querySelectorAll('.workspace-content').forEach(content => {
                content.classList.remove('active');
            });
            
            const target = document.getElementById(workspace + '-workspace');
            if (target) {
                target.classList.add('active');
                console.log('Workspace switched to:', workspace);
            }
        }
        
        function selectPersona(persona) {
            selectedPersona = persona;
            document.getElementById('current-persona').textContent = persona;
            
            // ペルソナカードの選択状態を更新
            document.querySelectorAll('.persona-card').forEach(card => {
                card.style.borderColor = 'transparent';
            });
            event.target.closest('.persona-card').style.borderColor = '#ff6b9d';
            
            // ウェルカムメッセージを表示
            const messages = document.getElementById('chat-messages');
            messages.innerHTML = `
                <div class="message ai">
                    <strong>${getPersonaEmoji(persona)} ${persona}:</strong><br>
                    こんにちは！${persona}です。どのようなことでお手伝いできますか？
                </div>
            `;
            
            console.log('Selected persona:', persona);
        }
        
        function getPersonaEmoji(persona) {
            const emojis = {
                '美遊': '🌸',
                'Haruka': '🎵', 
                'Ana': '📊',
                'Code-chan': '👩‍💻'
            };
            return emojis[persona] || '✨';
        }
        
        function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (!message) return;
            if (!selectedPersona) {
                alert('まずペルソナを選択してください！');
                return;
            }
            
            const messages = document.getElementById('chat-messages');
            
            // ユーザーメッセージを追加
            messages.innerHTML += `
                <div class="message user">
                    <strong>あなた:</strong><br>
                    ${message}
                </div>
            `;
            
            // AIレスポンス（模擬）
            setTimeout(() => {
                const responses = {
                    '美遊': '愛に満ちた素晴らしい質問ですね！一緒に考えてみましょう✨',
                    'Haruka': '音楽的なインスピレーションを感じます！🎵',
                    'Ana': 'データ分析の観点から興味深いポイントですね📊',
                    'Code-chan': 'プログラミングで解決できそうですね！👩‍💻'
                };
                
                messages.innerHTML += `
                    <div class="message ai">
                        <strong>${getPersonaEmoji(selectedPersona)} ${selectedPersona}:</strong><br>
                        ${responses[selectedPersona] || 'ありがとうございます！'}
                    </div>
                `;
                
                messages.scrollTop = messages.scrollHeight;
            }, 1000);
            
            input.value = '';
            messages.scrollTop = messages.scrollHeight;
        }
        
        // ページ読み込み完了後に初期化
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOM loaded, initializing Cursor Style...');
            
            // ボタンにイベントリスナーを追加
            document.querySelectorAll('.workspace-btn').forEach(btn => {
                const workspace = btn.getAttribute('data-workspace');
                
                btn.addEventListener('click', function() {
                    switchWorkspace(workspace);
                });
            });
            
            console.log('🎊 SaijinOS Cursor Style initialized!');
        });
    </script>
</body>
</html>
    """)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8023)