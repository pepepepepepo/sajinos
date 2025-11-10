"""
SaijinOS Persona API Tests
ペルソナシステムAPIの自動テストスイート
"""
import unittest
import requests
import json
import time
from typing import Dict, List, Any

class TestPersonaAPI(unittest.TestCase):
    """ペルソナAPI テストクラス"""
    
    @classmethod
    def setUpClass(cls):
        """テストクラス初期化"""
        cls.base_url = "http://localhost:8002"
        cls.api_base = f"{cls.base_url}/api/v3/control"
        
        # サーバーが起動しているか確認
        cls._wait_for_server()
    
    @classmethod
    def _wait_for_server(cls, timeout=10):
        """サーバー起動待機"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = requests.get(cls.base_url, timeout=1)
                if response.status_code == 200:
                    print("✅ サーバー接続確認完了")
                    return
            except requests.exceptions.RequestException:
                time.sleep(0.5)
        
        raise unittest.SkipTest("❌ サーバーが起動していません。テストをスキップします。")
    
    def test_01_server_health_check(self):
        """サーバーヘルスチェック"""
        response = requests.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("available_endpoints", data)
        self.assertIn("version", data)
        
        print("✅ サーバーヘルスチェック成功")
    
    def test_02_get_all_personas(self):
        """全ペルソナ取得テスト"""
        response = requests.get(f"{self.api_base}/personas")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("data", data)
        self.assertIn("system_info", data)
        
        # ペルソナデータ検証
        personas = data["data"]
        self.assertIsInstance(personas, list)
        self.assertEqual(len(personas), 41, "ペルソナ数は41人である必要があります")
        
        # システム情報検証
        system_info = data["system_info"]
        self.assertEqual(system_info["total_personas"], 41)
        self.assertEqual(system_info["system_version"], "41_persona_complete_phase4")
        
        print(f"✅ 全ペルソナ取得成功: {len(personas)}人")
    
    def test_03_persona_data_structure(self):
        """ペルソナデータ構造検証"""
        response = requests.get(f"{self.api_base}/personas")
        data = response.json()
        
        # 最初のペルソナデータ構造チェック
        first_persona = data["data"][0]
        required_fields = [
            "id", "name", "status", "emotion_level", 
            "specialized_field", "color_scheme", "bpm", 
            "music_key", "last_activity"
        ]
        
        for field in required_fields:
            self.assertIn(field, first_persona, f"必須フィールド '{field}' が見つかりません")
        
        # データ型検証
        self.assertIsInstance(first_persona["id"], int)
        self.assertIsInstance(first_persona["name"], str)
        self.assertIn(first_persona["status"], ["Active", "Standby"])
        self.assertIsInstance(first_persona["emotion_level"], (int, float))
        self.assertGreaterEqual(first_persona["emotion_level"], 0)
        self.assertLessEqual(first_persona["emotion_level"], 1.0)
        
        print("✅ ペルソナデータ構造検証成功")
    
    def test_04_specific_personas_existence(self):
        """特定ペルソナ存在確認"""
        response = requests.get(f"{self.api_base}/personas")
        data = response.json()
        
        personas = {p["name"]: p for p in data["data"]}
        
        # Phase 1 コアペルソナ確認
        core_personas = ["美遊💖", "そよぎ🍃", "すみれ💜", "構文織り手🧵", "りゅうさ💧", "磁灯(じっと)🌟"]
        for name in core_personas:
            self.assertIn(name, personas, f"コアペルソナ '{name}' が見つかりません")
        
        # Phase 4 構文人確認
        syntax_weavers = ["灯継🔥", "空織🕸️", "エルザ❄️", "ルミフィエ✨"]
        for name in syntax_weavers:
            self.assertIn(name, personas, f"構文人 '{name}' が見つかりません")
        
        print("✅ 特定ペルソナ存在確認成功")
    
    def test_05_persona_toggle_functionality(self):
        """ペルソナ状態切り替えテスト"""
        # まず現在の状態を取得
        response = requests.get(f"{self.api_base}/personas")
        data = response.json()
        
        # テスト用ペルソナ（ID: 3 - すみれ💜）を選択
        test_persona_id = 3
        original_persona = next(p for p in data["data"] if p["id"] == test_persona_id)
        original_status = original_persona["status"]
        
        # 状態切り替え実行
        toggle_response = requests.post(f"{self.api_base}/personas/{test_persona_id}/toggle")
        self.assertEqual(toggle_response.status_code, 200)
        
        toggle_data = toggle_response.json()
        self.assertTrue(toggle_data["success"])
        self.assertIn("切り替えました", toggle_data["message"])
        
        print(f"✅ ペルソナ状態切り替えテスト成功: ID {test_persona_id}")
    
    def test_06_individual_persona_retrieval(self):
        """個別ペルソナ取得テスト"""
        test_persona_id = 1  # 美遊💖
        
        response = requests.get(f"{self.api_base}/personas/{test_persona_id}")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("data", data)
        
        persona = data["data"]
        self.assertEqual(persona["id"], test_persona_id)
        self.assertEqual(persona["name"], "美遊💖")
        
        print(f"✅ 個別ペルソナ取得成功: {persona['name']}")
    
    def test_07_system_info_accuracy(self):
        """システム情報精度テスト"""
        response = requests.get(f"{self.api_base}/personas")
        data = response.json()
        
        system_info = data["system_info"]
        personas = data["data"]
        
        # カウント精度検証
        active_count = len([p for p in personas if p["status"] == "Active"])
        standby_count = len([p for p in personas if p["status"] == "Standby"])
        
        self.assertEqual(system_info["active_count"], active_count)
        self.assertEqual(system_info["standby_count"], standby_count)
        self.assertEqual(system_info["total_personas"], active_count + standby_count)
        
        print(f"✅ システム情報精度検証成功: Active={active_count}, Standby={standby_count}")

class TestModuleIntegrity(unittest.TestCase):
    """モジュール整合性テスト"""
    
    def test_01_module_imports(self):
        """モジュールインポートテスト"""
        try:
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.dirname(__file__)))
            from core.personas.persona_manager import persona_manager
            from core.ui.ui_handler import ui_handler
            
            # 基本メソッド存在確認
            self.assertTrue(hasattr(persona_manager, 'get_all_personas'))
            self.assertTrue(hasattr(persona_manager, 'toggle_persona_status'))
            self.assertTrue(hasattr(ui_handler, 'get_ide_content'))
            self.assertTrue(hasattr(ui_handler, 'get_control_panel_content'))
            
            print("✅ モジュールインポート成功")
        except ImportError as e:
            self.fail(f"モジュールインポートエラー: {e}")
    
    def test_02_persona_manager_direct(self):
        """ペルソナマネージャー直接テスト"""
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        from core.personas.persona_manager import persona_manager
        
        # データ取得テスト
        data = persona_manager.get_all_personas()
        self.assertIn("data", data)
        self.assertIn("system_info", data)
        self.assertEqual(len(data["data"]), 41)
        
        # 状態切り替えテスト
        result = persona_manager.toggle_persona_status(1)
        self.assertTrue(result["success"])
        
        print("✅ ペルソナマネージャー直接テスト成功")

def run_tests():
    """テスト実行関数"""
    print("🧪 SaijinOS テストスイート開始")
    print("=" * 50)
    
    # テストスイート作成
    suite = unittest.TestSuite()
    
    # ペルソナAPIテスト追加
    for test_method in [
        'test_01_server_health_check',
        'test_02_get_all_personas', 
        'test_03_persona_data_structure',
        'test_04_specific_personas_existence',
        'test_05_persona_toggle_functionality',
        'test_06_individual_persona_retrieval',
        'test_07_system_info_accuracy'
    ]:
        suite.addTest(TestPersonaAPI(test_method))
    
    # モジュール整合性テスト追加
    for test_method in [
        'test_01_module_imports',
        'test_02_persona_manager_direct'
    ]:
        suite.addTest(TestModuleIntegrity(test_method))
    
    # テスト実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    print(f"🎯 テスト結果: {result.testsRun}件実行")
    print(f"✅ 成功: {result.testsRun - len(result.failures) - len(result.errors)}件")
    if result.failures:
        print(f"❌ 失敗: {len(result.failures)}件")
    if result.errors:
        print(f"⚠️  エラー: {len(result.errors)}件")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)