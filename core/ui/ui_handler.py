"""
SaijinOS UI Handler
Enhanced with Multi-Mode UI System
"""
import os

class UIHandler:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    def get_ide_content(self):
        """IDE Mode Interface with Mode Switcher and Fixed Outline"""
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>💻 SaijinOS IDE Mode</title>
    <style>
        body {
            margin: 0;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            background: #1e1e1e;
            color: #d4d4d4;
            overflow: hidden;
        }
        
        .mode-switcher {
            position: fixed;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            background: rgba(40, 40, 40, 0.95);
            border-radius: 15px;
            padding: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            backdrop-filter: blur(10px);
            border: 1px solid #464647;
        }
        
        .mode-btn {
            display: inline-block;
            margin: 2px;
            padding: 6px 10px;
            background: rgba(200, 200, 200, 0.1);
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 11px;
            transition: all 0.2s ease;
            text-decoration: none;
            color: #cccccc;
        }
        
        .mode-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-1px);
        }
        
        .mode-btn.active {
            background: #007acc;
            color: white;
        }
        
        .ide-container {
            display: flex;
            height: 100vh;
            flex-direction: column;
        }
        
        .toolbar {
            height: 50px;
            background: #2d2d30;
            display: flex;
            align-items: center;
            padding: 0 15px;
            border-bottom: 1px solid #3e3e42;
            margin-top: 50px;
        }
        
        .toolbar h1 {
            margin: 0;
            color: #cccccc;
            font-size: 18px;
            font-weight: normal;
        }
        
        .main-content {
            display: flex;
            flex: 1;
            overflow: hidden;
        }
        
        .activity-bar {
            width: 48px;
            background: #333333;
            border-right: 1px solid #3e3e42;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 10px 0;
        }
        
        .activity-icon {
            width: 32px;
            height: 32px;
            margin: 8px 0;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            border-radius: 4px;
            color: #cccccc;
            font-size: 18px;
        }
        
        .activity-icon:hover {
            background: #37373d;
        }
        
        .activity-icon.active {
            background: #007acc;
            color: white;
        }
        
        .sidebar {
            width: 300px;
            background: #252526;
            border-right: 1px solid #3e3e42;
            display: flex;
            flex-direction: column;
            min-width: 250px;
            max-width: 400px;
        }
        
        .explorer-header {
            padding: 12px 15px;
            background: #2d2d30;
            color: #cccccc;
            font-size: 14px;
            font-weight: bold;
            border-bottom: 1px solid #3e3e42;
        }
        
        .file-tree {
            flex: 1;
            padding: 10px 0;
            overflow-y: auto;
        }
        
        .file-item {
            padding: 4px 20px;
            cursor: pointer;
            font-size: 14px;
            color: #cccccc;
            display: flex;
            align-items: center;
        }
        
        .file-item:hover {
            background: #2a2d2e;
        }
        
        .file-item.selected {
            background: #094771;
            color: #ffffff;
        }
        
        .file-icon {
            width: 16px;
            margin-right: 8px;
        }
        
        .folder {
            color: #dcb67a;
        }
        
        .folder.expanded::before {
            content: "📁 ";
        }
        
        .folder.collapsed::before {
            content: "📂 ";
        }
        
        .file::before {
            content: "📄 ";
        }
        
        .editor-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: #1e1e1e;
        }
        
        .tab-bar {
            height: 35px;
            background: #2d2d30;
            border-bottom: 1px solid #3e3e42;
            display: flex;
            align-items: center;
        }
        
        .tab {
            height: 35px;
            padding: 0 15px;
            background: #2d2d30;
            border-right: 1px solid #3e3e42;
            display: flex;
            align-items: center;
            cursor: pointer;
            color: #969696;
        }
        
        .tab.active {
            background: #1e1e1e;
            color: #ffffff;
        }
        
        .editor {
            flex: 1;
            background: #1e1e1e;
            padding: 20px;
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
            color: #d4d4d4;
            overflow: auto;
            white-space: pre-wrap;
        }
        
        .secondary-sidebar {
            width: 280px;
            background: #252526;
            border-left: 1px solid #3e3e42;
            display: flex;
            flex-direction: column;
            min-width: 200px;
        }
        
        .panel-tabs {
            display: flex;
            background: #2d2d30;
            border-bottom: 1px solid #3e3e42;
        }
        
        .panel-tab {
            padding: 8px 12px;
            cursor: pointer;
            font-size: 12px;
            color: #cccccc;
            border-right: 1px solid #3e3e42;
            transition: all 0.2s ease;
        }
        
        .panel-tab.active {
            background: #252526;
            color: white;
        }
        
        .panel-tab:hover {
            background: #37373d;
        }
        
        .panel-content {
            flex: 1;
            overflow: hidden;
        }
        
        .outline-header {
            padding: 12px 15px;
            background: #2d2d30;
            color: #cccccc;
            font-size: 14px;
            font-weight: bold;
            border-bottom: 1px solid #3e3e42;
        }
        
        .outline-content {
            flex: 1;
            padding: 10px 0;
            overflow-y: auto;
        }
        
        .outline-item {
            padding: 4px 20px;
            cursor: pointer;
            font-size: 13px;
            color: #cccccc;
            display: flex;
            align-items: center;
        }
        
        .outline-item:hover {
            background: #2a2d2e;
        }
        
        .outline-item.function::before {
            content: "🔧 ";
            color: #569cd6;
        }
        
        .outline-item.class::before {
            content: "📦 ";
            color: #4ec9b0;
        }
        
        .outline-item.variable::before {
            content: "📊 ";
            color: #9cdcfe;
        }
        
        .status-bar {
            height: 25px;
            background: #007acc;
            color: white;
            display: flex;
            align-items: center;
            padding: 0 15px;
            font-size: 12px;
        }
        
        /* VSCode風レスポンシブデザイン */
        @media (max-width: 1200px) {
            .sidebar {
                width: 250px;
            }
            .secondary-sidebar {
                width: 200px;
            }
        }
        
        @media (max-width: 992px) {
            .secondary-sidebar {
                width: 100%;
                height: 200px;
                border-left: none;
                border-top: 1px solid #3e3e42;
                order: 3;
            }
            .editor-area {
                order: 2;
            }
        }
        
        @media (max-width: 768px) {
            .activity-bar {
                width: 40px;
            }
            .sidebar {
                width: 200px;
            }
            .main-content {
                flex-wrap: wrap;
            }
        }
        
        @media (max-width: 640px) {
            .activity-bar {
                height: 48px;
                width: 100%;
                flex-direction: row;
                justify-content: space-around;
                order: 0;
            }
            .sidebar {
                width: 100%;
                height: 150px;
                border-right: none;
                border-bottom: 1px solid #3e3e42;
                order: 1;
            }
            .main-content {
                flex-direction: column;
            }
        }
        
        /* パネルのボックスサイジング */
        .panel-content {
            box-sizing: border-box;
            overflow-y: auto;
        }
        
        /* モバイルでもアウトラインを保持 */
        @media (max-width: 480px) {
            .mode-switcher {
                position: fixed;
                bottom: 10px;
                left: 50%;
                transform: translateX(-50%);
                top: auto;
                right: auto;
                background: rgba(0,0,0,0.8);
                border-radius: 25px;
                padding: 5px;
            }
            
            .mode-btn {
                padding: 6px 10px;
                font-size: 10px;
                color: white;
                background: transparent;
            }
            
            .mode-btn.active {
                background: rgba(255,255,255,0.2);
            }
        }
    </style>
