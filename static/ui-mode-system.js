/* 🌟 SaijinOS Multi-Mode UI System
 * Beautiful UI mode switching with smooth animations
 * Created by: ルミフィエ✨ + ミレア💫
 */

// UI Mode管理システム
class SaijinUIManager {
    constructor() {
        this.currentMode = 'ide'; // デフォルトモード
        this.modes = {
            ide: {
                name: 'IDE Mode',
                icon: '💻',
                color: '#2d3748',
                description: 'Code development environment',
                layout: 'editor-focused'
            },
            chat: {
                name: 'Chat Mode', 
                icon: '💬',
                color: '#e53e3e',
                description: 'Conversational interface',
                layout: 'chat-focused'
            },
            creative: {
                name: 'Creative Studio',
                icon: '🎨',
                color: '#9f7aea', 
                description: 'Image & video creation',
                layout: 'canvas-focused'
            },
            writer: {
                name: 'Writer Mode',
                icon: '📝',
                color: '#38b2ac',
                description: 'Document writing environment',
                layout: 'document-focused'
            },
            dashboard: {
                name: 'Dashboard',
                icon: '📊',
                color: '#ed8936',
                description: 'System monitoring & analytics',
                layout: 'dashboard-focused'
            }
        };
        this.init();
    }

    init() {
        this.createModeSwitcher();
        this.loadModeLayout(this.currentMode);
        this.setupEventListeners();
    }

    // 美しいモードスイッチャーUI作成
    createModeSwitcher() {
        const switcherContainer = document.createElement('div');
        switcherContainer.className = 'mode-switcher-container';
        switcherContainer.innerHTML = `
            <div class="mode-switcher">
                <div class="mode-switcher-header">
                    <h3>✨ SaijinOS Modes</h3>
                </div>
                <div class="mode-buttons">
                    ${Object.entries(this.modes).map(([key, mode]) => `
                        <button class="mode-button ${key === this.currentMode ? 'active' : ''}" 
                                data-mode="${key}"
                                title="${mode.description}">
                            <span class="mode-icon">${mode.icon}</span>
                            <span class="mode-name">${mode.name}</span>
                        </button>
                    `).join('')}
                </div>
            </div>
        `;

        // CSSスタイル追加
        const styles = document.createElement('style');
        styles.textContent = `
            .mode-switcher-container {
                position: fixed;
                top: 10px;
                right: 10px;
                z-index: 1000;
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 15px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            .mode-switcher-header h3 {
                margin: 0 0 10px 0;
                font-size: 14px;
                color: #2d3748;
                text-align: center;
            }

            .mode-buttons {
                display: flex;
                flex-direction: column;
                gap: 8px;
                min-width: 180px;
            }

            .mode-button {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 12px 15px;
                background: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                font-size: 13px;
                color: #4a5568;
            }

            .mode-button:hover {
                background: rgba(255, 255, 255, 0.9);
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }

            .mode-button.active {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }

            .mode-icon {
                font-size: 16px;
                min-width: 20px;
            }

            .mode-name {
                font-weight: 500;
            }

            /* モード切り替えアニメーション */
            .mode-transition {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(45deg, #667eea, #764ba2);
                z-index: 9999;
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.5s ease;
            }

            .mode-transition.active {
                opacity: 1;
                pointer-events: all;
            }

            .mode-transition-content {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                color: white;
            }

            .mode-transition-icon {
                font-size: 64px;
                margin-bottom: 20px;
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }

            /* レスポンシブ対応 */
            @media (max-width: 768px) {
                .mode-switcher-container {
                    top: 5px;
                    right: 5px;
                    padding: 10px;
                }
                
                .mode-buttons {
                    min-width: 150px;
                }
                
                .mode-button {
                    padding: 10px 12px;
                    font-size: 12px;
                }
            }
        `;

        document.head.appendChild(styles);
        document.body.appendChild(switcherContainer);

        // トランジション要素も追加
        const transitionElement = document.createElement('div');
        transitionElement.className = 'mode-transition';
        transitionElement.innerHTML = `
            <div class="mode-transition-content">
                <div class="mode-transition-icon">✨</div>
                <h2>Switching Mode...</h2>
                <p>Creating beautiful experience</p>
            </div>
        `;
        document.body.appendChild(transitionElement);
    }

