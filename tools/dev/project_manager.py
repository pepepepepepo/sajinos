#!/usr/bin/env python3
"""
SaijinOS Universe - Project Structure Manager
Auto-generates and maintains project folder structure documentation
Created: 2025-11-22 Phase 20.2 Enhancement

Features:
- Real-time folder structure generation
- Git repository information tracking
- Automatic structure updates
- GitHub integration monitoring
- Project health metrics
"""

import os
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess
import sys

class SaijinOSProjectManager:
    """
    Complete project structure and Git management system
    Tracks folder structure, Git state, and repository information
    """
    
    def __init__(self, workspace_root: str = "F:/saijinos"):
        self.workspace_root = Path(workspace_root)
        self.logs_dir = self.workspace_root / "docs" / "logs"
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Exclude patterns
        self.exclude_patterns = {
            '.venv', '__pycache__', '.git', 'node_modules',
            '.pytest_cache', 'dist', 'build', '*.pyc',
            'Lib', 'Scripts', 'Include', 'pyvenv.cfg'
        }
        
    def scan_project_structure(self) -> Dict[str, Any]:
        """Scan and generate complete project structure"""
        structure = {
            "scan_timestamp": datetime.now().isoformat(),
            "workspace_root": str(self.workspace_root),
            "total_directories": 0,
            "total_files": 0,
            "directory_tree": {},
            "file_inventory": {},
            "recent_files": []
        }
        
        # Build directory tree
        structure["directory_tree"] = self._build_directory_tree(self.workspace_root)
        
        # Count totals
        structure["total_directories"] = self._count_directories()
        structure["total_files"] = self._count_files()
        
        # File inventory by type
        structure["file_inventory"] = self._analyze_file_types()
        
        # Recent files (last 24 hours)
        structure["recent_files"] = self._get_recent_files()
        
        return structure
    
    def _build_directory_tree(self, path: Path, max_depth: int = 4, current_depth: int = 0) -> Dict:
        """Build hierarchical directory tree"""
        if current_depth >= max_depth:
            return {"...": "max_depth_reached"}
            
        tree = {}
        
        try:
            items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
            
            for item in items:
                # Skip excluded patterns
                if any(pattern in item.name for pattern in self.exclude_patterns):
                    continue
                    
                if item.is_dir():
                    subtree = self._build_directory_tree(item, max_depth, current_depth + 1)
                    if subtree:  # Only add if not empty
                        tree[f"{item.name}/"] = subtree
                else:
                    # Add file with metadata
                    try:
                        stat = item.stat()
                        tree[item.name] = {
                            "size_bytes": stat.st_size,
                            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            "type": item.suffix.lower() if item.suffix else "no_extension"
                        }
                    except (OSError, PermissionError):
                        tree[item.name] = {"error": "access_denied"}
                        
        except (OSError, PermissionError):
            return {"error": "access_denied"}
            
        return tree
    
    def _count_directories(self) -> int:
        """Count total directories"""
        count = 0
        try:
            for root, dirs, files in os.walk(self.workspace_root):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if not any(pattern in d for pattern in self.exclude_patterns)]
                count += len(dirs)
        except (OSError, PermissionError):
            pass
        return count
    
    def _count_files(self) -> int:
        """Count total files"""
        count = 0
        try:
            for root, dirs, files in os.walk(self.workspace_root):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if not any(pattern in d for pattern in self.exclude_patterns)]
                count += len(files)
        except (OSError, PermissionError):
            pass
        return count
    
    def _analyze_file_types(self) -> Dict[str, int]:
        """Analyze file types in project"""
        file_types = {}
        
        try:
            for root, dirs, files in os.walk(self.workspace_root):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if not any(pattern in d for pattern in self.exclude_patterns)]
                
                for file in files:
                    ext = Path(file).suffix.lower()
                    if not ext:
                        ext = "no_extension"
                    file_types[ext] = file_types.get(ext, 0) + 1
                    
        except (OSError, PermissionError):
            pass
            
        return dict(sorted(file_types.items(), key=lambda x: x[1], reverse=True))
    
    def _get_recent_files(self, hours: int = 24) -> List[Dict]:
        """Get recently modified files"""
        recent_files = []
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        
        try:
            for root, dirs, files in os.walk(self.workspace_root):
                # Filter out excluded directories
                dirs[:] = [d for d in dirs if not any(pattern in d for pattern in self.exclude_patterns)]
                
                for file in files:
                    file_path = Path(root) / file
                    try:
                        stat = file_path.stat()
                        if stat.st_mtime > cutoff_time:
                            recent_files.append({
                                "path": str(file_path.relative_to(self.workspace_root)),
                                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                                "size_bytes": stat.st_size,
                                "type": file_path.suffix.lower() if file_path.suffix else "no_extension"
                            })
                    except (OSError, PermissionError):
                        continue
                        
        except (OSError, PermissionError):
            pass
            
        return sorted(recent_files, key=lambda x: x["modified"], reverse=True)[:20]
    
    def get_git_information(self) -> Dict[str, Any]:
        """Get comprehensive Git repository information"""
        git_info = {
            "repository_status": "unknown",
            "remote_urls": {},
            "current_branch": "unknown",
            "branches": [],
            "commit_info": {},
            "working_tree_status": {},
            "upstream_info": {}
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
                    if line:
                        parts = line.split()
                        if len(parts) >= 2:
                            remote_name = parts[0]
                            remote_url = parts[1]
                            if remote_name not in git_info["remote_urls"]:
                                git_info["remote_urls"][remote_name] = remote_url
            
            # Get current branch
            result = subprocess.run(['git', 'branch', '--show-current'], 
                                  capture_output=True, text=True, cwd=self.workspace_root)
            if result.returncode == 0:
                git_info["current_branch"] = result.stdout.strip()
            
            # Get all branches
            result = subprocess.run(['git', 'branch', '-a'], 
                                  capture_output=True, text=True, cwd=self.workspace_root)
            if result.returncode == 0:
                branches = []
                for line in result.stdout.strip().split('\n'):
                    branch = line.strip().lstrip('* ').strip()
                    if branch and branch != '':
                        branches.append(branch)
                git_info["branches"] = branches
            
            # Get latest commit info
            result = subprocess.run(['git', 'log', '-1', '--pretty=format:%H|%an|%ae|%ad|%s'], 
                                  capture_output=True, text=True, cwd=self.workspace_root)
            if result.returncode == 0 and result.stdout:
                parts = result.stdout.split('|')
                if len(parts) >= 5:
                    git_info["commit_info"] = {
                        "hash": parts[0],
                        "author_name": parts[1],
                        "author_email": parts[2],
                        "date": parts[3],
                        "message": parts[4]
                    }
            
            # Get working tree status
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.workspace_root)
            if result.returncode == 0:
                status_lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
                
                status_summary = {
                    "untracked": [],
                    "modified": [],
                    "staged": [],
                    "deleted": [],
                    "total_changes": len(status_lines)
                }
                
                for line in status_lines:
                    if line:
                        status_code = line[:2]
                        file_path = line[3:]
                        
                        if status_code.startswith('??'):
                            status_summary["untracked"].append(file_path)
                        elif status_code.startswith(' M'):
                            status_summary["modified"].append(file_path)
                        elif status_code.startswith('M ') or status_code.startswith('A '):
                            status_summary["staged"].append(file_path)
                        elif status_code.startswith(' D'):
                            status_summary["deleted"].append(file_path)
                
                git_info["working_tree_status"] = status_summary
            
            # Get upstream tracking info
            result = subprocess.run(['git', 'status', '-b', '--porcelain'], 
                                  capture_output=True, text=True, cwd=self.workspace_root)
            if result.returncode == 0 and result.stdout:
                first_line = result.stdout.split('\n')[0]
                if 'ahead' in first_line or 'behind' in first_line:
                    git_info["upstream_info"]["tracking_status"] = first_line
                else:
                    git_info["upstream_info"]["tracking_status"] = "up_to_date"
                    
        except FileNotFoundError:
            git_info["repository_status"] = "git_not_installed"
        except Exception as e:
            git_info["repository_status"] = f"error: {str(e)}"
            
        return git_info
    
    def generate_comprehensive_state(self) -> Dict[str, Any]:
        """Generate comprehensive project and system state"""
        print("🔍 Scanning project structure...")
        project_structure = self.scan_project_structure()
        
        print("📡 Gathering Git information...")
        git_info = self.get_git_information()
        
        print("📊 Analyzing system metrics...")
        
        comprehensive_state = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "generator_version": "20.2.Enhanced",
                "workspace_root": str(self.workspace_root)
            },
            
            "project_structure": project_structure,
            "git_repository": git_info,
            
            "github_integration": {
                "repository_url": git_info.get("remote_urls", {}).get("origin", ""),
                "push_url": git_info.get("remote_urls", {}).get("origin", "").replace(".git", "") if git_info.get("remote_urls", {}).get("origin") else "",
                "current_branch": git_info.get("current_branch", "main"),
                "ready_to_push": len(git_info.get("working_tree_status", {}).get("untracked", [])) > 0
            },
            
            "development_environment": {
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "working_directory": str(self.workspace_root),
                "virtual_env": str(self.workspace_root / ".venv") if (self.workspace_root / ".venv").exists() else None
            },
            
            "project_health": {
                "total_files": project_structure["total_files"],
                "total_directories": project_structure["total_directories"],
                "recent_activity": len(project_structure["recent_files"]),
                "git_status": git_info["repository_status"],
                "uncommitted_changes": git_info.get("working_tree_status", {}).get("total_changes", 0)
            }
        }
        
        return comprehensive_state
    
    def update_system_state_with_structure(self):
        """Update SYSTEM_STATE.yaml with comprehensive project information"""
        comprehensive_state = self.generate_comprehensive_state()
        
        # Load existing system state
        state_file = self.logs_dir / "SYSTEM_STATE.yaml"
        existing_state = {}
        
        if state_file.exists():
            try:
                with open(state_file, 'r', encoding='utf-8') as f:
                    existing_state = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"⚠️ Could not load existing state: {e}")
        
        # Merge with existing state
        updated_state = existing_state.copy()
        
        # Update key sections
        updated_state["system_metadata"] = {
            **updated_state.get("system_metadata", {}),
            "last_updated": datetime.now().isoformat(),
            "state_version": "20.2.ProjectEnhanced",
            "monitoring_active": True
        }
        
        updated_state["workspace_state"] = {
            **updated_state.get("workspace_state", {}),
            "root_directory": str(self.workspace_root),
            "project_structure": comprehensive_state["project_structure"],
            "folder_tree": comprehensive_state["project_structure"]["directory_tree"]
        }
        
        updated_state["git_repository"] = comprehensive_state["git_repository"]
        updated_state["github_integration"] = comprehensive_state["github_integration"]
        updated_state["project_health"] = comprehensive_state["project_health"]
        updated_state["development_environment"] = comprehensive_state["development_environment"]
        
        # Save updated state
        with open(state_file, 'w', encoding='utf-8') as f:
            yaml.dump(updated_state, f, default_flow_style=False, allow_unicode=True)
            
        print(f"✅ System state updated with complete project structure")
        print(f"📁 {comprehensive_state['project_health']['total_directories']} directories")
        print(f"📄 {comprehensive_state['project_health']['total_files']} files")
        print(f"🔄 {comprehensive_state['project_health']['uncommitted_changes']} uncommitted changes")
        
        return comprehensive_state
    
    def generate_push_summary(self) -> str:
        """Generate summary for GitHub push"""
        git_info = self.get_git_information()
        
        untracked = git_info.get("working_tree_status", {}).get("untracked", [])
        modified = git_info.get("working_tree_status", {}).get("modified", [])
        staged = git_info.get("working_tree_status", {}).get("staged", [])
        
        summary = f"""
# 🚀 SaijinOS Phase 20.2 - Complete System Integration

## 📋 Changes Summary
- **New Files**: {len(untracked)} 
- **Modified**: {len(modified)}
- **Staged**: {len(staged)}

## 🌟 Major Features Added
- ⚡ WebSocket Real-time API (`tools/api/hope_core_api_websocket.py`)
- 🌸 Poetic Log Generator (`tools/api/poetic_log_generator.py`) 
- 👥 Persona Avatar Management (`tools/ui/persona_avatar_system.py`)
- 🌍 i18n Localization System (`tools/ui/localization_system.py`)
- 📊 Development Log Manager (`tools/dev/log_manager.py`)

## 🎯 Repository Information
- **URL**: {git_info.get("remote_urls", {}).get("origin", "Not configured")}
- **Branch**: {git_info.get("current_branch", "main")}
- **Ready to Push**: {"Yes" if len(untracked) > 0 else "No changes"}

## 🔧 Next Integration Steps
1. Flutter WebSocket Client Integration
2. Real-time Dashboard Updates  
3. Persona Avatar UI Display
4. Multi-language Support Activation
        """.strip()
        
        return summary