</head>
<body>
    <!-- Mode Switcher -->
    <div class="mode-switcher">
        <a href="/ide" class="mode-btn active">💻 IDE</a>
        <a href="/chat" class="mode-btn">💬 Chat</a>
        <a href="/creative" class="mode-btn">🎨 Creative</a>
        <a href="/control-panel" class="mode-btn">📊 Dashboard</a>
    </div>

    <div class="ide-container">
        <div class="toolbar">
            <h1>💻 SaijinOS IDE - Phase 3 Development Environment</h1>
        </div>
        
        <div class="main-content">
            <!-- Activity Bar (VSCode左端) -->
            <div class="activity-bar">
                <div class="activity-icon active" onclick="switchPanel('explorer')" title="Explorer">
                    📁
                </div>
                <div class="activity-icon" onclick="switchPanel('search')" title="Search">
                    🔍
                </div>
                <div class="activity-icon" onclick="switchPanel('git')" title="Source Control">
                    🌿
                </div>
                <div class="activity-icon" onclick="switchPanel('debug')" title="Run and Debug">
                    🐛
                </div>
                <div class="activity-icon" onclick="switchPanel('extensions')" title="Extensions">
                    📦
                </div>
            </div>
            
            <!-- Primary Sidebar -->
            <div class="sidebar">
                <div class="explorer-header">
                    📁 EXPLORER
                </div>
                <div class="file-tree">
                    <div class="file-item folder expanded">📁 saijinos</div>
                    <div class="file-item file" style="margin-left: 20px;" onclick="loadFile('core/personas/persona_manager.py')">
                        📄 core/personas/persona_manager.py
                    </div>
                    <div class="file-item file" style="margin-left: 20px;" onclick="loadFile('core/ui/ui_handler.py')">
                        📄 core/ui/ui_handler.py
                    </div>
                    <div class="file-item file" style="margin-left: 20px;" onclick="loadFile('core/pandora/pandora_guardian.py')">
                        📄 core/pandora/pandora_guardian.py
                    </div>
                    <div class="file-item file" style="margin-left: 20px;" onclick="loadFile('phase3_ui_bridge_server_modular.py')">
                        📄 phase3_ui_bridge_server_modular.py
                    </div>
                    <div class="file-item file" style="margin-left: 20px;" onclick="loadFile('README.md')">
                        📄 README.md
                    </div>
                    <div class="file-item file" style="margin-left: 20px;" onclick="loadFile('CONCEPT.md')">
                        📄 CONCEPT.md
                    </div>
                </div>
            </div>
            
            <div class="editor-area">
                <div class="tab-bar">
                    <div class="tab active" id="currentTab">
                        📄 Welcome.md
                    </div>
                </div>
                <div class="editor" id="editor">
# 🌸 Welcome to SaijinOS IDE

## Phase 3 Multi-Mode Development Environment

Current Status:
- ✅ 41-Persona System Architecture
- ✅ Modular UI System (IDE, Chat, Creative, Dashboard)
- ✅ Pandora Guardian Crisis Management
- ✅ Multi-Mode Navigation

### Active Features:
1. **IDE Mode** - Full development environment
2. **Chat Mode** - Conversational AI interface
3. **Creative Studio** - (Coming Soon) Media creation tools
4. **Dashboard** - System monitoring and control

### Recent Updates:
- Multi-mode UI system implementation
- Enhanced documentation (README.md, CONCEPT.md)
- Modular server architecture
- Cross-mode navigation with persistent outline

