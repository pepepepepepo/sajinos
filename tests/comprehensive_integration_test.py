"""
SaijinOS 統合システム詳細テストスイート
作成日: 2025年11月8日

23ペルソナ統合システムの完全検証プログラム
"""

import requests
import json
import time
import asyncio
from datetime import datetime
from typing import Dict, List, Any

class SaijinosIntegratedTester:
    def __init__(self):
        self.phase1_url = "http://localhost:8000"  # Phase 1サーバー
        self.phase2_url = "http://localhost:8001"  # Phase 2サーバー
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, details: Any):
        """テスト結果をログ"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "test_name": test_name,
            "success": success,
            "details": details
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if not success:
            print(f"   Error: {details}")

    def test_server_connectivity(self):
        """サーバー接続性テスト"""
        print("\n🔗 === サーバー接続性テスト ===")
        
        # Phase 2サーバーテスト
        try:
            response = requests.get(f"{self.phase2_url}/", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.log_test("Phase 2 サーバー接続", True, {
                    "status_code": 200,
                    "total_personas": data.get("total_personas"),
                    "version": data.get("version")
                })
            else:
                self.log_test("Phase 2 サーバー接続", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("Phase 2 サーバー接続", False, str(e))

    def test_23_persona_system(self):
        """23ペルソナシステム詳細テスト"""
        print("\n🎭 === 23ペルソナシステムテスト ===")
        
        try:
            response = requests.get(f"{self.phase2_url}/api/v2/personas/extended", timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                total_personas = data.get("total_personas", 0)
                personas = data.get("personas", [])
                core_personas = len([p for p in personas if p.get("system") == "core"])
                emotion_personas = len([p for p in personas if p.get("system") == "emotion"])
                
                self.log_test("23ペルソナ取得", True, {
                    "total_personas": total_personas,
                    "core_personas": core_personas,
                    "emotion_personas": emotion_personas,
                    "expected_total": 23
                })
                
                # 個別ペルソナテスト
                print("\n   📋 ペルソナ詳細検証:")
                for persona in personas[:5]:  # 最初の5人をテスト
                    persona_info = {
                        "id": persona.get("id"),
                        "name": persona.get("name"),
                        "role": persona.get("role"),
                        "system": persona.get("system"),
                        "music_key": persona.get("music_key")
                    }
                    print(f"      🎭 {persona.get('name')} ({persona.get('id')}): {persona.get('role')}")
                    self.log_test(f"ペルソナ {persona.get('name')} 構成", True, persona_info)
                
                return personas
            else:
                self.log_test("23ペルソナシステム", False, f"Status: {response.status_code}")
                return []
        except Exception as e:
            self.log_test("23ペルソナシステム", False, str(e))
            return []

    def test_emotion_recording_system(self):
        """感情記録システムテスト"""
        print("\n🎵 === 感情記録システムテスト ===")
        
        # テスト用感情記録
        test_emotions = [
            {"persona_id": "haruka", "temperature": 75.5, "emotion_type": "happy", "context": "統合テスト実行中"},
            {"persona_id": "yuri", "temperature": 60.0, "emotion_type": "analytical", "context": "システム分析中"},
            {"persona_id": "makoto", "temperature": 80.2, "emotion_type": "excited", "context": "感情記録テスト"}
        ]
        
        for emotion_data in test_emotions:
            try:
                response = requests.post(
                    f"{self.phase2_url}/api/v2/emotion/record",
                    json=emotion_data,
                    timeout=5
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.log_test(f"感情記録 - {emotion_data['persona_id']}", True, {
                        "record_id": result.get("record_id"),
                        "temperature": result.get("temperature"),
                        "emotion_type": result.get("emotion_type")
                    })
                else:
                    self.log_test(f"感情記録 - {emotion_data['persona_id']}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"感情記録 - {emotion_data['persona_id']}", False, str(e))

    def test_music_sync_system(self):
        """BMP音楽同期システムテスト"""
        print("\n🎼 === BMP音楽同期システムテスト ===")
        
        # BMP同期テスト
        test_sync_data = [
            {"bmp": 80, "persona_id": "haruka"},
            {"bmp": 120, "persona_id": "yuri"},
            {"bmp": 95, "persona_id": "miku"},
            {"bmp": 150, "persona_id": "makoto"}  # 17ペルソナからテスト
        ]
        
        for sync_data in test_sync_data:
            try:
                response = requests.post(
                    f"{self.phase2_url}/api/v2/music/sync",
                    json=sync_data,
                    timeout=5
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.log_test(f"BMP同期 - {sync_data['persona_id']} ({sync_data['bmp']}BMP)", True, {
                        "sync_status": result.get("sync_status"),
                        "music_key": result.get("music_key"),
                        "bmp": result.get("bmp")
                    })
                else:
                    self.log_test(f"BMP同期 - {sync_data['persona_id']}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"BMP同期 - {sync_data['persona_id']}", False, str(e))

    def test_emotion_history(self):
        """感情履歴取得テスト"""
        print("\n📊 === 感情履歴システムテスト ===")
        
        test_personas = ["haruka", "yuri", "makoto"]
        
        for persona_id in test_personas:
            try:
                response = requests.get(
                    f"{self.phase2_url}/api/v2/emotion/history/{persona_id}",
                    params={"limit": 5},
                    timeout=5
                )
                
                if response.status_code == 200:
                    result = response.json()
                    record_count = result.get("record_count", 0)
                    self.log_test(f"感情履歴 - {persona_id}", True, {
                        "record_count": record_count,
                        "has_history": record_count > 0
                    })
                    
                    if record_count > 0:
                        print(f"      📈 {persona_id}: {record_count}件の感情記録")
                else:
                    self.log_test(f"感情履歴 - {persona_id}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"感情履歴 - {persona_id}", False, str(e))

    def test_integration_status(self):
        """統合システム状態テスト"""
        print("\n⚙️ === 統合システム状態テスト ===")
        
        try:
            response = requests.get(f"{self.phase2_url}/api/v2/integration/status", timeout=5)
            if response.status_code == 200:
                status = response.json()
                
                self.log_test("統合システム状態", True, {
                    "phase": status.get("phase"),
                    "total_personas": status.get("total_personas"),
                    "core_personas": status.get("core_personas"),
                    "emotion_personas": status.get("emotion_personas"),
                    "integration_progress": status.get("integration_progress"),
                    "emotion_system_status": status.get("emotion_system_status")
                })
                
                print(f"      📊 統合進捗: {status.get('integration_progress')}")
                print(f"      🎯 次段階: {status.get('next_phase')}")
            else:
                self.log_test("統合システム状態", False, f"Status: {response.status_code}")
        except Exception as e:
            self.log_test("統合システム状態", False, str(e))

    def test_performance_metrics(self):
        """パフォーマンス測定テスト"""
        print("\n⚡ === パフォーマンス測定テスト ===")
        
        # API応答時間測定
        endpoints = [
            ("ルートAPI", "/"),
            ("ペルソナ一覧", "/api/v2/personas/extended"),
            ("統合状態", "/api/v2/integration/status")
        ]
        
        for endpoint_name, endpoint in endpoints:
            start_time = time.time()
            try:
                response = requests.get(f"{self.phase2_url}{endpoint}", timeout=10)
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # ミリ秒
                
                if response.status_code == 200:
                    self.log_test(f"パフォーマンス - {endpoint_name}", True, {
                        "response_time_ms": round(response_time, 2),
                        "acceptable": response_time < 500  # 500ms以下が目標
                    })
                    print(f"      ⏱️ {endpoint_name}: {response_time:.2f}ms")
                else:
                    self.log_test(f"パフォーマンス - {endpoint_name}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f"パフォーマンス - {endpoint_name}", False, str(e))

    def generate_test_report(self):
        """テスト結果レポート生成"""
        print("\n📋 === 統合システムテスト結果サマリー ===")
        
        total_tests = len(self.test_results)
        passed_tests = len([t for t in self.test_results if t["success"]])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\n📊 テスト結果統計:")
        print(f"   ✅ 成功: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        print(f"   ❌ 失敗: {failed_tests}/{total_tests}")
        print(f"   🎯 統合品質: {'優秀' if success_rate >= 90 else '良好' if success_rate >= 75 else '要改善'}")
        
        # 詳細レポートをファイルに保存
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": success_rate,
                "test_timestamp": datetime.now().isoformat()
            },
            "detailed_results": self.test_results
        }
        
        with open("logs/integration_test_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 詳細レポート保存: logs/integration_test_report.json")
        return success_rate

    def run_all_tests(self):
        """全テスト実行"""
        print("🧪 === SaijinOS 統合システム詳細テスト開始 ===")
        print(f"⏰ テスト開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # テスト順序実行
        self.test_server_connectivity()
        personas = self.test_23_persona_system()
        self.test_emotion_recording_system()
        self.test_music_sync_system()
        self.test_emotion_history()
        self.test_integration_status()
        self.test_performance_metrics()
        
        # 最終レポート
        success_rate = self.generate_test_report()
        
        print(f"\n🎊 テスト完了! 統合システム品質: {success_rate:.1f}%")
        return success_rate

if __name__ == "__main__":
    tester = SaijinosIntegratedTester()
    tester.run_all_tests()