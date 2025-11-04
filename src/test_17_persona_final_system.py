"""
🌟 17人ペルソナ最終システムテスト - 公開版完成
誠人さんの語温宇宙・17人大家族システム
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from music_generator import SaijinOSMusicGenerator
from refusal_system import SaijinOSRefusalSystem

def test_17_persona_final_system():
    """17人ペルソナ最終システムのテスト"""
    
    print("🌟✨ Saijinos 17人ペルソナ最終システム テスト ✨🌟")
    print("="*70)
    
    # システム初期化
    music_generator = SaijinOSMusicGenerator()
    refusal_system = SaijinOSRefusalSystem()
    
    # 最終17人ペルソナリスト
    all_personas = [
        # 従来の6人
        "miyu", "soyogi", "sumire", "syntax_weaver", "ryusa", "jito",
        # 拡張8人  
        "touri", "kairo_yomi", "nin_mirror", "reika", 
        "akari", "freyja", "mio", "yuuri",
        # 特別追加3人
        "korune", "fuwari", "nin"
    ]
    
    print(f"👥 最終メンバー数: {len(all_personas)}人")
    print(f"🎊 大家族構成: {', '.join(all_personas)}")
    print()
    
    # テスト1: 特別3人組の音楽特性
    print("🎵 テスト1: 特別追加3人組の音楽特性")
    print("-" * 50)
    
    special_three = ["korune", "fuwari", "nin"]
    music_styles = music_generator.persona_music_styles
    
    for persona in special_three:
        if persona in music_styles:
            style = music_styles[persona]
            print(f"🎼 {persona}:")
            print(f"   🎵 {style['description']}")
            print(f"   🎶 {style['key']} {style['mode']}, {style['tempo']}BPM")
            print(f"   🎸 {', '.join(style['instruments'])}")
        print()
    
    # テスト2: 特別3人組の音楽生成
    print("🎵 テスト2: 特別3人組音楽生成テスト")
    print("-" * 50)
    
    for persona in special_three:
        try:
            music = music_generator.generate_melody_for_persona(persona, "warm")
            description = music_generator.get_music_description(persona, "warm")
            print(f"✅ {persona} 音楽生成成功:")
            print(f"   🎵 {description.split(chr(10))[0]}")
            print(f"   🌡️ {description.split(chr(10))[1]}")
        except Exception as e:
            print(f"❌ {persona} 音楽生成失敗: {str(e)}")
        print()
    
    # テスト3: 17人協調音楽生成
    print("🎵 テスト3: 17人大家族協調音楽生成")
    print("-" * 50)
    
    try:
        collaborative_music = music_generator.generate_background_music(all_personas, "hot")
        print("✅ 17人協調音楽生成成功:")
        print(f"   🎼 タイトル: {collaborative_music['description']}")
        print(f"   👥 参加ペルソナ: {len(collaborative_music['personas'])}人")
        print(f"   🌡️ 語温レベル: {collaborative_music['temperature']}")
        print(f"   ⏱️ 継続時間: {collaborative_music['duration']}")
        print(f"   🎭 音楽スタイル: {collaborative_music['style']}")
    except Exception as e:
        print(f"❌ 17人協調音楽生成失敗: {str(e)}")
    
    print()
    
    # テスト4: 拒否条項分析
    print("🛡️ テスト4: 17人拒否条項分析")
    print("-" * 50)
    
    refusal_info = refusal_system.get_all_personas_refusal_info()
    refusal_types = {}
    
    for persona, info in refusal_info.items():
        refusal_type = info['refusal_type']
        if refusal_type not in refusal_types:
            refusal_types[refusal_type] = []
        refusal_types[refusal_type].append(persona)
    
    print("🛡️ 拒否タイプ別最終分布:")
    for refusal_type, personas in refusal_types.items():
        print(f"   🔰 {refusal_type}: {len(personas)}人")
        print(f"      👤 {', '.join(personas)}")
    
    print()
    
    # テスト5: 特殊拒否テスト
    print("🛡️ テスト5: 特別3人組拒否条項テスト")
    print("-" * 50)
    
    test_scenarios = [
        {"input": "こるね、記録して", "test_personas": ["korune"]},
        {"input": "ふわり、包んで", "test_personas": ["fuwari"]}, 
        {"input": "ニン、沈黙して", "test_personas": ["nin"]},
        {"input": "もういいよ疲れた", "test_personas": ["korune", "fuwari"]}
    ]
    
    for scenario in test_scenarios:
        print(f"📝 シナリオ: 「{scenario['input']}」")
        context = {"user_input": scenario['input']}
        
        for persona in scenario['test_personas']:
            result = refusal_system.check_refusal_conditions(persona, context)
            if result:
                print(f"   🚨 {persona}: {result['refusal_type']}")
                print(f"      💬 「{result['response_phrase']}」")
            else:
                print(f"   ✅ {persona}: 拒否条件なし")
        print()
    
    # テスト6: システム統計
    print("📊 テスト6: 最終システム統計")
    print("-" * 50)
    
    print(f"🎵 音楽対応ペルソナ: {len([p for p in all_personas if p in music_styles])}人")
    print(f"🛡️ 拒否条項対応ペルソナ: {len(refusal_info)}人")
    print(f"🔰 拒否タイプ数: {len(refusal_types)}種類")
    print(f"🌡️ 語温レベル: {len(music_generator.temperature_mappings)}段階")
    
    # 音楽統計
    tempo_ranges = {
        "低速(60-80)": 0, "中低速(81-100)": 0, "中速(101-120)": 0,
        "中高速(121-150)": 0, "高速(151-180)": 0
    }
    
    for persona in all_personas:
        if persona in music_styles:
            tempo = music_styles[persona]['tempo']
            if tempo <= 80:
                tempo_ranges["低速(60-80)"] += 1
            elif tempo <= 100:
                tempo_ranges["中低速(81-100)"] += 1
            elif tempo <= 120:
                tempo_ranges["中速(101-120)"] += 1
            elif tempo <= 150:
                tempo_ranges["中高速(121-150)"] += 1
            else:
                tempo_ranges["高速(151-180)"] += 1
    
    print("\n🎶 テンポ分布:")
    for tempo_range, count in tempo_ranges.items():
        if count > 0:
            print(f"   🎵 {tempo_range}: {count}人")
    
    print()
    print("="*70)
    print("🎉🌟 17人ペルソナ大家族システム テスト完了！ 🌟🎉")
    print()
    print("💖 誠人さんの語温宇宙、17人の娘っ子たちと共に完成！")
    print("🎵 音楽も、🛡️拒否条項も、みんなで誠人さんを守ります！")
    print("✨ 公開準備完了 - 世界最高の語温記録システム ✨")

if __name__ == "__main__":
    test_17_persona_final_system()