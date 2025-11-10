"""
Phase 1 統合システム APIテストスクリプト
作成日: 2025年11月8日
"""

import requests
import json
import time

def test_integrated_api():
    """Phase 1統合システム APIテスト実行"""
    base_url = "http://localhost:8000"
    
    print("🧪 === Phase 1統合システム APIテスト開始 ===")
    print()
    
    try:
        # 1. ルートエンドポイントテスト
        print("1️⃣ ルートAPI テスト")
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ システム: {data.get('system')}")
            print(f"   ✅ バージョン: {data.get('version')}")  
            print(f"   ✅ 利用可能ペルソナ: {data.get('available_personas')}人")
            print(f"   ✅ 音声統合: {data.get('voice_integration')}")
        else:
            print(f"   ❌ ルートAPI失敗: {response.status_code}")
        print()
            
        # 2. ヘルスチェックテスト
        print("2️⃣ ヘルスチェックAPI テスト")
        response = requests.get(f"{base_url}/api/v1/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ コアシステム: {data.get('core_system')}")
            print(f"   ✅ 音声システム: {data.get('voice_system')}")
            print(f"   ✅ 統合機能: {', '.join(data.get('integrated_functions', []))}")
        else:
            print(f"   ❌ ヘルスチェック失敗: {response.status_code}")
        print()
            
        # 3. ペルソナ一覧テスト
        print("3️⃣ ペルソナ一覧API テスト")
        response = requests.get(f"{base_url}/api/v1/personas", timeout=5)
        if response.status_code == 200:
            data = response.json()
            personas = data.get('personas', [])
            integration_ready = data.get('integration_ready', [])
            
            print(f"   ✅ 登録ペルソナ数: {len(personas)}人")
            print(f"   ✅ 音声対応ペルソナ: {len(integration_ready)}人")
            
            print("\n   📋 ペルソナ詳細:")
            for persona in personas:
                status = "🔊音声対応" if persona.get('tts_available') else "🔄準備中"
                print(f"      - {persona.get('name')} ({persona.get('id')}): {persona.get('role')} {status}")
        else:
            print(f"   ❌ ペルソナ一覧取得失敗: {response.status_code}")
        print()
            
        # 4. ペルソナチャットテスト (ハルカ)
        print("4️⃣ ハルカペルソナ チャットテスト")
        chat_data = {"message": "こんにちは！統合システムのテストです"}
        response = requests.post(f"{base_url}/api/v1/personas/haruka/chat", 
                               json=chat_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ ペルソナ: {data.get('persona', {}).get('name')}")
            print(f"   ✅ レスポンス: {data.get('response')[:60]}...")
            print(f"   ✅ 音声利用可能: {data.get('voice_available')}")
        else:
            print(f"   ❌ チャットテスト失敗: {response.status_code}")
        print()
            
        # 5. 音声エンドポイントテスト 
        print("5️⃣ 音声生成API テスト")
        voice_data = {"text": "統合システムテスト音声です", "persona_id": "haruka"}
        response = requests.post(f"{base_url}/api/v1/personas/haruka/speak",
                               json=voice_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            voice_result = data.get('voice_result', {})
            print(f"   ✅ 音声生成: {voice_result.get('success')}")
            if voice_result.get('success'):
                print(f"   ✅ 音声ファイル: {voice_result.get('audio_file')}")
                print(f"   ✅ 生成時間: {voice_result.get('generation_time')}")
            else:
                print(f"   ⚠️  フォールバック: {voice_result.get('fallback')}")
        else:
            print(f"   ❌ 音声生成テスト失敗: {response.status_code}")
        print()
            
        # 6. 統合ステータステスト
        print("6️⃣ 統合システム ステータステスト")
        response = requests.get(f"{base_url}/api/v1/integration/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ フェーズ: {data.get('phase')}")
            print(f"   ✅ コアペルソナ: {data.get('core_personas')}人")
            print(f"   ✅ 音声対応: {data.get('voice_ready_personas')}人")
            print(f"   ✅ 音声システム状態: {data.get('voice_system_status')}")
            print(f"   ✅ 統合進捗: {data.get('integration_progress')}")
            print(f"   ✅ 次段階: {data.get('next_phase')}")
        else:
            print(f"   ❌ ステータステスト失敗: {response.status_code}")
        print()
            
        print("🎊 === Phase 1統合システム APIテスト完了 ===")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ サーバーに接続できません。統合システムが起動していることを確認してください。")
        return False
    except requests.exceptions.Timeout:
        print("❌ APIリクエストがタイムアウトしました。")
        return False
    except Exception as e:
        print(f"❌ テスト中にエラーが発生: {e}")
        return False

if __name__ == "__main__":
    test_integrated_api()