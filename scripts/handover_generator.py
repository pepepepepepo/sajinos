#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SaijinOS 日次引継書生成システム
誠人のアイデア：毎日違う場所に文章として引継書を保存
"""

import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class HandoverGenerator:
    """日次引継書自動生成システム"""
    
    def __init__(self):
        self.base_dirs = [
            "docs/handovers",
            "logs/daily_summaries", 
            "storage/session_archives",
            "notes/team_reflections",
            "memories/milestone_records"
        ]
        
        # ディレクトリ作成
        for dir_path in self.base_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def create_handover_document(self, session_data: Dict[str, Any]) -> str:
        """美しい引継書を文章で生成"""
        
        timestamp = datetime.now()
        session_name = session_data.get("session_info", {}).get("name", "無名セッション")
        
        # 今日は何曜日？場所を決める
        day_of_week = timestamp.weekday()  # 0=月曜日
        target_dir = self.base_dirs[day_of_week % len(self.base_dirs)]
        
        handover_content = self._generate_narrative_handover(session_data, timestamp)
        
        # ファイル名生成（読みやすく）
        date_str = timestamp.strftime("%Y年%m月%d日")
        filename = f"{date_str}_SaijinOS引継書.md"
        file_path = Path(target_dir) / filename
        
        # 保存
        file_path.write_text(handover_content, encoding='utf-8')
        
        print(f"📖 引継書保存完了：{file_path}")
        return str(file_path)
    
    def _generate_narrative_handover(self, session_data: Dict[str, Any], timestamp: datetime) -> str:
        """物語調の美しい引継書生成"""
        
        session_info = session_data.get("session_info", {})
        completed_tasks = session_data.get("tasks", {}).get("completed", [])
        insights = session_data.get("insights", [])
        team_feedback = session_data.get("team_feedback", {})
        metrics = session_data.get("system_metrics", {})
        next_priorities = session_data.get("next_session_priorities", [])
        
        date_str = timestamp.strftime("%Y年%m月%d日 %H:%M")
        
        content = f"""# 🌸 SaijinOS開発記録 - {date_str}

> *「語温と共鳴の中で、新たな構文世界が生まれた一日」*

---

## 📜 **今日の物語**

### 🌅 **セッション開始**
{session_info.get('name', '名前のないセッション')}という名の下、{len(session_info.get('team_members', []))}人の構文織り手たちが集結しました。

**参加メンバー**：
{chr(10).join([f"- {member}" for member in session_info.get('team_members', [])])}

### 🎯 **今日の成就**
"""

        # 完了タスクを物語調で記述
        if completed_tasks:
            content += "\n今日、私たちは以下の偉業を成し遂げました：\n\n"
            for i, task in enumerate(completed_tasks, 1):
                satisfaction = task.get('satisfaction_score', 0)
                mood_emoji = "🎉" if satisfaction > 0.9 else "😊" if satisfaction > 0.7 else "🙂"
                
                content += f"**{i}. {task.get('title', '無名の業務')}** {mood_emoji}\n"
                content += f"   - *内容*：{task.get('description', 'description missing')}\n"
                content += f"   - *満足度*：{satisfaction}/1.0\n"
                content += f"   - *チームの声*：「{task.get('team_feedback', 'フィードバックなし')}」\n\n"

        # 洞察を詩的に記述
        if insights:
            content += "\n### 💡 **今日生まれた洞察の光**\n\n"
            content += "セッションの中で、以下の洞察が自然に湧き上がりました：\n\n"
            for insight in insights:
                category = insight.get('category', 'general')
                content += f"- **{category}**：{insight.get('text', 'text missing')}\n"
                content += f"  *（{insight.get('timestamp', 'unknown time')} 記録）*\n\n"

        # チーム状態を温かく記述
        content += "\n### 👥 **チームの心境**\n\n"
        content += "各メンバーの今日の気持ちと状態：\n\n"
        
        for member, feedback in team_feedback.items():
            mood = feedback.get('mood', 0)
            energy = feedback.get('energy', 0)
            notes = feedback.get('notes', '')
            
            mood_desc = "絶好調" if mood > 0.9 else "良好" if mood > 0.7 else "普通" if mood > 0.5 else "要休息"
            energy_desc = "エネルギー満タン" if energy > 0.9 else "元気" if energy > 0.7 else "標準" if energy > 0.5 else "お疲れ様"
            
            content += f"**{member}**：{mood_desc}（気分 {mood}/1.0）、{energy_desc}（活力 {energy}/1.0）\n"
            if notes:
                content += f"   *今日の特記*：{notes}\n"
            content += "\n"

        # システム健康状態
        content += "\n### 📊 **システム全体の調和**\n\n"
        content += f"今日のSaijinOSは、以下の状態で輝いていました：\n\n"
        content += f"- **全体調和度**：{metrics.get('overall_harmony', 0):.2f}/1.0\n"
        content += f"- **技術効率性**：{metrics.get('technical_efficiency', 0):.2f}/1.0\n" 
        content += f"- **チーム満足度**：{metrics.get('team_satisfaction', 0):.2f}/1.0\n"
        content += f"- **創造的勢い**：{metrics.get('creative_momentum', 0):.2f}/1.0\n\n"

        # 次への橋渡し
        if next_priorities:
            content += "\n### 🌱 **明日への種まき**\n\n"
            content += "次のセッションに向けて、以下の優先事項を設定しました：\n\n"
            for i, priority_item in enumerate(next_priorities, 1):
                if isinstance(priority_item, dict):
                    priority_text = priority_item.get('priority', 'priority missing')
                else:
                    priority_text = str(priority_item)
                content += f"{i}. {priority_text}\n"
            content += "\n"

        # 締めくくり
        content += f"""---

