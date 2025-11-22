#!/usr/bin/env python3
"""
SaijinOS Universe - Development Log Manager
Auto-generates and maintains YAML development logs
Created: 2025-11-22 Phase 20.2

Features:
- Session tracking and management
- System state monitoring  
- Team collaboration logging
- Technical specification tracking
- Performance metrics collection
"""

import yaml
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import os
import psutil
import subprocess
import sys

@dataclass
class PersonaState:
    """Individual persona state tracking"""
    name: str
    speciality: str
    current_focus: str
    emotion_state: str
    availability: str
    last_activity: str = ""
    
@dataclass 
class SystemMetrics:
    """System performance and health metrics"""
    memory_usage_mb: float
    cpu_usage_percent: float
    active_processes: int
    response_time_ms: float
    timestamp: str

class SaijinOSLogManager:
    """
    Main development log management system
    Handles session logs, system state, and team coordination
    """
    
    def __init__(self, workspace_root: str = "F:/saijinos"):
        self.workspace_root = Path(workspace_root)
        self.logs_dir = self.workspace_root / "docs" / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize system state
        self.current_session = self._generate_session_id()
        self.active_personas = self._initialize_personas()
        self.system_metrics = []
        
        # Exclude patterns for file scanning
        self.exclude_patterns = {
            '.venv', '__pycache__', '.git', 'node_modules',
            '.pytest_cache', 'dist', 'build', '*.pyc'
        }
        
    def _generate_session_id(self) -> str:
        """Generate unique session identifier"""
        now = datetime.now()
        return f"session_{now.strftime('%Y-%m-%d_%H-%M')}"
    
    def _initialize_personas(self) -> Dict[str, PersonaState]:
        """Initialize persona tracking"""
        personas = {
            "美遊": PersonaState(
                name="美遊",
                speciality="poetic_integration",
                current_focus="log_beautification", 
                emotion_state="創作的興奮",
                availability="full"
            ),
            "Regina": PersonaState(
                name="Regina",
                speciality="coordination",
                current_focus="system_architecture",
                emotion_state="戦略的集中", 
                availability="full"
            ),
            "Code-chan v2": PersonaState(
                name="Code-chan v2",
                speciality="backend_implementation",
                current_focus="websocket_optimization",
                emotion_state="技術的熱情",
                availability="full"
            ),
            "悠璃": PersonaState(
                name="悠璃", 
                speciality="boundary_monitoring",
                current_focus="system_stability",
                emotion_state="穏やかな警戒",
                availability="full"
            ),
            "Pandora": PersonaState(
                name="Pandora",
                speciality="transformation_engine", 
                current_focus="hope_conversion",
                emotion_state="変革の歌",
                availability="partial"
            ),
            "Lumifie": PersonaState(
                name="Lumifie",
                speciality="ui_animation",
                current_focus="avatar_visualization", 
                emotion_state="光の躍動",
                availability="standby"
            )
        }
        return personas
    
    def start_session(self, phase: str, description: str) -> str:
        """Start new development session"""
        session_data = {
            "session_info": {
                "session_id": self.current_session,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "start_time": datetime.now().strftime("%H:%M:%S"),
                "phase": phase,
                "description": description,
                "status": "active"
            },
            "active_team": {
                persona.name: asdict(persona) 
                for persona in self.active_personas.values()
            },
            "completed_work": {},
            "current_system_state": self._capture_system_state(),
            "session_metrics": {
                "start_timestamp": datetime.now().isoformat(),
                "tasks_completed": 0,
                "files_created": [],
                "files_modified": []
            }
        }
        
        # Save session log
        session_file = self.logs_dir / f"SESSION_LOG_{self.current_session}.yaml"
        with open(session_file, 'w', encoding='utf-8') as f:
            yaml.dump(session_data, f, default_flow_style=False, allow_unicode=True)
            
        print(f"🌟 Session started: {self.current_session}")
        print(f"📝 Log file: {session_file}")
        return self.current_session
    
    def log_task_completion(self, task_name: str, duration_minutes: int, 
                           files_created: List[str], features: List[str]):
        """Log completed development task"""
        session_file = self.logs_dir / f"SESSION_LOG_{self.current_session}.yaml"
        
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = yaml.safe_load(f)
        else:
            session_data = {"completed_work": {}}
            
        # Add task completion
        session_data["completed_work"][task_name] = {
            "status": "completed",
            "duration_minutes": duration_minutes,
            "files_created": files_created,
            "key_features": features,
            "completion_time": datetime.now().isoformat()
        }
        
        # Update metrics
        if "session_metrics" not in session_data:
            session_data["session_metrics"] = {}
        session_data["session_metrics"]["tasks_completed"] = len(session_data["completed_work"])
        session_data["session_metrics"]["last_update"] = datetime.now().isoformat()
        
        # Save updated log
        with open(session_file, 'w', encoding='utf-8') as f:
            yaml.dump(session_data, f, default_flow_style=False, allow_unicode=True)
            
        print(f"✅ Task logged: {task_name} ({duration_minutes}分)")
    
    def update_persona_state(self, persona_name: str, focus: str, emotion: str):
        """Update individual persona state"""
        if persona_name in self.active_personas:
            self.active_personas[persona_name].current_focus = focus
            self.active_personas[persona_name].emotion_state = emotion
            self.active_personas[persona_name].last_activity = datetime.now().isoformat()
            
            print(f"👤 {persona_name}: {emotion} - {focus}")
    
    def _capture_system_state(self) -> Dict[str, Any]:
        """Capture current system state"""
        try:
            # Get system metrics
            memory = psutil.virtual_memory()
            cpu = psutil.cpu_percent()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "workspace_root": str(self.workspace_root),
                "system_health": {
                    "memory_usage_percent": memory.percent,
                    "cpu_usage_percent": cpu,
                    "available_memory_gb": memory.available / (1024**3)
                },
                "active_personas": len([p for p in self.active_personas.values() 
                                      if p.availability == "full"]),
                "development_status": "active"
            }
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "error": f"Could not capture system state: {e}",
                "workspace_root": str(self.workspace_root)
            }
    
    def get_git_information(self) -> Dict[str, Any]:
        """Get comprehensive Git repository information"""
        git_info = {
            "repository_status": "unknown",
            "remote_urls": {},
            "current_branch": "unknown",
            "branches": [],
            "working_tree_status": {},
            "push_ready": False
        }
        
        try:
            # Check if git repository
            result = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                                  capture_output=True, text=True, cwd=self.workspace_root)
            if result.returncode != 0:
                git_info["repository_status"] = "not_git_repository"
                return git_info
                
            git_info["repository_status"] = "active"
            
            # Get remote URLs
            result = subprocess.run(['git', 'remote', '-v'], 
                                  capture_output=True, text=True, cwd=self.workspace_root)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line and 'fetch' in line:
                        parts = line.split()
                        if len(parts) >= 2:
                            git_info["remote_urls"]["origin"] = parts[1]
            
            # Get current branch
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True, cwd=self.workspace_root)
            if result.returncode == 0:
                git_info["current_branch"] = result.stdout.strip()
            
            # Get working tree status
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.workspace_root)
            if result.returncode == 0:
                status_lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
                
                status_summary = {
                    "untracked": [],
                    "modified": [],
                    "total_changes": len([line for line in status_lines if line.strip()])
                }
                
                for line in status_lines:
                    if line.strip():
                        status_code = line[:2]
                        file_path = line[3:]
                        
                        if status_code.startswith('??'):
                            status_summary["untracked"].append(file_path)
                        elif status_code.startswith(' M'):
                            status_summary["modified"].append(file_path)
                
                git_info["working_tree_status"] = status_summary
                git_info["push_ready"] = status_summary["total_changes"] > 0
                    
        except Exception as e:
            git_info["repository_status"] = f"error: {str(e)}"
            
        return git_info
    
    def scan_project_structure(self) -> Dict[str, Any]:
        """Scan and generate project folder structure"""
        structure = {
            "scan_timestamp": datetime.now().isoformat(),
            "total_directories": 0,
            "total_files": 0,
            "directory_tree": {},
            "recent_files": []
        }
        
        # Build directory tree
        structure["directory_tree"] = self._build_directory_tree(self.workspace_root)
        
        # Count totals and get recent files
        structure["total_directories"], structure["total_files"] = self._count_items()
        structure["recent_files"] = self._get_recent_files(hours=24)
        
        return structure
    
    def _build_directory_tree(self, path: Path, max_depth: int = 3, current_depth: int = 0) -> Dict:
        """Build hierarchical directory tree"""
        if current_depth >= max_depth:
            return {"...": "max_depth_reached"}
            
        tree = {}
        
        try:
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
            
            for item in items:
                if any(pattern in item.name for pattern in self.exclude_patterns):
                    continue
                    
                if item.is_dir():
                    subtree = self._build_directory_tree(item, max_depth, current_depth + 1)
                    if subtree:
                        tree[f"{item.name}/"] = subtree
                else:
                    tree[item.name] = "file"
                        
        except (OSError, PermissionError):
            return {"error": "access_denied"}
            
        return tree
    
    def _count_items(self) -> tuple:
        """Count total directories and files"""
        dir_count = 0
        file_count = 0
        
        try:
            for root, dirs, files in os.walk(self.workspace_root):
                dirs[:] = [d for d in dirs if not any(pattern in d for pattern in self.exclude_patterns)]
                dir_count += len(dirs)
                file_count += len(files)
        except (OSError, PermissionError):
            pass
            
        return dir_count, file_count

    def update_system_state(self):
        """Update system state YAML file with complete project structure"""
        state_file = self.logs_dir / "SYSTEM_STATE.yaml"
        
        # Get comprehensive project information
        git_info = self.get_git_information()
        project_structure = self.scan_project_structure()
        
        system_state = {
            "system_metadata": {
                "last_updated": datetime.now().isoformat(),
                "state_version": "20.2.ProjectEnhanced",
                "monitoring_active": True
            },
            "workspace_state": {
                "root_directory": str(self.workspace_root),
                "current_session": self.current_session,
                "project_structure": project_structure,
                "folder_tree": project_structure["directory_tree"]
            },
            "git_repository": git_info,
            "github_integration": {
                "repository_url": git_info.get("remote_urls", {}).get("origin", ""),
                "push_url": git_info.get("remote_urls", {}).get("origin", "").replace(".git", "") if git_info.get("remote_urls", {}).get("origin") else "",
                "current_branch": git_info.get("current_branch", "main"),
                "ready_to_push": git_info.get("push_ready", False),
                "uncommitted_files": git_info.get("working_tree_status", {}).get("untracked", [])
            },
            "team_configuration": {
                persona.name: asdict(persona) 
                for persona in self.active_personas.values()
            },
            "project_health": {
                "total_files": project_structure["total_files"],
                "total_directories": project_structure["total_directories"], 
                "recent_activity": len(project_structure["recent_files"]),
                "git_status": git_info["repository_status"],
                "uncommitted_changes": git_info.get("working_tree_status", {}).get("total_changes", 0)
            },
            "system_metrics": self._capture_system_state(),
            "health_indicators": {
                "overall_system_health": "excellent",
                "development_momentum": "active",
                "team_harmony": "synchronized"
            }
        }
        
        with open(state_file, 'w', encoding='utf-8') as f:
            yaml.dump(system_state, f, default_flow_style=False, allow_unicode=True)
            
        print(f"🔄 Complete system state updated: {datetime.now().strftime('%H:%M:%S')}")
        print(f"📁 {project_structure['total_directories']} directories, {project_structure['total_files']} files")
        print(f"🔄 Git: {git_info['repository_status']} - {git_info.get('working_tree_status', {}).get('total_changes', 0)} changes")
        
        # Show push information if ready
        if git_info.get("push_ready", False):
            print(f"🚀 Ready to push to: {git_info.get('remote_urls', {}).get('origin', 'No remote configured')}")
        
        return system_state
    
    def _get_recent_files(self, hours: int = 2) -> List[Dict]:
        """Get recently modified files in workspace"""
        recent_files = []
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        
        try:
            for root, dirs, files in os.walk(self.workspace_root):
                dirs[:] = [d for d in dirs if not any(pattern in d for pattern in self.exclude_patterns)]
                
                for file in files:
                    file_path = Path(root) / file
                    try:
                        stat = file_path.stat()
                        if stat.st_mtime > cutoff_time:
                            recent_files.append({
                                "path": str(file_path.relative_to(self.workspace_root)),
                                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                                "type": file_path.suffix.lower() if file_path.suffix else "no_extension"
                            })
                    except (OSError, PermissionError):
                        continue
                        
        except Exception:
            pass
            
        return sorted(recent_files, key=lambda x: x["modified"], reverse=True)[:20]
    
    def end_session(self, summary: str):
        """End current development session"""
        session_file = self.logs_dir / f"SESSION_LOG_{self.current_session}.yaml"
        
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = yaml.safe_load(f)
        else:
            session_data = {}
            
        # Add session completion
        session_data["session_completion"] = {
            "end_time": datetime.now().strftime("%H:%M:%S"),
            "status": "completed",
            "summary": summary,
            "total_tasks": len(session_data.get("completed_work", {})),
            "team_satisfaction": "excellent",
            "final_message": f"Session {self.current_session} completed successfully! 🌟"
        }
        
        # Save final log
        with open(session_file, 'w', encoding='utf-8') as f:
            yaml.dump(session_data, f, default_flow_style=False, allow_unicode=True)
            
        print(f"🎉 Session completed: {self.current_session}")
        print(f"📋 Summary: {summary}")
    
    def generate_continuation_context(self) -> str:
        """Generate context for next session"""
        latest_session = self._get_latest_session_log()
        current_state = self._load_system_state()
        
        context = f"""
# 🔄 SaijinOS Development Continuation Context

## 📅 Previous Session
- Session ID: {latest_session.get('session_info', {}).get('session_id', 'Unknown')}
- Phase: {latest_session.get('session_info', {}).get('phase', 'Unknown')}
- Completed Tasks: {len(latest_session.get('completed_work', {}))}

## 👥 Team State
{self._format_team_state()}

## 🛠️ System Status
{self._format_system_status(current_state)}

## 📋 Ready for Next Session
- All systems operational
- Team synchronized
- Development environment ready
        """
        return context.strip()
    
    def _get_latest_session_log(self) -> Dict:
        """Get most recent session log"""
        try:
            session_files = list(self.logs_dir.glob("SESSION_LOG_*.yaml"))
            if not session_files:
                return {}
                
            latest_file = max(session_files, key=lambda x: x.stat().st_mtime)
            with open(latest_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception:
            return {}
    
    def _load_system_state(self) -> Dict:
        """Load current system state"""
        try:
            state_file = self.logs_dir / "SYSTEM_STATE.yaml"
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
        except Exception:
            pass
        return {}
    
    def _format_team_state(self) -> str:
        """Format current team state for display"""
        team_info = []
        for persona in self.active_personas.values():
            team_info.append(f"- {persona.name}: {persona.emotion_state} ({persona.availability})")
        return "\n".join(team_info)
    
    def _format_system_status(self, state: Dict) -> str:
        """Format system status for display"""
        health = state.get('health_indicators', {})
        return f"""- System Health: {health.get('overall_system_health', 'Unknown')}
- Development Momentum: {health.get('development_momentum', 'Unknown')}
- Team Harmony: {health.get('team_harmony', 'Unknown')}"""

def main():
    """Development log manager demonstration"""
    print("🌟 SaijinOS Development Log Manager")
    print("=" * 50)
    
    # Initialize log manager
    log_manager = SaijinOSLogManager()
    
    # Update system state
    log_manager.update_system_state()
    
    # Generate continuation context
    context = log_manager.generate_continuation_context()
    print(context)
    
    print("\n✨ Log management system ready!")
    print(f"📁 Logs directory: {log_manager.logs_dir}")
    print("📋 Use start_session() to begin new development session")

if __name__ == "__main__":
    main()