def main():
    """Project structure manager demonstration"""
    print("🌟 SaijinOS Project Structure Manager")
    print("=" * 60)
    
    # Initialize project manager
    project_manager = SaijinOSProjectManager()
    
    # Update system state with complete project information
    comprehensive_state = project_manager.update_system_state_with_structure()
    
    print("\n" + "=" * 60)
    print("📊 Project Health Summary")
    print("=" * 60)
    
    health = comprehensive_state["project_health"]
    github = comprehensive_state["github_integration"]
    
    print(f"📁 Total Directories: {health['total_directories']}")
    print(f"📄 Total Files: {health['total_files']}")
    print(f"⏰ Recent Activity: {health['recent_activity']} files")
    print(f"🔄 Git Status: {health['git_status']}")
    print(f"📝 Uncommitted Changes: {health['uncommitted_changes']}")
    
    print(f"\n🌐 GitHub Integration:")
    print(f"📡 Repository: {github['repository_url']}")
    print(f"🌿 Branch: {github['current_branch']}")
    print(f"🚀 Ready to Push: {github['ready_to_push']}")
    
    # Generate push summary
    if github['ready_to_push']:
        print("\n" + "="*60)
        print("🚀 PUSH SUMMARY")
        print("="*60)
        push_summary = project_manager.generate_push_summary()
        print(push_summary)
    
    print("\n✨ Project structure management system ready!")

if __name__ == "__main__":
    main()