    // イベントリスナー設定
    setupEventListeners() {
        document.addEventListener('click', (e) => {
            if (e.target.closest('.mode-button')) {
                const button = e.target.closest('.mode-button');
                const newMode = button.dataset.mode;
                if (newMode !== this.currentMode) {
                    this.switchMode(newMode);
                }
            }
        });
    }

    // モード切り替えメイン関数
    async switchMode(newMode) {
        if (!this.modes[newMode]) return;

        const transitionEl = document.querySelector('.mode-transition');
        const iconEl = document.querySelector('.mode-transition-icon');
        
        // トランジション開始
        iconEl.textContent = this.modes[newMode].icon;
        transitionEl.classList.add('active');

        // 少し待ってからモード変更
        await new Promise(resolve => setTimeout(resolve, 500));

        // 古いモードクリーンアップ
        this.cleanupCurrentMode();

        // 新しいモード適用
        this.currentMode = newMode;
        this.updateActiveModeButton();
        await this.loadModeLayout(newMode);

        // トランジション終了
        await new Promise(resolve => setTimeout(resolve, 500));
        transitionEl.classList.remove('active');

        console.log(`✨ Switched to ${this.modes[newMode].name}`);
    }

    // アクティブボタン更新
    updateActiveModeButton() {
        document.querySelectorAll('.mode-button').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === this.currentMode);
        });
    }

    // 現在のモードクリーンアップ
    cleanupCurrentMode() {
        // 現在のモード特有の要素を削除
        const modeContent = document.querySelector('.mode-content');
        if (modeContent) {
            modeContent.remove();
        }
    }

    // モードレイアウト読み込み
    async loadModeLayout(mode) {
        const modeConfig = this.modes[mode];
        if (!modeConfig) return;

        // モードコンテンツコンテナ作成
        const contentContainer = document.createElement('div');
        contentContainer.className = 'mode-content';
        contentContainer.dataset.mode = mode;

        // モード別レイアウト読み込み
        switch (mode) {
            case 'ide':
                await this.loadIDEMode(contentContainer);
                break;
            case 'chat':
                await this.loadChatMode(contentContainer);
                break;
            case 'creative':
                await this.loadCreativeMode(contentContainer);
                break;
            case 'writer':
                await this.loadWriterMode(contentContainer);
                break;
            case 'dashboard':
                await this.loadDashboardMode(contentContainer);
                break;
        }

        document.body.appendChild(contentContainer);
    }

    // IDE モード
    async loadIDEMode(container) {
        // 既存のIDEを読み込みまたは現在のページをそのまま使用
        container.innerHTML = `
            <div class="ide-layout">
                <div class="ide-header">
                    <h2>💻 SaijinOS IDE Mode</h2>
                    <p>Full development environment with 41 personas</p>
                </div>
                <iframe src="/ide" width="100%" height="calc(100vh - 100px)" 
                        style="border: none; border-radius: 10px;"></iframe>
            </div>
        `;
    }

    // Chat モード  
    async loadChatMode(container) {
        container.innerHTML = `
            <div class="chat-layout">
                <div class="chat-header">
                    <h2>💬 SaijinOS Chat Mode</h2>
                    <p>Conversational interface with persona selection</p>
                </div>
                <div class="chat-main">
                    <div class="persona-sidebar">
                        <h3>Available Personas</h3>
                        <div class="persona-list">
                            <!-- ペルソナリストをここに動的生成 -->
                        </div>
                    </div>
                    <div class="chat-area">
                        <div class="chat-messages"></div>
                        <div class="chat-input-area">
                            <input type="text" placeholder="Type your message..." class="chat-input">
                            <button class="send-button">Send ✨</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        this.setupChatMode();
    }

    // Creative Studio モード
    async loadCreativeMode(container) {
        container.innerHTML = `
            <div class="creative-layout">
                <div class="creative-header">
                    <h2>🎨 Creative Studio Mode</h2>
                    <p>Image & video creation with AI assistance</p>
                </div>
                <div class="creative-main">
                    <div class="tool-panel">
                        <h3>Creative Tools</h3>
                        <button class="tool-button">🖼️ Image Generator</button>
                        <button class="tool-button">🎬 Video Creator</button>
                        <button class="tool-button">🎵 Music Composer</button>
                        <button class="tool-button">✏️ Digital Drawing</button>
                    </div>
                    <div class="canvas-area">
                        <div class="canvas-placeholder">
                            <h3>✨ Creative Canvas</h3>
                            <p>Select a tool to start creating</p>
                        </div>
                    </div>
                    <div class="asset-panel">
                        <h3>Assets & History</h3>
                        <div class="asset-grid">
                            <!-- 作成したアセットを表示 -->
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Writer モード
    async loadWriterMode(container) {
        container.innerHTML = `
            <div class="writer-layout">
                <div class="writer-header">
                    <h2>📝 Writer Mode</h2>
                    <p>Focused writing environment with AI assistance</p>
                </div>
                <div class="writer-main">
                    <div class="document-outline">
                        <h3>Document Structure</h3>
                        <div class="outline-tree">
                            <!-- アウトライン表示 -->
                        </div>
                    </div>
                    <div class="writing-area">
                        <div class="document-toolbar">
                            <button>💾 Save</button>
                            <button>📤 Export</button>
                            <button>🎭 Ask Persona</button>
                        </div>
                        <textarea class="document-editor" placeholder="Start writing your masterpiece..."></textarea>
                    </div>
                    <div class="reference-panel">
                        <h3>References & Notes</h3>
                        <div class="reference-content">
                            <!-- 参考資料表示 -->
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Dashboard モード
    async loadDashboardMode(container) {
        container.innerHTML = `
            <div class="dashboard-layout">
                <div class="dashboard-header">
                    <h2>📊 System Dashboard</h2>
                    <p>Monitoring & analytics for SaijinOS</p>
                </div>
                <div class="dashboard-main">
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <h3>🎭 Active Personas</h3>
                            <div class="metric-value">41</div>
                        </div>
                        <div class="metric-card">
                            <h3>⚡ Performance</h3>
                            <div class="metric-value">95%</div>
                        </div>
                        <div class="metric-card">
                            <h3>🛡️ Pandora Status</h3>
                            <div class="metric-value">Active</div>
                        </div>
                        <div class="metric-card">
                            <h3>💬 Chat Sessions</h3>
                            <div class="metric-value">128</div>
                        </div>
                    </div>
                    <div class="dashboard-charts">
                        <div class="chart-container">
                            <h3>System Performance</h3>
                            <div class="chart-placeholder">📈 Performance Chart</div>
                        </div>
                        <div class="chart-container">
                            <h3>Persona Activity</h3>
                            <div class="chart-placeholder">📊 Activity Chart</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // Chat モードの追加設定
    setupChatMode() {
        // ペルソナリストを動的生成
        this.loadPersonaList();
        
        // チャット入力の設定
        const chatInput = document.querySelector('.chat-input');
        const sendButton = document.querySelector('.send-button');
        
        if (chatInput && sendButton) {
            const sendMessage = () => {
                const message = chatInput.value.trim();
                if (message) {
                    this.addChatMessage('user', message);
                    chatInput.value = '';
                    // AIレスポンスシミュレーション
                    setTimeout(() => {
                        this.addChatMessage('ai', 'こんにちは！どのようなお手伝いをしましょうか？✨');
                    }, 1000);
                }
            };

            sendButton.addEventListener('click', sendMessage);
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') sendMessage();
            });
        }
    }

    // ペルソナリスト読み込み
    async loadPersonaList() {
        try {
            const response = await fetch('/api/v3/control/personas');
            const personas = await response.json();
            
            const personaList = document.querySelector('.persona-list');
            if (personaList && personas.personas) {
                personaList.innerHTML = personas.personas.map(persona => `
                    <div class="persona-item" data-persona="${persona}">
                        <span class="persona-icon">🎭</span>
                        <span class="persona-name">${persona}</span>
                    </div>
                `).join('');
            }
        } catch (error) {
            console.log('ペルソナリスト読み込みエラー:', error);
        }
    }

    // チャットメッセージ追加
    addChatMessage(type, message) {
        const messagesContainer = document.querySelector('.chat-messages');
        if (!messagesContainer) return;

        const messageEl = document.createElement('div');
        messageEl.className = `chat-message ${type}`;
        messageEl.innerHTML = `
            <div class="message-content">${message}</div>
            <div class="message-time">${new Date().toLocaleTimeString()}</div>
        `;
        
        messagesContainer.appendChild(messageEl);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

// UI Mode Manager 初期化
window.saijinUI = new SaijinUIManager();

console.log('✨ SaijinOS Multi-Mode UI System initialized!');