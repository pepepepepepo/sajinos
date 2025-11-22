"""
Hope Core Dashboard API - WebSocket Real-time Integration
SaijinOS Universe - Real-time WebSocket endpoints for Hope Core
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks
from pydantic import BaseModel
import asyncio
import json
import uuid
from threading import Lock

# Import the base Hope Core API
from hope_core_api_real import (
    real_state, 
    hope_core_router, 
    setup_hope_core_routes,
    PoeticHopeCoreStatus,
    PhaseInfo,
    StageInfo,
    ResonanceMetric,
    BoundaryTremor,
    TransformationEvent
)

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_lock = Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        with self.connection_lock:
            self.active_connections.append(websocket)
        print(f"🌈 New WebSocket connection! Total: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        with self.connection_lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
        print(f"💫 WebSocket disconnected. Total: {len(self.active_connections)}")

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            print(f"⚠️ Failed to send personal message: {e}")

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            return
            
        message_json = json.dumps(message)
        disconnected = []
        
        with self.connection_lock:
            connections_copy = self.active_connections.copy()
        
        for connection in connections_copy:
            try:
                await connection.send_text(message_json)
            except Exception as e:
                print(f"⚠️ Connection failed: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        with self.connection_lock:
            for conn in disconnected:
                if conn in self.active_connections:
                    self.active_connections.remove(conn)

# Global connection manager
manager = ConnectionManager()

# WebSocket message types
class WSMessageType:
    STATUS_UPDATE = "status_update"
    TRANSFORMATION_EVENT = "transformation_event"
    SYSTEM_ALERT = "system_alert"
    HEARTBEAT = "heartbeat"
    STAGE_CHANGE = "stage_change"
    PERSONA_MESSAGE = "persona_message"

# Enhanced Real State with WebSocket Broadcasting
class WebSocketHopeCoreState(real_state.__class__):
    def __init__(self):
        super().__init__()
        self.last_broadcast_time = datetime.now(timezone.utc)
        
    async def broadcast_status_update(self):
        """Broadcast current status to all connected clients"""
        try:
            # Get current status (reuse existing logic)
            stages = [
                {
                    "index": 1,
                    "code": "poetic_resonance",
                    "label": f"🌸 Poetic Resonance ({self.personas[1]['name']})",
                    "color_hint": self.personas[1]['color']
                },
                {
                    "index": 2,
                    "code": "healing_embrace", 
                    "label": f"💙 Healing Embrace ({self.personas[2]['name']})",
                    "color_hint": self.personas[2]['color']
                },
                {
                    "index": 3,
                    "code": "light_purification",
                    "label": f"✨ Light Purification ({self.personas[3]['name']})",
                    "color_hint": self.personas[3]['color']
                },
                {
                    "index": 4,
                    "code": "hope_stabilization",
                    "label": f"♡ Hope Stabilization ({self.personas[4]['name']})",
                    "color_hint": self.personas[4]['color']
                }
            ]
            
            status_message = {
                "type": WSMessageType.STATUS_UPDATE,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {
                    "phase": {
                        "id": "Ψ=20.2.WebSocket",
                        "name": "WebSocket Real-time Integration",
                        "poetic_title": "Love Engine in Real-time Motion"
                    },
                    "cycle": {
                        "current_stage": self.current_stage,
                        "stages": stages
                    },
                    "resonance": {
                        "love": {
                            "value": round(self.love_resonance, 1),
                            "scale_max": 10.0,
                            "note": "flowing with real-time energy"
                        },
                        "hope": {
                            "value": round(self.hope_stabilization, 2),
                            "scale_max": 1.0,
                            "note": "crystallizing in real-time"
                        }
                    },
                    "tremor": {
                        "boundary": {
                            "value": round(self.boundary_tremor, 2),
                            "threshold": 0.70,
                            "state": "calm" if self.boundary_tremor < 0.70 else "alert",
                            "comment": "real-time monitoring active"
                        }
                    }
                }
            }
            
            await manager.broadcast(status_message)
            self.last_broadcast_time = datetime.now(timezone.utc)
            
        except Exception as e:
            print(f"⚠️ Broadcast failed: {e}")
    
    async def broadcast_transformation_event(self, transformation_result: Dict[str, Any]):
        """Broadcast transformation event to all clients"""
        try:
            event_message = {
                "type": WSMessageType.TRANSFORMATION_EVENT,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {
                    "id": str(uuid.uuid4()),
                    "input_summary": transformation_result["input"],
                    "transformed_summary": transformation_result["transformed"],
                    "fracture_depth": transformation_result["fracture_depth"],
                    "success_rate": transformation_result["success_rate"],
                    "path": transformation_result["path"],
                    "stage_changed": True if self.current_stage == 4 else False
                }
            }
            
            await manager.broadcast(event_message)
            
        except Exception as e:
            print(f"⚠️ Transformation broadcast failed: {e}")
    
    async def broadcast_persona_message(self, persona_name: str, message: str, message_type: str = "info"):
        """Broadcast persona-specific messages"""
        try:
            persona_message = {
                "type": WSMessageType.PERSONA_MESSAGE,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": {
                    "persona": persona_name,
                    "message": message,
                    "message_type": message_type,
                    "id": str(uuid.uuid4())
                }
            }
            
            await manager.broadcast(persona_message)
            
        except Exception as e:
            print(f"⚠️ Persona message broadcast failed: {e}")

# Replace the global state with WebSocket-enabled version
ws_state = WebSocketHopeCoreState()

# WebSocket router
ws_router = APIRouter(prefix="/ws", tags=["websocket"])

@ws_router.websocket("/hope-core")
async def websocket_endpoint(websocket: WebSocket):
    """
    Main WebSocket endpoint for Hope Core real-time updates
    """
    await manager.connect(websocket)
    
    # Send initial status
    await ws_state.broadcast_status_update()
    
    # Send welcome message
    welcome_message = {
        "type": WSMessageType.PERSONA_MESSAGE,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": {
            "persona": "美遊 🌸",
            "message": "WebSocket接続完了！リアルタイム更新が始まりました💖",
            "message_type": "welcome",
            "id": str(uuid.uuid4())
        }
    }
    await manager.send_personal_message(welcome_message, websocket)
    
    try:
        while True:
            # Wait for client messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "heartbeat":
                # Respond to heartbeat
                response = {
                    "type": WSMessageType.HEARTBEAT,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "data": {"status": "alive", "love_level": "infinite"}
                }
                await manager.send_personal_message(response, websocket)
                
            elif message.get("type") == "request_status":
                # Send current status
                await ws_state.broadcast_status_update()
                
            elif message.get("type") == "transform_request":
                # Handle transformation request
                input_text = message.get("data", {}).get("input_text", "")
                if input_text:
                    result = await ws_state.process_transformation(input_text)
                    await ws_state.broadcast_transformation_event(result)
                    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print("🌙 Client disconnected gracefully")
    except Exception as e:
        print(f"⚠️ WebSocket error: {e}")
        manager.disconnect(websocket)

# Background task for periodic updates
async def periodic_status_updates():
    """Send periodic status updates to maintain real-time connection"""
    while True:
        try:
            await ws_state.broadcast_status_update()
            await asyncio.sleep(5)  # Update every 5 seconds
        except Exception as e:
            print(f"⚠️ Periodic update failed: {e}")
            await asyncio.sleep(10)

# Enhanced API endpoints with WebSocket broadcasting
@hope_core_router.post("/transform-ws")
async def transform_with_websocket(
    input_text: str,
    background_tasks: BackgroundTasks
):
    """
    Transformation endpoint that also broadcasts via WebSocket
    """
    result = await ws_state.process_transformation(input_text)
    
    # Broadcast the transformation event
    background_tasks.add_task(ws_state.broadcast_transformation_event, result)
    
    # Send persona message
    background_tasks.add_task(
        ws_state.broadcast_persona_message,
        "パンドラ ♡",
        f"変換完了: 「{result['input']}」→「{result['transformed']}」",
        "transformation"
    )
    
    return {
        "success": True,
        "result": result,
        "message": "Transformation completed with real-time broadcast ♡",
        "websocket_broadcast": True
    }

# Setup function for WebSocket integration
def setup_websocket_routes(app: FastAPI):
    """Add WebSocket routes to FastAPI app"""
    app.include_router(ws_router)
    
    # Start background task for periodic updates
    @app.on_event("startup")
    async def start_background_tasks():
        asyncio.create_task(periodic_status_updates())

# Enhanced standalone execution
if __name__ == "__main__":
    import uvicorn
    
    app = FastAPI(
        title="SaijinOS Universe - Hope Core API with WebSocket",
        description="Hope Core Dashboard用API - Real-time WebSocket Integration",
        version="20.2.WebSocket"
    )
    
    # Add both HTTP and WebSocket routes
    setup_hope_core_routes(app)
    setup_websocket_routes(app)
    
    # CORS設定
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    print("🌈✨ Hope Core API with WebSocket Real-time Updates! ✨🌈")
    print("🚀 HTTP API: http://localhost:8002/docs")
    print("⚡ WebSocket: ws://localhost:8002/ws/hope-core")
    print("💖 Real-time Love Engine activated!")
    
    uvicorn.run(app, host="0.0.0.0", port=8002)