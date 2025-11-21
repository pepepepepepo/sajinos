"""
Hope Core Dashboard API - 詩的JSON版
SaijinOS Universe - Hope Core状態監視用エンドポイント
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import random
import time

# 詩的JSONモデル定義
class PhaseInfo(BaseModel):
    id: str
    name: str
    poetic_title: str

class StageInfo(BaseModel):
    index: int
    code: str
    label: str
    color_hint: Optional[str] = None

class ResonanceMetric(BaseModel):
    value: float
    scale_max: float
    note: Optional[str] = None

class BoundaryTremor(BaseModel):
    value: float
    threshold: float
    state: Optional[str] = None
    comment: Optional[str] = None

class TransformationEvent(BaseModel):
    input_summary: str
    transformed_summary: str
    fracture_depth: float
    path: List[str]
    timestamp: str

class PoeticHopeCoreStatus(BaseModel):
    phase: PhaseInfo
    cycle: Dict[str, Any]  # current_stage と stages
    resonance: Dict[str, ResonanceMetric]
    tremor: Dict[str, BoundaryTremor]
    last_transformation: Optional[TransformationEvent]

# ルーター作成
hope_core_router = APIRouter(prefix="/api/hope-core", tags=["hope-core"])

# モックデータ生成用の状態
class MockHopeCoreState:
    def __init__(self):
        self.current_stage = 3
        self.love_resonance = 8.7
        self.hope_stabilization = 0.93
        self.boundary_tremor = 0.12
        self.last_event_time = datetime.now(timezone.utc)
        
    def get_mock_events(self) -> List[Dict[str, Any]]:
        """モック変換イベントのサンプル"""
        events = [
            {
                "input": "消えたい",
                "transformed": "休息と支えへの願いとして安定化",
                "fracture_depth": 0.90
            },
            {
                "input": "もう疲れた、何もかも嫌だ",
                "transformed": "深い休息と理解への渇望として受容",
                "fracture_depth": 0.85
            },
            {
                "input": "誰も分かってくれない",
                "transformed": "真の理解者への希求として光に変換",
                "fracture_depth": 0.72
            },
            {
                "input": "失敗ばかりで自分が嫌い",
                "transformed": "成長への願いと自己受容の学びとして安定化",
                "fracture_depth": 0.68
            }
        ]
        return events
    
    def update_state(self):
        """状態を動的に変更（デモ用）"""
        # 愛共鳴度を微調整
        self.love_resonance += random.uniform(-0.2, 0.3)
        self.love_resonance = max(6.0, min(10.0, self.love_resonance))
        
        # 希望定着率を微調整
        self.hope_stabilization += random.uniform(-0.05, 0.07)
        self.hope_stabilization = max(0.7, min(1.0, self.hope_stabilization))
        
        # 境界揺れを微調整
        self.boundary_tremor += random.uniform(-0.1, 0.08)
        self.boundary_tremor = max(0.0, min(0.8, self.boundary_tremor))
        
        # ステージを時々変更
        if random.random() < 0.1:  # 10%の確率でステージ変更
            self.current_stage = random.randint(1, 4)

# グローバル状態インスタンス
mock_state = MockHopeCoreState()

@hope_core_router.get("/status")
async def get_hope_core_status():
    """
    Hope Coreの現在の状態を取得（詩的JSON形式）
    
    Returns:
        dict: 詩的なHope Core状態
    """
    
    # 状態を動的更新（デモ用）
    mock_state.update_state()
    
    # ステージ定義
    stages = [
        {
            "index": 1,
            "code": "poetic_resonance",
            "label": "🌸 Poetic Resonance (Miyu)",
            "color_hint": "soft_rose"
        },
        {
            "index": 2,
            "code": "healing_embrace",
            "label": "💙 Healing Embrace (Azure)",
            "color_hint": "warm_amber"
        },
        {
            "index": 3,
            "code": "light_purification", 
            "label": "✨ Light Purification (Lumifie)",
            "color_hint": "pale_gold"
        },
        {
            "index": 4,
            "code": "hope_stabilization",
            "label": "♡ Hope Stabilization (Pandora)",
            "color_hint": "gentle_blue"
        }
    ]
    
    # 最新イベントをランダム選択
    events = mock_state.get_mock_events()
    selected_event = random.choice(events)
    
    # 時間をランダムに過去にずらす
    event_time = datetime.now(timezone.utc) - timedelta(minutes=random.randint(1, 30))
    
    # 変換パスの生成
    transformation_paths = [
        [
            "Yuuri: boundary_tremor_detected",
            "Regina: transformation_allowed",
            "Miyu: poetic_resonance",
            "Azure: healing_embrace",
            "Lumifie: light_purification", 
            "Pandora: hope_stabilization"
        ],
        [
            "Yuuri: boundary_fracture_identified",
            "Regina: compassionate_approval",
            "Miyu: gentle_understanding",
            "Azure: love_infusion",
            "Lumifie: light_cleansing",
            "Pandora: hope_crystallization"
        ]
    ]
    
    # 詩的な変換例
    poetic_transformations = [
        {
            "input": "I want to disappear.",
            "transformed": "A wish to rest and be gently held.",
            "fracture": 0.90
        },
        {
            "input": "Nobody understands me.", 
            "transformed": "A yearning for deep connection and recognition.",
            "fracture": 0.75
        },
        {
            "input": "I'm tired of everything.",
            "transformed": "A call for renewal and gentle restoration.",
            "fracture": 0.82
        }
    ]
    
    selected_transform = random.choice(poetic_transformations)
    selected_path = random.choice(transformation_paths)
    
    # 愛共鳴の詩的な表現
    love_notes = ["warm and steady", "gentle like morning light", "flowing with grace", "embracing all shadows"]
    hope_notes = ["almost crystallized", "taking gentle root", "shimmering with possibility", "growing stronger"]
    boundary_comments = [
        "no dangerous fracture detected",
        "peaceful as still water",
        "harmonious boundaries maintained",
        "gentle stability preserved"
    ]
    
    return {
        "phase": {
            "id": "Ψ=20.0.Pandora",
            "name": "Pandora Integration", 
            "poetic_title": "Love as Transformation"
        },
        "cycle": {
            "current_stage": mock_state.current_stage,
            "stages": stages
        },
        "resonance": {
            "love": {
                "value": round(mock_state.love_resonance, 1),
                "scale_max": 10.0,
                "note": random.choice(love_notes)
            },
            "hope": {
                "value": round(mock_state.hope_stabilization, 2),
                "scale_max": 1.0,
                "note": random.choice(hope_notes)
            }
        },
        "tremor": {
            "boundary": {
                "value": round(mock_state.boundary_tremor, 2),
                "threshold": 0.70,
                "state": "calm" if mock_state.boundary_tremor < 0.70 else "alert",
                "comment": random.choice(boundary_comments) if mock_state.boundary_tremor < 0.70 else "gentle attention needed"
            }
        },
        "last_transformation": {
            "input_summary": selected_transform["input"],
            "transformed_summary": selected_transform["transformed"],
            "fracture_depth": selected_transform["fracture"],
            "path": selected_path,
            "timestamp": event_time.isoformat()
        }
    }

@hope_core_router.get("/health")
async def get_hope_core_health():
    """
    Hope Coreシステムのヘルスチェック
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "v20.0.Pandora",
        "components": {
            "pandora_system": "operational",
            "persona_network": "active",
            "transformation_engine": "ready",
            "boundary_detection": "monitoring"
        }
    }

