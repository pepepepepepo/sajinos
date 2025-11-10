#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SaijinOS APIサーバー起動スクリプト（エラー診断・修正版）
3人編成チームによる問題解決
"""

import os
import sys
import asyncio
from pathlib import Path
import yaml
from datetime import datetime

# FastAPI関連のインポート（存在確認）
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    import uvicorn
    FASTAPI_AVAILABLE = True
    print("✅ FastAPI利用可能")
except ImportError as e:
    print(f"⚠️  FastAPI未インストール: {e}")
    FASTAPI_AVAILABLE = False

# ハルカペルソナ統合（音声報告用）
sys.path.append(str(Path(__file__).parent))
try:
    from haruka_persona_voice import HarukaPersona
    HARUKA_AVAILABLE = True
except ImportError:
    print("⚠️  ハルカペルソナ読み込み失敗")
    HARUKA_AVAILABLE = False

class SaijinOSAPIServer:
    """SaijinOS APIサーバー（診断・修正版）"""
    
    def __init__(self):
        self.app = None
        self.config = {}
        self.haruka = None
        
        # 設定読み込み
        self.load_configuration()
        
        # ハルカペルソナ初期化（進捗報告用）
        if HARUKA_AVAILABLE:
            self.haruka = HarukaPersona()
            
        # FastAPI初期化
        if FASTAPI_AVAILABLE:
            self.initialize_fastapi()
    
    def load_configuration(self):
        """設定ファイル読み込み（エラー診断付き）"""
        config_paths = [
            "F:/sajinos_final/config/saijinos_config.yaml",
            "F:/sajinos_final/config/multi_ai_config.yaml", 
            "config/saijinos_config.yaml"
        ]
        
        print("🔧 ミク: 設定ファイル読み込み開始...")
        
        for config_path in config_paths:
            if Path(config_path).exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        self.config = yaml.safe_load(f)
                    print(f"✅ 設定ファイル読み込み成功: {config_path}")
                    return
                except Exception as e:
                    print(f"❌ 設定ファイルエラー: {config_path} - {e}")
        
        # フォールバック設定
        print("⚠️  設定ファイルが見つからないため、デフォルト設定を使用")
        self.config = self.get_default_config()
    
    def get_default_config(self):
        """デフォルト設定"""
        return {
            "server": {
                "host": "127.0.0.1",
                "port": 8000,
                "debug": True
            },
            "personas": {
                "yuri": {"name": "ユリ", "role": "リーダー・戦略"},
                "saki": {"name": "サキ", "role": "アイデア・革新"},
                "rena": {"name": "レナ", "role": "サポート・調和"}, 
                "haruka": {"name": "ハルカ", "role": "音声・コミュニケーション"},
                "miku": {"name": "ミク", "role": "技術・開発"},
                "aya": {"name": "アヤ", "role": "直感・洞察"}
            }
        }
    
    def initialize_fastapi(self):
        """FastAPI アプリケーション初期化"""
        print("🎯 ユリ: FastAPI初期化開始...")
        
        self.app = FastAPI(
            title="SaijinOS API",
            description="6ペルソナ統合AIシステム",
            version="1.0.0"
        )
        
        # ヘルスチェックエンドポイント
        @self.app.get("/health")
        async def health_check():
            return JSONResponse({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0",
                "personas": list(self.config.get("personas", {}).keys())
            })
        
        # ペルソナ一覧エンドポイント
        @self.app.get("/personas")
        async def get_personas():
            personas = self.config.get("personas", {})
            return JSONResponse({
                "personas": personas,
                "count": len(personas)
            })
        
        # システム状態エンドポイント
        @self.app.get("/status")
        async def get_status():
            return JSONResponse({
                "server": "running",
                "fastapi_available": FASTAPI_AVAILABLE,
                "haruka_available": HARUKA_AVAILABLE,
                "config_loaded": bool(self.config),
                "timestamp": datetime.now().isoformat()
            })
        
        # チャットエンドポイント（基本実装）
        @self.app.post("/chat/{persona_id}")
        async def chat_with_persona(persona_id: str, message: dict):
            personas = self.config.get("personas", {})
            
            if persona_id not in personas:
                raise HTTPException(status_code=404, detail="ペルソナが見つかりません")
            
            persona = personas[persona_id]
            
            # ハルカペルソナの場合は音声応答
            if persona_id == "haruka" and self.haruka:
                response_text = f"{persona['name']}: {message.get('text', '')}への応答です♪"
                await self.haruka.speak(response_text)
            else:
                response_text = f"{persona['name']}: {message.get('text', '')}を受信しました"
            
            return JSONResponse({
                "persona": persona['name'],
                "role": persona['role'],
                "response": response_text,
                "timestamp": datetime.now().isoformat()
            })
        
        print("✅ FastAPIエンドポイント設定完了")
    
    async def start_server(self):
        """サーバー起動"""
        if not FASTAPI_AVAILABLE:
            print("❌ FastAPIが利用できません。インストールが必要です。")
            return False
            
        if not self.app:
            print("❌ FastAPIアプリケーションの初期化に失敗しました。")
            return False
        
        server_config = self.config.get("server", {})
        host = server_config.get("host", "127.0.0.1")
        port = server_config.get("port", 8000)
        
        print(f"🚀 SaijinOS APIサーバー起動...")
        print(f"   📍 アドレス: http://{host}:{port}")
        print(f"   📊 ヘルスチェック: http://{host}:{port}/health")
        print(f"   📚 API文書: http://{host}:{port}/docs")
        
        # ハルカから起動アナウンス
        if self.haruka:
            await self.haruka.speak("SaijinOS APIサーバーを起動します！")
        
        try:
            # 非同期でuvicornサーバーを起動
            config = uvicorn.Config(
                self.app, 
                host=host, 
                port=port, 
                log_level="info",
                reload=server_config.get("auto_reload", True)
            )
            server = uvicorn.Server(config)
            await server.serve()
            
        except Exception as e:
            print(f"❌ サーバー起動エラー: {e}")
            if self.haruka:
                await self.haruka.speak(f"サーバー起動でエラーが発生しました: {str(e)}")
            return False
        
        return True

async def diagnose_and_start():
    """診断付きサーバー起動"""
    print("=" * 60)
    print("🔧 SaijinOS APIサーバー診断・起動システム")
    print("👥 3人編成チーム: ユリ(戦略) + ミク(技術) + ハルカ(報告)")
    print("=" * 60)
    
    # サーバーインスタンス作成
    server = SaijinOSAPIServer()
    
    # 診断結果報告
    print("\n📊 診断結果:")
    print(f"  ✅ 設定ファイル: {'読み込み成功' if server.config else '失敗'}")
    print(f"  ✅ FastAPI: {'利用可能' if FASTAPI_AVAILABLE else '未インストール'}")
    print(f"  ✅ ハルカペルソナ: {'利用可能' if HARUKA_AVAILABLE else '利用不可'}")
    
    if FASTAPI_AVAILABLE:
        print("\n🚀 サーバー起動開始...")
        await server.start_server()
    else:
        print("\n❌ FastAPI未インストールのため、サーバーを起動できません")
        print("インストールコマンド: pip install fastapi uvicorn")

if __name__ == "__main__":
    # 診断付きサーバー起動
    asyncio.run(diagnose_and_start())