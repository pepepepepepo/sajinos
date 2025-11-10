#!/usr/bin/env python3
"""
SaijinOS Quick Test Script
簡易テストスクリプト
"""
import requests
import sys
import time

def test_server():
    """サーバー基本テスト"""
    base_url = "http://localhost:8002"
    
    print("🧪 SaijinOS クイックテスト開始")
    print("=" * 40)
    
    try:
        # 1. サーバーヘルスチェック
        print("1️⃣  サーバーヘルスチェック...")
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ サーバー正常稼働")
            data = response.json()
            print(f"   Version: {data.get('version', 'N/A')}")
        else:
            print(f"❌ サーバーエラー: {response.status_code}")
            return False
        
        # 2. ペルソナAPI テスト
        print("\n2️⃣  ペルソナAPI テスト...")
        response = requests.get(f"{base_url}/api/v3/control/personas", timeout=5)
        if response.status_code == 200:
            data = response.json()
            personas_count = len(data.get("data", []))
            print(f"✅ ペルソナ取得成功: {personas_count}人")
            
            # システム情報確認
            system_info = data.get("system_info", {})
            print(f"   Total: {system_info.get('total_personas', 'N/A')}")
            print(f"   Active: {system_info.get('active_count', 'N/A')}")
            print(f"   Standby: {system_info.get('standby_count', 'N/A')}")
        else:
            print(f"❌ ペルソナAPI エラー: {response.status_code}")
            return False
        
        # 3. 個別ペルソナテスト
        print("\n3️⃣  個別ペルソナテスト...")
        response = requests.get(f"{base_url}/api/v3/control/personas/1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                persona = data.get("data", {})
                print(f"✅ 個別取得成功: {persona.get('name', 'N/A')}")
            else:
                print("❌ 個別取得失敗")
                return False
        else:
            print(f"❌ 個別ペルソナAPI エラー: {response.status_code}")
            return False
        
        print("\n" + "=" * 40)
        print("🎉 全テスト成功！")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ サーバーに接続できません。サーバーが起動していることを確認してください。")
        return False
    except Exception as e:
        print(f"❌ テスト中にエラーが発生しました: {e}")
        return False

if __name__ == "__main__":
    success = test_server()
    sys.exit(0 if success else 1)