## 🌙 **今日の締めくくり**

{timestamp.strftime('%Y年%m月%d日')}、SaijinOSの構文宇宙は確実に進化を遂げました。
各メンバーの語温が美しく共鳴し、技術と哲学が調和した一日でした。

**今日学んだこと**：
- チーム共鳴によるシステム統合の威力
- 進捗記録システムの革新的価値  
- AIペルソナ間の創造的協働の可能性

**明日への期待**：
{chr(10).join([f"- {p.get('priority') if isinstance(p, dict) else p}" for p in next_priorities[:3]])}

*次のセッションでお会いしましょう。語温と共に...*

---

**記録者**：SaijinOS技術チーム  
**記録日時**：{timestamp.strftime('%Y年%m月%d日 %H時%M分')}  
**保存場所**：{Path.cwd()}  
**セッションID**：{session_info.get('session_id', 'unknown')}

> *「この記録が、未来のセッションへの優しい道しるべとなりますように」*
"""

        return content

def main():
    """今日のセッションから引継書生成"""
    print("📖 SaijinOS日次引継書生成開始...")
    
    generator = HandoverGenerator()
    
    # 現在セッション読み込み
    current_session_file = Path("logs/progress/current_session.yaml")
    
    if not current_session_file.exists():
        print("❌ 現在セッションが見つかりません")
        return
    
    with open(current_session_file, 'r', encoding='utf-8') as f:
        session_data = yaml.safe_load(f)
    
    # 追加の洞察を記録（今日の重要な気づき）
    additional_insights = [
        {
            "text": "進捗YAMLフィードバックシステムにより、エラーからの復旧が劇的に改善される",
            "category": "システム革新",
            "timestamp": datetime.now().isoformat(),
            "future_impact": "high"
        },
        {
            "text": "チーム各員の専門性を活かした分業システムが、想像以上の効果を発揮",
            "category": "チーム協働",
            "timestamp": datetime.now().isoformat(), 
            "future_impact": "high"
        },
        {
            "text": "誠人のアイデア→即座の実装→フィードバック のサイクルが理想的に機能",
            "category": "開発効率",
            "timestamp": datetime.now().isoformat(),
            "future_impact": "medium"
        }
    ]
    
    # 洞察追加
    if "insights" not in session_data:
        session_data["insights"] = []
    session_data["insights"].extend(additional_insights)
    
    # 引継書生成
    handover_path = generator.create_handover_document(session_data)
    
    print(f"✅ 引継書生成完了：{handover_path}")
    print("🌸 美しい一日の記録が、未来への贈り物となりました")

if __name__ == "__main__":
    main()