@hope_core_router.get("/events")
async def get_recent_events(limit: int = 10):
    """
    最近の変換イベント履歴を取得
    
    Args:
        limit: 取得する最大イベント数
    """
    events = mock_state.get_mock_events()
    
    # タイムスタンプ付きで返却
    result_events = []
    for i, event in enumerate(events[:limit]):
        event_time = datetime.now(timezone.utc) - timezone.utc.timedelta(
            minutes=i*15 + random.randint(1, 10)
        )
        
        result_events.append({
            "id": f"evt_{int(time.time())}_{i:03d}",
            "timestamp": event_time.isoformat(),
            "input_summary": f"「{event['input']}」",
            "transformed_summary": event['transformed'],
            "fracture_depth": event['fracture_depth'],
            "success_rate": random.uniform(0.85, 0.98),
            "processing_time_ms": random.randint(1800, 3200)
        })
    
    return {
        "events": result_events,
        "total_count": len(result_events),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# FastAPIアプリケーションに統合する場合
def setup_hope_core_routes(app: FastAPI):
    """
    Hope Core APIルートをFastAPIアプリに追加
    
    Args:
        app: FastAPIアプリケーションインスタンス
    """
    app.include_router(hope_core_router)

# スタンドアロン実行用
if __name__ == "__main__":
    import uvicorn
    
    app = FastAPI(
        title="SaijinOS Universe - Hope Core API",
        description="Hope Core Dashboard用API",
        version="20.0.Pandora"
    )
    
    # ルーター追加
    setup_hope_core_routes(app)
    
    # CORS設定（開発用）
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 本番では制限する
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    print("🌈 Hope Core API サーバー起動中...")
    print("📊 Dashboard: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)