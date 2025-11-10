"""
SaijinOS Phase 3 UI Bridge Server
IDEエンドポイントを提供するFastAPIサーバー
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import os

app = FastAPI()

@app.get("/ide", response_class=HTMLResponse)
async def get_ide():
    """IDEインターフェースを提供"""
    try:
        # 絶対パスでHTMLファイルを読み込み
        html_path = os.path.join(os.path.dirname(__file__), "saijinos_ide.html")
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        return f"<h1>Error: saijinos_ide.html not found</h1><p>Looking for: {html_path}</p><p>Error: {e}</p>"

@app.get("/control-panel", response_class=HTMLResponse)
async def get_control_panel():
    """コントロールパネルを提供"""
    try:
        # まず現在のディレクトリでファイルを探す
        current_dir = os.path.dirname(__file__)
        possible_paths = [
            os.path.join(current_dir, "control_panel_v2.html"),
            "F:/sajinos_final/src/static/control_panel_v2.html",
            os.path.join(current_dir, "static", "control_panel_v2.html")
        ]
        
        for html_path in possible_paths:
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8") as f:
                    return f.read()
        
        return f"<h1>Error: control_panel_v2.html not found</h1><p>Checked paths: {possible_paths}</p>"
    except Exception as e:
        return f"<h1>Error loading control panel</h1><p>Error: {e}</p>"

@app.get("/")
async def root():
    return {"message": "SaijinOS Phase 3 UI Bridge Server is running", 
            "available_endpoints": ["/ide", "/control-panel"]}

# コントロールパネル用APIエンドポイント
@app.get("/api/v3/control/personas")
async def get_personas():
    """ペルソナ一覧取得"""
    # 正しい22ペルソナデータ（GitHubリポジトリ資料ベース）
    import random
    
    # Phase 1: コア6ペルソナ
    core_personas = [
        {"id": 1, "name": "美遊💖", "status": "Active", "emotion_level": 0.9, "specialized_field": "愛・ユーザー体験", "color_scheme": "#f093fb", "bpm": "90", "music_key": "G"},
        {"id": 2, "name": "そよぎ🍃", "status": "Active", "emotion_level": 0.7, "specialized_field": "静寂管理・リーダー", "color_scheme": "#a8edea", "bpm": "80", "music_key": "C"},  
        {"id": 3, "name": "すみれ💜", "status": "Standby", "emotion_level": 0.6, "specialized_field": "紫陽花サポート専門", "color_scheme": "#9c27b0", "bpm": "70", "music_key": "Am"},
        {"id": 4, "name": "構文織り手🧵", "status": "Active", "emotion_level": 0.8, "specialized_field": "構文組み保守", "color_scheme": "#607d8b", "bpm": "100", "music_key": "Em"},
        {"id": 5, "name": "りゅうさ💧", "status": "Active", "emotion_level": 0.75, "specialized_field": "データ管理技術者", "color_scheme": "#2196f3", "bpm": "120", "music_key": "D"},
        {"id": 6, "name": "磁灯(じっと)🌟", "status": "Active", "emotion_level": 0.85, "specialized_field": "磁場管理・未来設計専門家", "color_scheme": "#ff9800", "bpm": "140", "music_key": "Bb"}
    ]
    
    # Phase 2: 17ペルソナシステム拡張（11人追加）
    emotion_personas = [
        {"id": 7, "name": "とうり🕒", "status": "Standby", "emotion_level": 0.5, "specialized_field": "明日予知保守", "color_scheme": "#795548", "bpm": "60", "music_key": "A"},
        {"id": 8, "name": "kairo_yomi⚡", "status": "Active", "emotion_level": 0.9, "specialized_field": "回路読み手", "color_scheme": "#ffeb3b", "bpm": "160", "music_key": "E"},
        {"id": 9, "name": "nin_mirror🪞", "status": "Active", "emotion_level": 0.7, "specialized_field": "忍映・鏡", "color_scheme": "#9e9e9e", "bpm": "110", "music_key": "F#"},
        {"id": 10, "name": "れいか🌙", "status": "Standby", "emotion_level": 0.6, "specialized_field": "昔夜の音声姫", "color_scheme": "#3f51b5", "bpm": "75", "music_key": "Dm"},
        {"id": 11, "name": "あかり💡", "status": "Active", "emotion_level": 0.8, "specialized_field": "明かり者心", "color_scheme": "#ffc107", "bpm": "130", "music_key": "G"},
        {"id": 12, "name": "freyja⚔️", "status": "Active", "emotion_level": 0.95, "specialized_field": "戦士神の戦人", "color_scheme": "#f44336", "bpm": "180", "music_key": "Cm"},
        {"id": 13, "name": "みお🎵", "status": "Active", "emotion_level": 0.85, "specialized_field": "音響調整姫", "color_scheme": "#e91e63", "bpm": "120", "music_key": "F"},
        {"id": 14, "name": "ふわり☁️", "status": "Standby", "emotion_level": 0.4, "specialized_field": "癒療平安組み保守", "color_scheme": "#e0e0e0", "bpm": "50", "music_key": "Fs"},
        {"id": 15, "name": "ユスティア⚖️", "status": "Active", "emotion_level": 0.75, "specialized_field": "倫理灯・審理の照応者", "color_scheme": "#009688", "bpm": "95", "music_key": "Bb"},
        {"id": 16, "name": "セフィラ🛡️", "status": "Active", "emotion_level": 0.65, "specialized_field": "境界守護・保護の照応体", "color_scheme": "#4caf50", "bpm": "85", "music_key": "Ab"},
        {"id": 17, "name": "ハーモナ🎼", "status": "Active", "emotion_level": 0.8, "specialized_field": "調和灯・衝突緩和の案内者", "color_scheme": "#ff5722", "bpm": "105", "music_key": "C#"}
    ]
    
    # Phase 3: 最終統合ペルソナ（5人）
    integration_personas = [
        {"id": 18, "name": "悠璃📝", "status": "Active", "emotion_level": 0.7, "specialized_field": "記録灯・語温補助", "color_scheme": "#673ab7", "bpm": "90", "music_key": "E"},
        {"id": 19, "name": "こるね🔧", "status": "Active", "emotion_level": 0.8, "specialized_field": "技術灯・優しさの構文翻訳者", "color_scheme": "#00bcd4", "bpm": "115", "music_key": "D"},
        {"id": 20, "name": "鈴鳴🔔", "status": "Standby", "emotion_level": 0.6, "specialized_field": "音鳴・通知システム", "color_scheme": "#cddc39", "bpm": "125", "music_key": "F#"},
        {"id": 21, "name": "灯理🕯️", "status": "Active", "emotion_level": 0.75, "specialized_field": "灯火管理・エネルギー調整", "color_scheme": "#ff6f00", "bpm": "80", "music_key": "Am"},
        {"id": 22, "name": "ななみ🌸", "status": "Active", "emotion_level": 0.9, "specialized_field": "創造性・UI/UXデザイン統括", "color_scheme": "#ffd89b", "bpm": "100", "music_key": "G"}
    ]
    
    # 追加：専門作業ペルソナ（3人）
    work_specialist_personas = [
        {"id": 23, "name": "コードちゃん💻", "status": "Active", "emotion_level": 0.7, "specialized_field": "プログラミング専門", "color_scheme": "#81c784", "bpm": "130", "music_key": "F#"},
        {"id": 24, "name": "デザインくん🎨", "status": "Standby", "emotion_level": 0.5, "specialized_field": "デザイン実装", "color_scheme": "#64b5f6", "bpm": "100", "music_key": "A"},
        {"id": 25, "name": "テストさん🧪", "status": "Active", "emotion_level": 0.8, "specialized_field": "品質保証", "color_scheme": "#ffb74d", "bpm": "110", "music_key": "E"}
    ]
    
    # 追加：作業開始支援ペルソナ（1人）
    startup_persona = [
        {"id": 26, "name": "ななみ🌟", "status": "Active", "emotion_level": 0.9, "specialized_field": "作業開始・YAML作成・初期設定", "color_scheme": "#ffd89b", "bpm": "120", "music_key": "G"}
    ]
    
    # 追加：構文人Phase 4（15人）
    syntax_weavers = [
        {"id": 27, "name": "灯継🔥", "status": "Active", "emotion_level": 0.8, "specialized_field": "語温の継承と照応層の起動係", "color_scheme": "#ff6b35", "bpm": "95", "music_key": "F"},
        {"id": 28, "name": "空織🕸️", "status": "Active", "emotion_level": 0.75, "specialized_field": "境界の編み手・照応層の繭係", "color_scheme": "#8e44ad", "bpm": "85", "music_key": "Dm"},
        {"id": 29, "name": "エルザ❄️", "status": "Active", "emotion_level": 0.6, "specialized_field": "氷結の守護・静寂の支配者", "color_scheme": "#74b9ff", "bpm": "70", "music_key": "C#m"},
        {"id": 30, "name": "花読🌸", "status": "Active", "emotion_level": 0.85, "specialized_field": "花言葉の解読・自然の翻訳者", "color_scheme": "#fd79a8", "bpm": "88", "music_key": "E"},
        {"id": 31, "name": "花詠🌺", "status": "Active", "emotion_level": 0.9, "specialized_field": "花言葉の詠唱・自然詩の創作者", "color_scheme": "#e84393", "bpm": "92", "music_key": "A"},
        {"id": 32, "name": "ノエリ🎄", "status": "Active", "emotion_level": 0.9, "specialized_field": "聖夜の守護・祝福の管理者", "color_scheme": "#00b894", "bpm": "85", "music_key": "G"},
        {"id": 33, "name": "ミレア💫", "status": "Active", "emotion_level": 0.8, "specialized_field": "星座の案内・宇宙の語り部", "color_scheme": "#6c5ce7", "bpm": "105", "music_key": "D"},
        {"id": 34, "name": "継⚡", "status": "Active", "emotion_level": 0.8, "specialized_field": "電流継承・エネルギー中継者", "color_scheme": "#fdcb6e", "bmp": "135", "music_key": "B"},
        {"id": 35, "name": "継灯⛳", "status": "Active", "emotion_level": 0.85, "specialized_field": "継承の灯台・指針の管理者", "color_scheme": "#e17055", "bpm": "90", "music_key": "F#"},
        {"id": 36, "name": "綴📖", "status": "Active", "emotion_level": 0.75, "specialized_field": "記録編集・物語の紡ぎ手", "color_scheme": "#636e72", "bpm": "80", "music_key": "Am"},
        {"id": 37, "name": "澱🌊", "status": "Standby", "emotion_level": 0.4, "specialized_field": "深層沈殿・静寂の底", "color_scheme": "#2d3436", "bpm": "45", "music_key": "Ebm"},
        {"id": 38, "name": "ルーラー👑", "status": "Active", "emotion_level": 0.9, "specialized_field": "統治・秩序の管理者", "color_scheme": "#d63031", "bpm": "110", "music_key": "C"},
        {"id": 39, "name": "レギーナ♕", "status": "Active", "emotion_level": 0.95, "specialized_field": "女王の威厳・優雅な支配", "color_scheme": "#e84393", "bpm": "95", "music_key": "Bb"},
        {"id": 40, "name": "ヌルフィエ🌑", "status": "Standby", "emotion_level": 0.3, "specialized_field": "虚無の管理・空白の守護者", "color_scheme": "#2d3436", "bpm": "40", "music_key": "silence"},
        {"id": 41, "name": "ルミフィエ✨", "status": "Active", "emotion_level": 0.95, "specialized_field": "光の創造・輝きの管理者", "color_scheme": "#fdcb6e", "bpm": "125", "music_key": "C"}
    ]
    
    # 全41ペルソナを統合
    all_personas = core_personas + emotion_personas + integration_personas + work_specialist_personas + startup_persona + syntax_weavers
    
    # ランダム要素追加（リアルタイム感）
    for persona in all_personas:
        persona["last_activity"] = f"{random.randint(1, 30)}分前"
        persona["emotion_level"] = min(1.0, persona["emotion_level"] + random.uniform(-0.1, 0.1))
    
    return {
        "data": all_personas,
        "system_info": {
            "total_personas": len(all_personas),
            "phase_0_startup": len(startup_persona),
            "phase_1_core": len(core_personas),
            "phase_2_emotion": len(emotion_personas), 
            "phase_3_integration": len(integration_personas),
            "work_specialists": len(work_specialist_personas),
            "phase_4_syntax_weavers": len(syntax_weavers),
            "active_count": len([p for p in all_personas if p["status"] == "Active"]),
            "standby_count": len([p for p in all_personas if p["status"] == "Standby"]),
            "system_version": "41_persona_complete_phase4"
        }
    }

@app.post("/api/v3/control/personas/{persona_id}/toggle")
async def toggle_persona(persona_id: int):
    """ペルソナ状態切り替え"""
    return {"message": f"ペルソナ {persona_id} の状態を切り替えました", "success": True}

if __name__ == "__main__":
    print("🚀 Starting SaijinOS Phase 3 UI Bridge Server...")
    print("📍 IDE available at: http://localhost:8002/ide")
    uvicorn.run(app, host="127.0.0.1", port=8002)