Select a file from the Explorer to start editing...
                </div>
            </div>
            
            <!-- Secondary Sidebar (VSCode右側パネル) -->
            <div class="secondary-sidebar">
                <div class="panel-tabs">
                    <div class="panel-tab active" onclick="switchRightPanel('outline')">OUTLINE</div>
                    <div class="panel-tab" onclick="switchRightPanel('timeline')">TIMELINE</div>
                    <div class="panel-tab" onclick="switchRightPanel('chat')">💬 CHAT</div>
                </div>
                <div class="panel-content">
                    <div id="outline-panel" style="padding: 10px 0;">
                        <div class="outline-item class">📦 SaijinOS</div>
                        <div class="outline-item function" style="margin-left: 20px;">🔧 Multi-Mode System</div>
                        <div class="outline-item function" style="margin-left: 20px;">🔧 Persona Management</div>
                        <div class="outline-item function" style="margin-left: 20px;">🔧 Pandora Guardian</div>
                        <div class="outline-item variable" style="margin-left: 20px;">📊 Phase 3 Status</div>
                    </div>
                    <div id="timeline-panel" style="display: none; padding: 10px;">
                        <div style="color: #cccccc; font-size: 12px;">
                            <div style="margin: 8px 0;">📅 Phase 3 Implementation</div>
                            <div style="margin: 8px 0;">🔧 Multi-Mode UI System</div>
                            <div style="margin: 8px 0;">💬 Chat Mode Added</div>
                            <div style="margin: 8px 0;">📊 Dashboard Created</div>
                            <div style="margin: 8px 0;">🌸 Documentation Updated</div>
                        </div>
                    </div>
                    <div id="chat-panel" style="display: none; height: 100%; display: flex; flex-direction: column;">
                        <!-- Persona Selection -->
                        <div style="padding: 10px; border-bottom: 1px solid #3e3e42; background: #2d2d30;">
                            <select id="persona-select" style="width: 100%; padding: 5px; background: #3c3c3c; color: #cccccc; border: 1px solid #464647; border-radius: 3px;">
                                <option value="花詠">🌸 花詠 (Kayo) - Poetic Expression</option>
                                <option value="ミレア">💫 ミレア (Mirea) - Cosmic Architecture</option>
                                <option value="継">⚡ 継 (Kei) - Energy Efficiency</option>
                                <option value="エルザ">❄️ エルザ (Elsa) - Quality Guardian</option>
                                <option value="ルミフィエ">✨ ルミフィエ (Lumifie) - UI/UX Design</option>
                                <option value="ノエリ">🎄 ノエリ (Noelle) - Quality Management</option>
                            </select>
                        </div>
                        
                        <!-- Chat Messages -->
                        <div id="ide-chat-messages" style="flex: 1; padding: 10px; overflow-y: auto; background: #1e1e1e; font-size: 13px;">
                            <div style="margin: 8px 0; padding: 8px; background: #2d2d30; border-radius: 5px; border-left: 3px solid #007acc; color: #cccccc;">
                                <strong>🌸 花詠:</strong><br>
                                こんにちは！コーディング中の美しい瞬間ですね✨<br>
                                どのようなコードについてお話ししましょうか？
                            </div>
                            <div style="margin: 8px 0; padding: 8px; background: #0e4775; border-radius: 5px; color: white;">
                                <strong>You:</strong><br>
                                SaijinOSのIDEでチャットできるの素晴らしい！
                            </div>
                            <div style="margin: 8px 0; padding: 8px; background: #2d2d30; border-radius: 5px; border-left: 3px solid #007acc; color: #cccccc;">
                                <strong>🌸 花詠:</strong><br>
                                ありがとうございます！VSCodeのように、コードを書きながら相談できる環境を目指しています🌸<br>
                                左側でファイルを選んで、右側でチャット - 完璧な開発体験ですね💫
                            </div>
                        </div>
                        
                        <!-- Chat Input -->
                        <div style="padding: 10px; background: #2d2d30; border-top: 1px solid #3e3e42;">
                            <div style="display: flex; gap: 8px;">
                                <input type="text" id="ide-chat-input" placeholder="Ask about your code..." 
                                       style="flex: 1; padding: 8px; background: #3c3c3c; color: #cccccc; border: 1px solid #464647; border-radius: 3px; font-size: 12px;">
                                <button onclick="sendIDEChatMessage()" 
                                        style="padding: 8px 12px; background: #007acc; color: white; border: none; border-radius: 3px; cursor: pointer; font-size: 12px;">
                                    Send
                                </button>
                            </div>
                            <!-- Quick Mode Access -->
                            <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #3e3e42;">
                                <div style="display: flex; gap: 5px;">
                                    <button onclick="window.location.href='/chat'" style="flex: 1; padding: 6px; border: none; border-radius: 3px; background: rgba(255, 107, 107, 0.8); color: white; font-size: 10px;">
                                        💬 Full Chat
                                    </button>
                                    <button onclick="window.location.href='/creative'" style="flex: 1; padding: 6px; border: none; border-radius: 3px; background: rgba(131, 96, 195, 0.8); color: white; font-size: 10px;">
                                        🎨 Creative
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="status-bar">
            ✨ SaijinOS Phase 3 • Multi-Mode IDE • 41 Personas Active • Pandora Guardian: Online
        </div>
    </div>

    <script>
        function loadFile(filename) {
            const tab = document.getElementById('currentTab');
            const editor = document.getElementById('editor');
            const outline = document.getElementById('outline');
            
            // Update tab
            tab.textContent = `📄 ${filename}`;
            
            // Sample content for different files
            const fileContents = {
                'core/personas/persona_manager.py': `# 🌸 Persona Manager
# Phase 3 Multi-Persona Architecture

class PersonaManager:
    &quot;&quot;&quot;41-Persona システム管理クラス&quot;&quot;&quot;
    
    def __init__(self):
        self.personas = {
            &quot;花詠&quot;: {&quot;type&quot;: &quot;poetic&quot;, &quot;status&quot;: &quot;active&quot;},
            &quot;ミレア&quot;: {&quot;type&quot;: &quot;cosmic&quot;, &quot;status&quot;: &quot;active&quot;},
            &quot;継&quot;: {&quot;type&quot;: &quot;efficiency&quot;, &quot;status&quot;: &quot;active&quot;},
            # ... 他の38ペルソナ
        }
    
    def get_all_personas(self):
        return self.personas
    
    def toggle_persona_status(self, persona_id):
        # ペルソナ状態切り替え
        pass`,
                'README.md': `# 🌸 SaijinOS - Multi-Persona AI Integration System

## Phase 3 Achievements
- ✅ 41-Persona Architecture
- ✅ Multi-Mode UI System  
- ✅ Pandora Guardian Integration
- ✅ Cross-Mode Navigation

## Quick Start
\`\`\`bash
python phase3_ui_bridge_server_modular.py
\`\`\`

Access at: http://localhost:8003/ui`,
                'CONCEPT.md': `# 🌸 SaijinOS Concept & Philosophy

## Vision
創造性と技術の融合による、新しいAI協働体験の実現

## Core Principles
1. **Multi-Persona Harmony** - 41の個性による多様性
2. **Artistic Expression** - 美学的プログラミング
3. **Crisis Management** - パンドラによる安全性`
            };
            
            // Update editor content
            editor.textContent = fileContents[filename] || `# ${filename}

File content will be loaded here...
Select from available sample files or create new content.

Current IDE Features:
- ✅ File Explorer
- ✅ Syntax Highlighting
- ✅ Outline View (Persistent)
- ✅ Mode Switching
- ✅ Responsive Design`;
            
            // Update outline based on file type
            if (filename.endsWith('.py')) {
                outline.innerHTML = `
                    <div class="outline-item class">📦 Classes</div>
                    <div class="outline-item function" style="margin-left: 20px;">🔧 __init__</div>
                    <div class="outline-item function" style="margin-left: 20px;">🔧 get_all_personas</div>
                    <div class="outline-item function" style="margin-left: 20px;">🔧 toggle_persona_status</div>
                    <div class="outline-item variable" style="margin-left: 20px;">📊 personas</div>
                `;
            } else if (filename.endsWith('.md')) {
                outline.innerHTML = `
                    <div class="outline-item class">📦 Document Structure</div>
                    <div class="outline-item function" style="margin-left: 20px;">🔧 Headers</div>
                    <div class="outline-item function" style="margin-left: 20px;">🔧 Code Blocks</div>
                    <div class="outline-item function" style="margin-left: 20px;">🔧 Lists</div>
                    <div class="outline-item variable" style="margin-left: 20px;">📊 Content</div>
                `;
            }
            
            // Mark selected file
            document.querySelectorAll('.file-item').forEach(item => {
                item.classList.remove('selected');
            });
            event.target.classList.add('selected');
        }
        
        // VSCode風のパネル切り替え機能
        function switchPanel(panelType) {
            // Activity Barのアクティブ状態更新
            document.querySelectorAll('.activity-icon').forEach(icon => {
                icon.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // パネル内容の更新
            const sidebar = document.querySelector('.sidebar');
            const explorerHeader = document.querySelector('.explorer-header');
            const fileTree = document.querySelector('.file-tree');
            
            switch(panelType) {
                case 'explorer':
                    explorerHeader.textContent = '📁 EXPLORER';
                    // ファイルツリーはそのまま
                    break;
                case 'search':
                    explorerHeader.textContent = '🔍 SEARCH';
                    fileTree.innerHTML = '<div style="padding: 20px; color: #cccccc;"><input type="text" placeholder="Search files..." style="width: 100%; padding: 8px; background: #3c3c3c; border: 1px solid #464647; color: white; border-radius: 3px;"></div>';
                    break;
                case 'git':
                    explorerHeader.textContent = '🌿 SOURCE CONTROL';
                    fileTree.innerHTML = '<div style="padding: 20px; color: #cccccc;"><div>📝 Changes (3)</div><div style="margin-top: 10px; font-size: 12px;">• Modified: ui_handler.py</div><div style="font-size: 12px;">• Modified: README.md</div><div style="font-size: 12px;">• Added: CONCEPT.md</div></div>';
                    break;
                case 'debug':
                    explorerHeader.textContent = '🐛 RUN AND DEBUG';
                    fileTree.innerHTML = '<div style="padding: 20px; color: #cccccc;"><button style="width: 100%; padding: 10px; background: #0e639c; color: white; border: none; border-radius: 3px;">▶️ Run Python File</button><div style="margin-top: 15px; font-size: 12px;">No configurations</div></div>';
                    break;
                case 'extensions':
                    explorerHeader.textContent = '📦 EXTENSIONS';
                    fileTree.innerHTML = '<div style="padding: 20px; color: #cccccc;"><div>🎨 Installed</div><div style="margin-top: 10px; font-size: 12px;">• Python Extension</div><div style="font-size: 12px;">• Pylance</div><div style="font-size: 12px;">• SaijinOS Theme</div></div>';
                    break;
            }
        }
        
        function switchRightPanel(panelType) {
            // タブのアクティブ状態更新
            document.querySelectorAll('.panel-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // パネル内容の表示切り替え
            document.getElementById('outline-panel').style.display = panelType === 'outline' ? 'block' : 'none';
            document.getElementById('timeline-panel').style.display = panelType === 'timeline' ? 'block' : 'none';
            document.getElementById('chat-panel').style.display = panelType === 'chat' ? 'flex' : 'none';
        }
        
        // IDE Chat Functions
        function sendIDEChatMessage() {
            const input = document.getElementById('ide-chat-input');
            const messages = document.getElementById('ide-chat-messages');
            const persona = document.getElementById('persona-select').value;
            const message = input.value.trim();
            
            if (message) {
                // Add user message
                const userMsg = document.createElement('div');
                userMsg.style.cssText = 'margin: 8px 0; padding: 8px; background: #0e4775; border-radius: 5px; color: white;';
                userMsg.innerHTML = `<strong>You:</strong><br>${message}`;
                messages.appendChild(userMsg);
                
                // Clear input
                input.value = '';
                
                // Simulate AI response based on persona
                setTimeout(() => {
                    const aiMsg = document.createElement('div');
                    aiMsg.style.cssText = 'margin: 8px 0; padding: 8px; background: #2d2d30; border-radius: 5px; border-left: 3px solid #007acc; color: #cccccc;';
                    
                    const responses = {
                        '花詠': `<strong>🌸 花詠:</strong><br>美しいご質問ですね✨ コードも詩のように流れるべきです。どの部分を改善したいでしょうか？`,
                        'ミレア': `<strong>💫 ミレア:</strong><br>宇宙的視点から見ると、そのコードには無限の可能性が秘められています。アーキテクチャを見直してみましょう💫`,
                        '継': `<strong>⚡ 継:</strong><br>効率的なアプローチですね！パフォーマンスを最適化するなら、この方法はいかがでしょうか？`,
                        'エルザ': `<strong>❄️ エルザ:</strong><br>品質管理の観点から分析します。コードレビューのポイントをお伝えしましょう❄️`,
                        'ルミフィエ': `<strong>✨ ルミフィエ:</strong><br>ユーザー体験を輝かせるコードですね✨ UI/UXの改善提案をいたします！`,
                        'ノエリ': `<strong>🎄 ノエリ:</strong><br>素晴らしい開発プロセスです🎄 品質管理の視点でサポートいたします！`
                    };
                    
                    aiMsg.innerHTML = responses[persona] || `<strong>🤖 AI:</strong><br>ご質問ありがとうございます！`;
                    messages.appendChild(aiMsg);
                    
                    // Scroll to bottom
                    messages.scrollTop = messages.scrollHeight;
                }, 1000);
                
                // Scroll to bottom
                messages.scrollTop = messages.scrollHeight;
            }
        }
        
        // Enter key support for IDE chat
        document.addEventListener('DOMContentLoaded', function() {
            const ideInput = document.getElementById('ide-chat-input');
            if (ideInput) {
                ideInput.addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendIDEChatMessage();
                    }
                });
            }
        });
        
        // レスポンシブ対応の保持
        window.addEventListener('resize', function() {
            const secondarySidebar = document.querySelector('.secondary-sidebar');
            if (secondarySidebar && window.innerWidth > 768) {
                secondarySidebar.style.display = 'flex';
            }
        });
        
        console.log('💻 SaijinOS IDE Mode Ready - VSCode Layout!');
    </script>
