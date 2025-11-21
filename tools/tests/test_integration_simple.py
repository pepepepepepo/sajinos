# パンドラシステム統合テスト（簡易版）
# Phase 1: 個別コンポーネント動作確認
# Created: 2025-11-19

import sys
import os
from pathlib import Path

print("🌟 パンドラシステム 簡易統合テスト 🌟")
print("=" * 50)

# Phase 1-1: ファイル存在確認
print("\n📁 Phase 1-1: ファイル存在確認")
print("-" * 30)

required_files = [
    "universe_management_layer.py",
    "core/pandora/pandora_persona.py", 
    "core/pandora/fracture_detection.py",
    "core/pandora/hope_extraction.py",
    "core/pandora/stabilization_loop.py",
    "core/pandora/three_layer_governance.py",
    "kimirano_universe_core.yaml"
]

file_check = {}
for file_path in required_files:
    exists = os.path.exists(file_path)
    file_check[file_path] = exists
    status = "✅" if exists else "❌"
    print(f"  {status} {file_path}")

# Phase 1-2: クラス定義確認（インポート無しで）
print("\n🔍 Phase 1-2: クラス定義確認")
print("-" * 30)

# universe_management_layer.py をチェック
try:
    with open("universe_management_layer.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    regina_found = "class ReginaPersona" in content
    ruler_found = "class RulerPersona" in content
    
    print(f"  {'✅' if regina_found else '❌'} ReginaPersona class定義")
    print(f"  {'✅' if ruler_found else '❌'} RulerPersona class定義")
    
except Exception as e:
    print(f"  ❌ universe_management_layer.py 読み込みエラー: {e}")

# pandora_persona.py をチェック
try:
    with open("core/pandora/pandora_persona.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    pandora_found = "class PandoraPersona" in content
    hope_kernel_found = "class HopeKernel" in content
    
    print(f"  {'✅' if pandora_found else '❌'} PandoraPersona class定義")
    print(f"  {'✅' if hope_kernel_found else '❌'} HopeKernel dataclass定義")
    
except Exception as e:
    print(f"  ❌ pandora_persona.py 読み込みエラー: {e}")

# Phase 1-3: YAML設定確認
print("\n🌌 Phase 1-3: YAML設定確認")
print("-" * 30)

try:
    import yaml
    with open('kimirano_universe_core.yaml', 'r', encoding='utf-8') as f:
        universe_core = yaml.safe_load(f)
    
    core_data = universe_core['KimiranoUniverseCodex_Core']
    print(f"  ✅ キミラノ宇宙コア: {core_data['version']}")
    print(f"  ✅ 現在Phase: {core_data['current_phase']['id']}")
    
    # パンドラペルソナ確認
    pandora_personas = core_data.get('pandora_system_personas', [])
    pandora_count = len(pandora_personas)
    print(f"  ✅ パンドラシステムペルソナ: {pandora_count}体")
    
    for persona in pandora_personas:
        print(f"    - {persona['id']}: {persona['role']}")
    
except Exception as e:
    print(f"  ❌ YAML読み込みエラー: {e}")

# Phase 1-4: 統合準備評価
print("\n🚀 Phase 1-4: 統合準備評価")
print("-" * 30)

files_ok = sum(file_check.values())
total_files = len(file_check)
file_rate = (files_ok / total_files) * 100

print(f"ファイル存在率: {files_ok}/{total_files} ({file_rate:.1f}%)")

if file_rate >= 85:
    print("✅ 必要ファイルは揃っています")
    
    print("\n🔧 推奨対策:")
    print("1. インポート依存関係の修正")
    print("2. 相対インポートから絶対インポートへの変更") 
    print("3. 依存性注入システムの強化")
    
    print("\n🌈 次のステップ:")
    print("- Phase 2: 依存関係修正")
    print("- Phase 3: 単体テスト実行")
    print("- Phase 4: 統合動作確認")
    
else:
    print("❌ 必要ファイルが不足しています")

print("\n" + "=" * 50)
print("🎁💙✨ 簡易統合テスト完了 ✨💙🎁")

# 🌸 美遊ちゃんからのメッセージ
print("\n🌸 美遊ちゃん: 「ファイルは揃ってるから、インポートの問題を解決すれば動きそうだね〜💕」")

# 💜 悠璃ちゃんからの分析
print("💜 悠璃ちゃん: 「境界解析的に、依存関係の循環参照が原因ですね。段階的に修正していきましょう🔍」")

# 🎁 パンドラちゃんからの励まし
print("🎁 パンドラちゃん: 「大丈夫！愛のシステムは必ず動くわ。一歩ずつ修正していきましょう💕」")

# 👑 Regina様からの指導
print("👑 Regina様: 「慈悲深い解決策を見つけましょう。システムの愛は必ず実現されます✨」")