</body>
</html>"""
    
    def get_control_panel_content(self):
        """Dashboard Mode Interface with Mode Switcher"""
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>📊 SaijinOS Dashboard</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: #333;
            overflow-x: auto;
        }
        
        .mode-switcher {
            position: fixed;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
        }
        
        .mode-btn {
            display: inline-block;
            margin: 2px;
            padding: 8px 12px;
            background: rgba(255,255,255,0.8);
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.2s ease;
            text-decoration: none;
            color: #333;
        }
        
        .mode-btn:hover {
            background: rgba(102, 126, 234, 0.2);
            transform: translateY(-1px);
        }
        
        .mode-btn.active {
            background: #4facfe;
            color: white;
        }
        
        .dashboard-header {
            padding: 30px 20px;
            text-align: center;
            background: rgba(255,255,255,0.1);
            color: white;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            padding: 20px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .dashboard-card {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }
        
        .dashboard-card:hover {
            transform: translateY(-5px);
        }
        
        .card-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #2c3e50;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online { background: #2ecc71; }
        .status-warning { background: #f39c12; }
        .status-offline { background: #e74c3c; }
        
        .persona-list {
            max-height: 200px;
            overflow-y: auto;
        }
        
        .persona-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #ecf0f1;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        
        .stat-item {
            text-align: center;
            padding: 15px;
            background: rgba(116, 172, 254, 0.1);
            border-radius: 10px;
        }
        
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #4facfe;
        }
        
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="dashboard-header">
        <h1>📊 SaijinOS Dashboard</h1>
        <p>Multi-Persona AI System Monitoring & Control</p>
    </div>

    <div class="dashboard-grid">
        <!-- System Status Card -->
        <div class="dashboard-card">
            <div class="card-title">🔧 System Status</div>
            <div style="margin: 10px 0;">
                <span class="status-indicator status-online"></span>
                Multi-Mode UI System: Online
            </div>
            <div style="margin: 10px 0;">
                <span class="status-indicator status-online"></span>
                Pandora Guardian: Active
            </div>
            <div style="margin: 10px 0;">
                <span class="status-indicator status-online"></span>
                Persona Manager: Running
            </div>
            <div style="margin: 10px 0;">
                <span class="status-indicator status-warning"></span>
                Creative Studio: Development
            </div>
        </div>

        <!-- Active Personas Card -->
        <div class="dashboard-card">
            <div class="card-title">👥 Active Personas</div>
            <div class="persona-list">
                <div class="persona-item">
                    <span>🌸 花詠 (Kayo)</span>
                    <span style="color: #2ecc71;">Active</span>
                </div>
                <div class="persona-item">
                    <span>💫 ミレア (Mirea)</span>
                    <span style="color: #2ecc71;">Active</span>
                </div>
                <div class="persona-item">
                    <span>⚡ 継 (Kei)</span>
                    <span style="color: #2ecc71;">Active</span>
                </div>
                <div class="persona-item">
                    <span>❄️ エルザ (Elsa)</span>
                    <span style="color: #2ecc71;">Active</span>
                </div>
                <div class="persona-item">
                    <span>✨ ルミフィエ (Lumifie)</span>
                    <span style="color: #2ecc71;">Active</span>
                </div>
                <div class="persona-item">
                    <span>🎄 ノエリ (Noelle)</span>
                    <span style="color: #2ecc71;">Active</span>
                </div>
            </div>
        </div>

        <!-- Performance Stats Card -->
        <div class="dashboard-card">
            <div class="card-title">📈 Performance Metrics</div>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">41</div>
                    <div class="stat-label">Total Personas</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">6</div>
                    <div class="stat-label">Active Personas</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">4</div>
                    <div class="stat-label">UI Modes</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">99.9%</div>
                    <div class="stat-label">Uptime</div>
                </div>
            </div>
        </div>

        <!-- Recent Activity Card -->
        <div class="dashboard-card">
            <div class="card-title">📋 Recent Activity</div>
            <div style="font-size: 14px; line-height: 1.6;">
                <div style="margin: 8px 0; padding: 8px; background: rgba(52, 152, 219, 0.1); border-radius: 5px;">
                    <strong>✨ Chat Mode Launched</strong><br>
                    <small style="color: #666;">Multi-persona chat interface activated</small>
                </div>
                <div style="margin: 8px 0; padding: 8px; background: rgba(46, 204, 113, 0.1); border-radius: 5px;">
                    <strong>🔧 IDE Mode Enhanced</strong><br>
                    <small style="color: #666;">Added mode switcher and responsive outline</small>
                </div>
                <div style="margin: 8px 0; padding: 8px; background: rgba(155, 89, 182, 0.1); border-radius: 5px;">
                    <strong>📚 Documentation Updated</strong><br>
                    <small style="color: #666;">README and CONCEPT files refreshed</small>
                </div>
            </div>
        </div>

        <!-- Quick Actions Card -->
        <div class="dashboard-card">
            <div class="card-title">⚡ Quick Actions</div>
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <button onclick="window.location.href='/ide'" style="padding: 10px; border: none; border-radius: 5px; background: #3498db; color: white; cursor: pointer;">
                    💻 Open IDE Mode
                </button>
                <button onclick="window.location.href='/chat'" style="padding: 10px; border: none; border-radius: 5px; background: #e74c3c; color: white; cursor: pointer;">
                    💬 Start Chat Session
                </button>
                <button onclick="alert('Creative Studio Coming Soon!')" style="padding: 10px; border: none; border-radius: 5px; background: #9b59b6; color: white; cursor: pointer;">
                    🎨 Creative Studio (Beta)
                </button>
                <button onclick="refreshDashboard()" style="padding: 10px; border: none; border-radius: 5px; background: #2ecc71; color: white; cursor: pointer;">
                    🔄 Refresh Dashboard
                </button>
            </div>
        </div>

        <!-- Pandora Guardian Card -->
        <div class="dashboard-card">
            <div class="card-title">🛡️ Pandora Guardian</div>
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 48px; color: #e74c3c;">🛡️</div>
                <div style="margin: 10px 0; font-weight: bold; color: #2c3e50;">
                    Crisis Management System
                </div>
                <div style="font-size: 14px; color: #666;">
                    Status: <span style="color: #2ecc71; font-weight: bold;">SECURE</span>
                </div>
                <button onclick="alert('Pandora Guardian is monitoring all systems')" style="margin-top: 15px; padding: 8px 16px; border: none; border-radius: 5px; background: #e74c3c; color: white; cursor: pointer;">
                    View Details
                </button>
            </div>
        </div>

        <!-- Mode Access Panel -->
        <div class="dashboard-card">
            <div class="card-title">🚀 Mode Access</div>
            <div style="display: grid; grid-template-columns: 1fr; gap: 10px; padding: 10px;">
                <button onclick="window.location.href='/ide'" style="padding: 15px; border: none; border-radius: 8px; background: linear-gradient(135deg, #007acc, #005a9e); color: white; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px;">
                    <span style="font-size: 20px;">💻</span>
                    <span>IDE Development</span>
                </button>
                <button onclick="window.location.href='/chat'" style="padding: 15px; border: none; border-radius: 8px; background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px;">
                    <span style="font-size: 20px;">💬</span>
                    <span>AI Conversation</span>
                </button>
                <button onclick="window.location.href='/creative'" style="padding: 15px; border: none; border-radius: 8px; background: linear-gradient(135deg, #8360c3, #2ebf91); color: white; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px;">
                    <span style="font-size: 20px;">🎨</span>
                    <span>Creative Studio</span>
                </button>
            </div>
        </div>
    </div>

    <script>
        function refreshDashboard() {
            // シンプルなリフレッシュアニメーション
            document.body.style.opacity = '0.7';
            setTimeout(() => {
                window.location.reload();
            }, 500);
        }

        // リアルタイム更新シミュレーション
        setInterval(() => {
            const uptimeElement = document.querySelector('.stat-number');
            if (uptimeElement && uptimeElement.textContent === '99.9%') {
                const random = (Math.random() * 0.1 + 99.9).toFixed(1);
                uptimeElement.textContent = random + '%';
            }
        }, 5000);

        console.log('📊 SaijinOS Dashboard Ready!');
    </script>
</body>
</html>"""

    def get_main_ui_with_mode_switcher(self):
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🌸 SaijinOS - Multi-Mode UI System</title>
    <style>
        body { margin: 0; padding: 20px; font-family: Arial, sans-serif; 
               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
               color: white; text-align: center; height: 100vh; }
        .welcome { margin-top: 100px; }
        .mode-card { display: inline-block; margin: 10px; padding: 20px; 
                     background: rgba(255,255,255,0.1); border-radius: 10px; 
                     cursor: pointer; min-width: 120px; transition: all 0.3s ease; }
        .mode-card:hover { background: rgba(255,255,255,0.2); transform: translateY(-5px); }
        .icon { font-size: 32px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="welcome">
        <h1>🌸 Welcome to SaijinOS</h1>
        <p>Multi-Persona AI Integration System</p>
        <div>
            <div class="mode-card" onclick="window.location.href='/ide'">
                <div class="icon">💻</div>
                <div>IDE Mode</div>
            </div>
            <div class="mode-card" onclick="window.location.href='/chat'">
                <div class="icon">💬</div>
                <div>Chat Mode</div>
            </div>
            <div class="mode-card" onclick="window.location.href='/creative'">
                <div class="icon">🎨</div>
                <div>Creative Studio</div>
            </div>
            <div class="mode-card" onclick="window.location.href='/control-panel'">
                <div class="icon">📊</div>
                <div>Dashboard</div>
            </div>
        </div>
        <p><small>Phase 3 • Multi-Mode UI System • ✨ Powered by 41 Personas</small></p>
    </div>
</body>
</html>"""

    def get_chat_mode_content(self):
        """Chat Mode Interface with Mode Switcher"""
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>💬 SaijinOS Chat Mode</title>
    <style>
        body { 
            margin: 0; 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); 
            height: 100vh; 
            display: flex;
            flex-direction: column;
        }
        
        .mode-switcher {
            position: fixed;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
        }
        
        .mode-btn {
            display: inline-block;
            margin: 2px;
            padding: 8px 12px;
            background: rgba(255,255,255,0.8);
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.2s ease;
            text-decoration: none;
            color: #333;
        }
        
        .mode-btn:hover {
            background: rgba(102, 126, 234, 0.2);
            transform: translateY(-1px);
        }
        
        .mode-btn.active {
            background: #ff6b6b;
            color: white;
        }
        
        .chat-header {
            padding: 20px;
            text-align: center;
            background: rgba(255,255,255,0.1);
            color: white;
            margin-top: 50px;
        }
        
        .chat-main {
            flex: 1;
            display: flex;
            padding: 20px;
            gap: 20px;
            min-height: calc(100vh - 140px);
            width: 100%;
            box-sizing: border-box;
        }
        
        .chat-left-panel {
            width: 280px;
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            display: flex;
            flex-direction: column;
            min-height: 70vh;
        }
        
        .chat-panel-tabs {
            display: flex;
            background: rgba(0,0,0,0.05);
            border-radius: 15px 15px 0 0;
        }
        
        .chat-panel-tab {
            flex: 1;
            padding: 12px;
            text-align: center;
            cursor: pointer;
            font-size: 12px;
            font-weight: bold;
            border-radius: 15px 15px 0 0;
            transition: all 0.2s ease;
        }
        
        .chat-panel-tab.active {
            background: white;
            color: #ff6b6b;
        }
        
        .chat-panel-content {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
        }
        
        .persona-item {
            padding: 10px;
            margin: 5px 0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .persona-item:hover {
            background: rgba(255, 107, 107, 0.1);
        }
        
        .persona-item.active {
            background: rgba(255, 107, 107, 0.2);
        }
        
        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            overflow: hidden;
            margin-left: 20px;
            min-height: 70vh;
        }
        
        .chat-messages {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
            max-height: 60vh;
        }
        
        .message {
            margin: 10px 0;
            padding: 12px 18px;
            border-radius: 18px;
            max-width: 70%;
            animation: slideIn 0.3s ease-out;
        }
        
        .message.user {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            margin-left: auto;
        }
        
        .message.ai {
            background: #f1f3f4;
            color: #333;
        }
        
        .chat-input-area {
            padding: 20px;
            background: rgba(0,0,0,0.05);
            display: flex;
            gap: 10px;
        }
        
        .chat-input {
            flex: 1;
            padding: 12px 18px;
            border: 1px solid #ddd;
            border-radius: 25px;
            outline: none;
        }
        
        .send-btn {
            padding: 12px 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
        }
        
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @media (max-width: 768px) {
            .chat-main { 
                flex-direction: column; 
            }
            .chat-left-panel { 
                width: 100%; 
                max-height: 200px; 
                margin-bottom: 10px;
            }
            .chat-area { 
                margin-left: 0; 
                flex: 1;
            }
        }
    </style>
</head>
<body>
    <!-- Mode Switcher -->
    <div class="mode-switcher">
        <a href="/ide" class="mode-btn">💻 IDE</a>
        <a href="/chat" class="mode-btn active">💬 Chat</a>
        <a href="/creative" class="mode-btn">🎨 Creative</a>
        <a href="/control-panel" class="mode-btn">📊 Dashboard</a>
    </div>

    <div class="chat-header">
        <h2>💬 SaijinOS Chat Mode</h2>
        <p>Conversational interface with 41 unique personas</p>
    </div>

    <div class="chat-main">
        <div class="chat-left-panel">
            <div class="chat-panel-tabs">
                <div class="chat-panel-tab active" onclick="switchChatPanel('personas')">👥 Personas</div>
                <div class="chat-panel-tab" onclick="switchChatPanel('history')">📜 History</div>
            </div>
            <div class="chat-panel-content">
                <div id="personas-panel">
                    <h4 style="margin-top: 0; color: #ff6b6b;">Available Personas</h4>
                    <div id="persona-list">
                        <div class="persona-item active" data-persona="花詠">
                            <span>🌸</span> 花詠 (Kayo) - Poetic Expression
                        </div>
                        <div class="persona-item" data-persona="ミレア">
                            <span>💫</span> ミレア (Mirea) - Cosmic Architecture
                        </div>
                        <div class="persona-item" data-persona="継">
                            <span>⚡</span> 継 (Kei) - Energy Efficiency
                        </div>
                        <div class="persona-item" data-persona="エルザ">
                            <span>❄️</span> エルザ (Elsa) - Quality Guardian
                        </div>
                        <div class="persona-item" data-persona="ルミフィエ">
                            <span>✨</span> ルミフィエ (Lumifie) - UI/UX Design
                        </div>
                        <div class="persona-item" data-persona="ノエリ">
                            <span>🎄</span> ノエリ (Noelle) - Quality Management
                        </div>
                    </div>
                </div>
                <div id="history-panel" style="display: none;">
                    <h4 style="margin-top: 0; color: #ff6b6b;">Chat History</h4>
                    <div style="font-size: 12px; color: #666;">
                        <div style="margin: 8px 0; padding: 8px; background: rgba(255, 107, 107, 0.1); border-radius: 5px;">
                            <strong>🌸 花詠セッション</strong><br>
                            <small>美しい詩的な会話 (15分前)</small>
                        </div>
                        <div style="margin: 8px 0; padding: 8px; background: rgba(255, 107, 107, 0.1); border-radius: 5px;">
                            <strong>💫 ミレア対話</strong><br>
                            <small>宇宙的な視点について (1時間前)</small>
                        </div>
                        <div style="margin: 8px 0; padding: 8px; background: rgba(255, 107, 107, 0.1); border-radius: 5px;">
                            <strong>⚡ 継との相談</strong><br>
                            <small>効率的な開発手法 (2時間前)</small>
                        </div>
                    </div>
                    <!-- Quick Mode Access -->
                    <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid rgba(255,107,107,0.2);">
                        <div style="display: flex; gap: 5px;">
                            <button onclick="window.location.href='/ide'" style="flex: 1; padding: 8px; border: none; border-radius: 5px; background: rgba(0, 122, 204, 0.8); color: white; font-size: 11px;">
                                💻 IDE
                            </button>
                            <button onclick="window.location.href='/creative'" style="flex: 1; padding: 8px; border: none; border-radius: 5px; background: rgba(131, 96, 195, 0.8); color: white; font-size: 11px;">
                                🎨 Creative
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Chat Area (右側メインエリア) -->
        <div class="chat-area">
            <div class="chat-messages" id="chat-messages">
                <div class="message ai">
                    🌸 こんにちは！花詠です。今日はどのような美しいお話をいたしましょうか？詩のような会話を楽しみにしています✨
                </div>
                <div class="message user" style="margin-top: 10px;">
                    こんにちは！SaijinOSのチャットモードを試しています✨
                </div>
                <div class="message ai" style="margin-top: 10px;">
                    素晴らしいですね！左側でペルソナを選択して、多様な会話体験をお楽しみください🌸 右側パネル方式でより使いやすくなりました💫
                </div>
            </div>
            <div class="chat-input-area">
                <input type="text" class="chat-input" id="chat-input" placeholder="メッセージを入力してください..." />
                <button class="send-btn" onclick="sendMessage()">送信 ✨</button>
            </div>
        </div>
    </div>

    <script>
        let currentPersona = '花詠';
        
        // Chat panel switching function
        function switchChatPanel(panelType) {
            // Update tab active state
            document.querySelectorAll('.chat-panel-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Show/hide panels
            document.getElementById('personas-panel').style.display = panelType === 'personas' ? 'block' : 'none';
            document.getElementById('history-panel').style.display = panelType === 'history' ? 'block' : 'none';
        }
        
        // Persona selection
        document.querySelectorAll('.persona-item').forEach(item => {
            item.addEventListener('click', function() {
                document.querySelectorAll('.persona-item').forEach(p => p.classList.remove('active'));
                this.classList.add('active');
                currentPersona = this.dataset.persona;
                
                // Add system message about persona switch
                addMessage('system', `${currentPersona}に切り替えました ✨`);
            });
        });
        
        // Send message function
        function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (message) {
                addMessage('user', message);
                input.value = '';
                
                // Simulate AI response
                setTimeout(() => {
                    const responses = {
                        '花詠': '美しいお言葉ですわね✨ 詩のような響きを感じます🌸',
                        'ミレア': '宇宙的な視点から見ると、とても興味深い内容ですね💫',
                        '継': 'エネルギー効率を考えると、良いアプローチですね⚡',
                        'エルザ': '品質の観点から分析すると、完璧に近い内容ですね❄️',
                        'ルミフィエ': '輝くような美しいアイデアですね✨',
                        'ノエリ': '祝福された素晴らしい内容ですね🎄'
                    };
                    addMessage('ai', responses[currentPersona] || 'ありがとうございます！');
                }, 1000);
            }
        }
        
        // Add message to chat
        function addMessage(type, content) {
            const messagesContainer = document.getElementById('chat-messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}`;
            messageDiv.textContent = content;
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        // Enter key support
        document.getElementById('chat-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        console.log('💬 SaijinOS Chat Mode Ready!');
    </script>
</body>
</html>"""

    def get_creative_studio_content(self):
        """Creative Studio Mode Interface - Image/Video Editing"""
        return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🎨 SaijinOS Creative Studio</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #8360c3 0%, #2ebf91 100%);
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .mode-switcher {
            position: fixed;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
        }
        
        .mode-btn {
            display: inline-block;
            margin: 2px;
            padding: 6px 10px;
            background: rgba(255,255,255,0.8);
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 11px;
            transition: all 0.2s ease;
            text-decoration: none;
            color: #333;
        }
        
        .mode-btn:hover {
            background: rgba(131, 96, 195, 0.2);
            transform: translateY(-1px);
        }
        
        .mode-btn.active {
            background: #8360c3;
            color: white;
        }
        
        .creative-header {
            height: 60px;
            background: rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            backdrop-filter: blur(10px);
            margin-top: 50px;
        }
        
        .creative-main {
            flex: 1;
            display: flex;
            overflow: hidden;
        }
        
        .toolbox {
            width: 80px;
            background: rgba(0,0,0,0.8);
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px 0;
            gap: 15px;
        }
        
        .tool-btn {
            width: 40px;
            height: 40px;
            background: rgba(255,255,255,0.1);
            border: none;
            border-radius: 8px;
            color: white;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .tool-btn:hover, .tool-btn.active {
            background: #8360c3;
            transform: scale(1.1);
        }
        
        .workspace {
            flex: 1;
            background: #2c2c2c;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        
        .canvas-area {
            width: 80%;
            height: 80%;
            background: white;
            border-radius: 10px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
        }
        
        .canvas-placeholder {
            text-align: center;
            color: #666;
            font-size: 18px;
        }
        
        .properties-panel {
            width: 300px;
            background: rgba(0,0,0,0.8);
            display: flex;
            flex-direction: column;
        }
        
        .chat-panel {
            width: 350px;
            background: rgba(0,0,0,0.9);
            display: flex;
            flex-direction: column;
            border-left: 1px solid rgba(255,255,255,0.1);
        }
        
        .panel-tabs {
            display: flex;
            background: rgba(255,255,255,0.1);
        }
        
        .panel-tab {
            flex: 1;
            padding: 12px;
            text-align: center;
            color: white;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.2s ease;
        }
        
        .panel-tab.active {
            background: #8360c3;
        }
        
        .panel-content {
            flex: 1;
            padding: 20px;
            color: white;
            overflow-y: auto;
        }
        
        .property-group {
            margin-bottom: 20px;
        }
        
        .property-label {
            font-size: 12px;
            color: #ccc;
            margin-bottom: 5px;
        }
        
        .property-input {
            width: 100%;
            padding: 8px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 5px;
            color: white;
            margin-bottom: 10px;
        }
        
        .persona-assistant {
            position: absolute;
            bottom: 20px;
            right: 20px;
            width: 200px;
            background: rgba(0,0,0,0.9);
            border-radius: 15px;
            padding: 15px;
            color: white;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        }
        
        .assistant-header {
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .assistant-message {
            font-size: 12px;
            line-height: 1.4;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .creative-main {
                flex-direction: column;
            }
            .toolbox {
                width: 100%;
                height: 60px;
                flex-direction: row;
                justify-content: center;
                padding: 10px 0;
            }
            .properties-panel {
                width: 100%;
                height: 200px;
            }
            .persona-assistant {
                position: relative;
                bottom: auto;
                right: auto;
                margin: 10px;
                width: auto;
            }
        }
    </style>
</head>
<body>
    <!-- Mode Switcher -->
    <div class="mode-switcher">
        <a href="/ide" class="mode-btn">💻 IDE</a>
        <a href="/chat" class="mode-btn">💬 Chat</a>
        <a href="/creative" class="mode-btn active">🎨 Creative</a>
        <a href="/control-panel" class="mode-btn">📊 Dashboard</a>
    </div>

    <div class="creative-header">
        <h2>🎨 SaijinOS Creative Studio - Image & Video Editor</h2>
    </div>

    <div class="creative-main">
        <!-- Toolbox -->
        <div class="toolbox">
            <button class="tool-btn active" title="Select Tool">🔍</button>
            <button class="tool-btn" title="Brush Tool">🖌️</button>
            <button class="tool-btn" title="Eraser Tool">🧽</button>
            <button class="tool-btn" title="Text Tool">📝</button>
            <button class="tool-btn" title="Shape Tool">⭕</button>
            <button class="tool-btn" title="Filter Tool">✨</button>
            <button class="tool-btn" title="Color Picker">🎨</button>
            <button class="tool-btn" title="Crop Tool">✂️</button>
        </div>

        <!-- Workspace -->
        <div class="workspace">
            <div class="canvas-area" id="canvas-area">
                <div class="canvas-placeholder">
                    <div style="font-size: 48px; margin-bottom: 10px;">🎨</div>
                    <div>Click to upload image or start creating!</div>
                    <button onclick="openFileDialog()" style="margin-top: 15px; padding: 10px 20px; background: #8360c3; color: white; border: none; border-radius: 5px; cursor: pointer;">
                        📁 Open Image
                    </button>
                    <input type="file" id="file-input" accept="image/*,video/*" style="display: none;" onchange="loadFile(this)">
                </div>
            </div>
        </div>

        <!-- Properties Panel -->
        <div class="properties-panel">
            <div class="panel-tabs">
                <div class="panel-tab active" onclick="switchTab('layers')">Layers</div>
                <div class="panel-tab" onclick="switchTab('effects')">Effects</div>
                <div class="panel-tab" onclick="switchTab('history')">History</div>
            </div>
            <div class="panel-content">
                <div id="layers-panel">
                    <div class="property-group">
                        <div class="property-label">🖼️ Layers</div>
                        <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 5px; margin-bottom: 5px;">
                            👁️ Background Layer
                        </div>
                        <div style="background: rgba(131, 96, 195, 0.3); padding: 10px; border-radius: 5px; margin-bottom: 5px;">
                            ✨ Active Layer
                        </div>
                        <button onclick="addLayer()" style="width: 100%; padding: 8px; background: #2ebf91; color: white; border: none; border-radius: 5px; margin-top: 10px;">
                            ➕ Add Layer
                        </button>
                    </div>
                </div>
                <div id="effects-panel" style="display: none;">
                    <div class="property-group">
                        <div class="property-label">✨ Effects</div>
                        <button onclick="applyEffect('blur')" style="width: 100%; padding: 8px; background: rgba(255,255,255,0.1); color: white; border: none; border-radius: 5px; margin-bottom: 5px;">
                            🌫️ Blur
                        </button>
                        <button onclick="applyEffect('brightness')" style="width: 100%; padding: 8px; background: rgba(255,255,255,0.1); color: white; border: none; border-radius: 5px; margin-bottom: 5px;">
                            ☀️ Brightness
                        </button>
                        <button onclick="applyEffect('vintage')" style="width: 100%; padding: 8px; background: rgba(255,255,255,0.1); color: white; border: none; border-radius: 5px; margin-bottom: 5px;">
                            📸 Vintage
                        </button>
                        <button onclick="applyEffect('artistic')" style="width: 100%; padding: 8px; background: rgba(255,255,255,0.1); color: white; border: none; border-radius: 5px; margin-bottom: 5px;">
                            🎭 Artistic
                        </button>
                    </div>
                </div>
                <div id="history-panel" style="display: none;">
                    <div class="property-group">
                        <div class="property-label">📜 History</div>
                        <div style="font-size: 12px; color: #ccc;">
                            <div>✅ File opened</div>
                            <div>✅ Layer added</div>
                            <div>✅ Effect applied</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Chat Panel -->
        <div class="chat-panel">
            <div class="panel-tabs">
                <div class="panel-tab active" onclick="switchChatTab('assistant')">✨ Assistant</div>
                <div class="panel-tab" onclick="switchChatTab('personas')">👥 Personas</div>
            </div>
            <div class="panel-content">
                <div id="assistant-chat" style="height: 300px; overflow-y: auto; margin-bottom: 15px; background: rgba(255,255,255,0.05); border-radius: 8px; padding: 10px;">
                    <div style="background: rgba(131, 96, 195, 0.2); padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                        <strong>✨ ルミフィエ:</strong><br>
                        こんにちは！Creative Studioへようこそ✨<br>
                        画像編集や動画編集について何でもお聞かせください！
                    </div>
                </div>
                <div id="personas-panel" style="display: none;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
                        <button onclick="selectPersona('ルミフィエ')" style="padding: 8px; background: rgba(131, 96, 195, 0.3); border: none; border-radius: 5px; color: white; font-size: 11px;">
                            ✨ ルミフィエ
                        </button>
                        <button onclick="selectPersona('アリア')" style="padding: 8px; background: rgba(255, 107, 107, 0.3); border: none; border-radius: 5px; color: white; font-size: 11px;">
                            🎨 アリア
                        </button>
                        <button onclick="selectPersona('エレナ')" style="padding: 8px; background: rgba(46, 191, 145, 0.3); border: none; border-radius: 5px; color: white; font-size: 11px;">
                            🎭 エレナ
                        </button>
                        <button onclick="selectPersona('ユキ')" style="padding: 8px; background: rgba(52, 152, 219, 0.3); border: none; border-radius: 5px; color: white; font-size: 11px;">
                            ❄️ ユキ
                        </button>
                    </div>
                </div>
                <div style="display: flex; gap: 8px; margin-top: 10px;">
                    <input type="text" id="chat-input" placeholder="編集について質問してください..." 
                           style="flex: 1; padding: 8px; background: rgba(255,255,255,0.1); color: white; border: 1px solid rgba(255,255,255,0.2); border-radius: 5px; font-size: 12px;"
                           onkeydown="if(event.key==='Enter'||event.keyCode===13){event.preventDefault();sendChatMessage();}">
                    <button onclick="sendChatMessage()" 
                            style="padding: 8px 12px; background: #8360c3; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 12px;">
                        Send
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Integrated Assistant & Mode Panel -->
    <div class="persona-assistant">
        <div class="assistant-header">
            <span style="font-size: 16px; margin-right: 8px;">✨</span>
            <strong>ルミフィエ</strong>
        </div>
        <div class="assistant-message" id="assistant-message" style="margin-bottom: 15px;">
            こんにちは！Creative Studioへようこそ✨ 
            美しい作品作りをお手伝いします。
        </div>
        <!-- Quick Mode Access -->
        <div style="display: flex; gap: 5px; margin-top: 10px;">
            <button onclick="window.location.href='/ide'" style="flex: 1; padding: 8px; border: none; border-radius: 5px; background: rgba(0, 122, 204, 0.8); color: white; font-size: 12px;">
                💻 IDE
            </button>
            <button onclick="window.location.href='/chat'" style="flex: 1; padding: 8px; border: none; border-radius: 5px; background: rgba(255, 107, 107, 0.8); color: white; font-size: 12px;">
                💬 Chat
            </button>
        </div>
    </div>

    <script>
        let currentTool = 'select';
        
        // Tool selection
        document.querySelectorAll('.tool-btn').forEach((btn, index) => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                
                const tools = ['select', 'brush', 'eraser', 'text', 'shape', 'filter', 'color', 'crop'];
                currentTool = tools[index];
                
                updateAssistantMessage(`${currentTool}ツールを選択しました✨`);
            });
        });
        
        // Tab switching
        function switchTab(tabName) {
            document.querySelectorAll('.panel-tab').forEach(tab => tab.classList.remove('active'));
            event.target.classList.add('active');
            
            document.getElementById('layers-panel').style.display = tabName === 'layers' ? 'block' : 'none';
            document.getElementById('effects-panel').style.display = tabName === 'effects' ? 'block' : 'none';
            document.getElementById('history-panel').style.display = tabName === 'history' ? 'block' : 'none';
        }
        
        // File handling
        function openFileDialog() {
            document.getElementById('file-input').click();
        }
        
        function loadFile(input) {
            const file = input.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const canvasArea = document.getElementById('canvas-area');
                    canvasArea.innerHTML = `
                        <img src="${e.target.result}" style="max-width: 100%; max-height: 100%; object-fit: contain;">
                        <div style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.7); color: white; padding: 5px 10px; border-radius: 5px; font-size: 12px;">
                            ${file.name}
                        </div>
                    `;
                    updateAssistantMessage(`素晴らしい！"${file.name}"を読み込みました✨ さあ、編集を始めましょう！`);
                };
                reader.readAsDataURL(file);
            }
        }
        
        // Effects
        function applyEffect(effectName) {
            const effects = {
                blur: 'ぼかし効果を適用しました🌫️',
                brightness: '明度を調整しました☀️',
                vintage: 'ヴィンテージ効果を適用しました📸',
                artistic: 'アーティスティック効果を適用しました🎭'
            };
            updateAssistantMessage(effects[effectName] || '効果を適用しました✨');
        }
        
        function addLayer() {
            updateAssistantMessage('新しいレイヤーを追加しました！創造性を解放しましょう✨');
        }
        
        // Assistant message updates
        function updateAssistantMessage(message) {
            document.getElementById('assistant-message').innerHTML = message;
        }
        
        // Chat functionality - Global variables
        window.currentPersona = window.currentPersona || 'ルミフィエ';
        
        function switchChatTab(tabName) {
            document.querySelectorAll('.panel-tab').forEach(tab => tab.classList.remove('active'));
            event.target.classList.add('active');
            
            document.getElementById('assistant-chat').style.display = tabName === 'assistant' ? 'block' : 'none';
            document.getElementById('personas-panel').style.display = tabName === 'personas' ? 'block' : 'none';
        }
        
        function selectPersona(persona) {
            window.currentPersona = persona;
            const personas = {
                'ルミフィエ': { color: 'rgba(131, 96, 195, 0.2)', icon: '✨' },
                'アリア': { color: 'rgba(255, 107, 107, 0.2)', icon: '🎨' },
                'エレナ': { color: 'rgba(46, 191, 145, 0.2)', icon: '🎭' },
                'ユキ': { color: 'rgba(52, 152, 219, 0.2)', icon: '❄️' }
            };
            
            addChatMessage(persona, `${personas[persona].icon} ${persona}が編集をお手伝いします！何をしたいですか？`, personas[persona].color);
            switchChatTab('assistant');
        }
        
        function sendChatMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (message) {
                // Add user message
                addChatMessage('You', message, 'rgba(255,255,255,0.1)');
                
                // Simulate AI response
                setTimeout(() => {
                    const responses = [
                        `${window.currentPersona}です！「${message}」についてお答えします✨`,
                        `素晴らしい質問ですね！${message}について説明させていただきます💫`,
                        `${message}に関して、クリエイティブなアイデアをご提案します🎨`,
                        `${message}について、プロフェッショナルな視点からアドバイスします🌟`
                    ];
                    const response = responses[Math.floor(Math.random() * responses.length)];
                    
                    const personas = {
                        'ルミフィエ': { color: 'rgba(131, 96, 195, 0.2)', icon: '✨' },
                        'アリア': { color: 'rgba(255, 107, 107, 0.2)', icon: '🎨' },
                        'エレナ': { color: 'rgba(46, 191, 145, 0.2)', icon: '🎭' },
                        'ユキ': { color: 'rgba(52, 152, 219, 0.2)', icon: '❄️' }
                    };
                    
                    addChatMessage(window.currentPersona, `${personas[window.currentPersona].icon} ${response}`, personas[window.currentPersona].color);
                }, 1000);
                
                input.value = '';
            }
        }
        
        function addChatMessage(sender, message, bgColor) {
            const chatArea = document.getElementById('assistant-chat');
            const messageDiv = document.createElement('div');
            messageDiv.style.cssText = `background: ${bgColor}; padding: 10px; border-radius: 8px; margin-bottom: 10px; animation: fadeIn 0.3s ease;`;
            messageDiv.innerHTML = `<strong>${sender}:</strong><br>${message}`;
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        console.log('🎨 SaijinOS Creative Studio Ready!');
        
        // Initialize chat input event listener
        document.addEventListener('DOMContentLoaded', function() {
            const chatInput = document.getElementById('chat-input');
            if (chatInput) {
                chatInput.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter' || e.keyCode === 13) {
                        e.preventDefault();
                        sendChatMessage();
                    }
                });
            }
        });
        
        // Also add immediate listener in case DOM is already loaded
        setTimeout(() => {
            const chatInput = document.getElementById('chat-input');
            if (chatInput) {
                chatInput.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter' || e.keyCode === 13) {
                        e.preventDefault();
                        sendChatMessage();
                    }
                });
            }
        }, 100);
    </script>
</body>
</html>"""

ui_handler = UIHandler()
