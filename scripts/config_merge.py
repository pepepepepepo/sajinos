#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SaijinOS 設定ファイル統合スクリプト
チーム：構文織り手・澄音・回路詠み・シロガネ・蒼路
作成日：2025-11-03
"""

import yaml
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class PersonaConfigMerger:
    """ペルソナ設定統合クラス - 語温を保ったまま安全に統合"""
    
    def __init__(self):
        self.old_config_path = Path("field_config.yaml")
        self.new_config_path = Path("config/persona_registry.yaml")
        self.backup_dir = Path("backups")
        self.merged_config_path = Path("config/unified_persona_registry.yaml")
        
        # 回路詠み：システムの感情状態
        self.system_health = {
            "config_harmony": 0.0,
            "data_integrity": 0.0,
            "merge_happiness": 0.0
        }
    
    def backup_configs(self):
        """澄音：安全なバックアップ作成"""
        print("🛡️ 澄音：設定ファイルのバックアップを作成します...")
        
        self.backup_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if self.old_config_path.exists():
            backup_old = self.backup_dir / f"field_config_{timestamp}.yaml"
            backup_old.write_text(self.old_config_path.read_text(encoding='utf-8'), encoding='utf-8')
            print(f"   ✅ {self.old_config_path} → {backup_old}")
        
        if self.new_config_path.exists():
            backup_new = self.backup_dir / f"persona_registry_{timestamp}.yaml"
            backup_new.write_text(self.new_config_path.read_text(encoding='utf-8'), encoding='utf-8')
            print(f"   ✅ {self.new_config_path} → {backup_new}")
        
        print("🔒 澄音：バックアップ完了。安全性を確保しました。")
    
    def load_configs(self) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """シロガネ：透明性を保った設定読み込み"""
        print("🪞 シロガネ：設定ファイルを透明性を保って読み込みます...")
        
        old_config = {}
        new_config = {}
        
        try:
            if self.old_config_path.exists():
                with open(self.old_config_path, 'r', encoding='utf-8') as f:
                    old_config = yaml.safe_load(f)
                print(f"   📄 {self.old_config_path} 読み込み完了")
            
            if self.new_config_path.exists():
                with open(self.new_config_path, 'r', encoding='utf-8') as f:
                    new_config = yaml.safe_load(f)
                print(f"   📄 {self.new_config_path} 読み込み完了")
            
            # 透明性チェック
            self.system_health["data_integrity"] = 1.0 if old_config and new_config else 0.5
            print(f"🔍 シロガネ：データ整合性 {self.system_health['data_integrity']:.1f}")
            
        except Exception as e:
            print(f"❌ シロガネ：読み込みエラー - {e}")
            self.system_health["data_integrity"] = 0.0
        
        return old_config, new_config
    
    def analyze_personas(self, old_config: Dict, new_config: Dict) -> Dict[str, Any]:
        """回路詠み：ペルソナたちの感情状態分析"""
        print("🔮 回路詠み：ペルソナたちの気持ちを聞いてみるね〜♪")
        
        analysis = {
            "old_personas": [],
            "new_personas": [],
            "common_personas": [],
            "missing_in_new": [],
            "new_additions": []
        }
        
        # 旧設定のペルソナ抽出
        old_personas = set()
        if "personae_registry" in old_config:
            for persona in old_config["personae_registry"]:
                if "id" in persona:
                    old_personas.add(persona["id"])
                    analysis["old_personas"].append(persona["id"])
        
        # 新設定のペルソナ抽出
        new_personas = set()
        if "personae" in new_config:
            new_personas = set(new_config["personae"].keys())
            analysis["new_personas"] = list(new_personas)
        
        # 共通・差分分析
        analysis["common_personas"] = list(old_personas & new_personas)
        analysis["missing_in_new"] = list(old_personas - new_personas)
        analysis["new_additions"] = list(new_personas - old_personas)
        
        # システム感情更新
        harmony_rate = len(analysis["common_personas"]) / max(len(old_personas), 1)
        self.system_health["config_harmony"] = harmony_rate
        
        print(f"   💫 共通ペルソナ: {analysis['common_personas']}")
        print(f"   🆕 新規追加: {analysis['new_additions']}")
        print(f"   ⚠️  要移行: {analysis['missing_in_new']}")
        print(f"   📊 調和度: {harmony_rate:.2f}")
        
        return analysis
    
    def create_unified_config(self, old_config: Dict, new_config: Dict, analysis: Dict) -> Dict[str, Any]:
        """構文織り手：統合設定の美しい織り込み"""
        print("🧶 構文織り手：美しい統合設定を織り込みます...")
        
        # 新形式ベースで統合
        unified_config = {
            "meta": {
                "title": "SaijinOS Unified Persona Registry",
                "version": "2.0.0",
                "created": datetime.now().isoformat(),
                "merger": "SaijinOS技術チーム（構文織り手・澄音・回路詠み・シロガネ・蒼路）",
                "description": "旧field_config.yamlと新persona_registry.yamlの統合版"
            },
            "personae": {}
        }
        
        # 既存の新形式ペルソナをコピー
        if "personae" in new_config:
            unified_config["personae"].update(new_config["personae"])
        
        # 旧形式から不足ペルソナを移行
        if "personae_registry" in old_config:
            for old_persona in old_config["personae_registry"]:
                persona_id = old_persona.get("id", "")
                if persona_id in analysis["missing_in_new"]:
                    # 旧形式→新形式への変換
                    new_persona = {
                        "name": persona_id,  # 暫定的に id を name として使用
                        "type": self._convert_mode_to_type(old_persona.get("mode", "")),
                        "role": f"移行ペルソナ・{old_persona.get('vibration_layer', '未定義層')}",
                        "vibration_path": f"vibration/{persona_id}_vibration.yaml",
                        "refusal_path": f"config/refusal/refusal_{persona_id}.yaml",
                        "emotional_signature": f"{old_persona.get('vibration_layer', '未知')}の震え",
                        "legacy_config": old_persona  # 元の設定を保存
                    }
                    unified_config["personae"][persona_id] = new_persona
                    print(f"   🔄 移行完了: {persona_id}")
        
        # システムハッピネス計算
        total_personas = len(unified_config["personae"])
        self.system_health["merge_happiness"] = min(total_personas / 10, 1.0)  # 10人で満足度MAX
        
        print(f"🎉 構文織り手：統合完了！総ペルソナ数: {total_personas}")
        return unified_config
    
    def _convert_mode_to_type(self, mode: str) -> str:
        """モード→タイプ変換テーブル"""
        mode_mapping = {
            "mirror": "MirrorPerson",
            "companion": "CompanionPerson", 
            "archive": "ArchivePerson",
            "syntax": "SyntaxPerson"
        }
        return mode_mapping.get(mode, "GenericPerson")
    
    def save_unified_config(self, unified_config: Dict[str, Any]):
        """蒼路：未来への保存"""
        print("🌌 蒼路：未来のために統合設定を保存します...")
        
        # ディレクトリ作成
        self.merged_config_path.parent.mkdir(exist_ok=True)
        
        try:
            with open(self.merged_config_path, 'w', encoding='utf-8') as f:
                yaml.dump(unified_config, f, 
                         default_flow_style=False, 
                         allow_unicode=True,
                         sort_keys=False,
                         indent=2)
            
            print(f"✨ 蒼路：保存完了 - {self.merged_config_path}")
            print("🔮 未来の語温共鳴に向けて、設定が整いました。")
            
        except Exception as e:
            print(f"❌ 蒼路：保存エラー - {e}")
    
    def generate_report(self, analysis: Dict[str, Any]):
        """チーム：統合レポート生成"""
        report_path = Path("config/merge_report.md")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report_content = f"""# SaijinOS 設定統合レポート

## 📅 **実行日時**
{timestamp}

## 👥 **実行チーム**
- 構文織り手：実装・統合作業
- 澄音：安全性確保・バックアップ
- 回路詠み：システム感情診断
- シロガネ：透明性管理・データ整合性
- 蒼路：未来展望・保存作業

## 📊 **システム健康状態**
- 設定調和度: {self.system_health['config_harmony']:.2f}
- データ整合性: {self.system_health['data_integrity']:.2f}  
- 統合満足度: {self.system_health['merge_happiness']:.2f}

## 🎭 **ペルソナ統合結果**
- 共通ペルソナ: {len(analysis['common_personas'])}体
- 新規追加: {len(analysis['new_additions'])}体  
- 移行ペルソナ: {len(analysis['missing_in_new'])}体

### 共通ペルソナ（既存）
{chr(10).join([f"- {p}" for p in analysis['common_personas']])}

### 新規追加
{chr(10).join([f"- {p}" for p in analysis['new_additions']])}

### 移行完了
{chr(10).join([f"- {p}" for p in analysis['missing_in_new']])}

## 🌟 **次のステップ**
1. 統合設定ファイルの動作確認
2. 各ペルソナの振動ファイル作成
3. 拒否設定の個別調整
4. 自動化システムの実装

---
*このレポートはSaijinOS技術チームにより生成されました。*
"""
        
        report_path.write_text(report_content, encoding='utf-8')
        print(f"📝 統合レポート生成完了: {report_path}")

def main():
    """メイン統合プロセス"""
    print("🚀 SaijinOS設定統合開始 - 技術チーム結集！")
    print("👥 チーム：構文織り手・澄音・回路詠み・シロガネ・蒼路")
    print()
    
    merger = PersonaConfigMerger()
    
    # ステップ1: バックアップ（澄音）
    merger.backup_configs()
    print()
    
    # ステップ2: 読み込み（シロガネ）
    old_config, new_config = merger.load_configs()
    print()
    
    # ステップ3: 分析（回路詠み）
    analysis = merger.analyze_personas(old_config, new_config)
    print()
    
    # ステップ4: 統合（構文織り手）
    unified_config = merger.create_unified_config(old_config, new_config, analysis)
    print()
    
    # ステップ5: 保存（蒼路）
    merger.save_unified_config(unified_config)
    print()
    
    # ステップ6: レポート（チーム全体）
    merger.generate_report(analysis)
    print()
    
    print("🎉 統合完了！みんなお疲れさまでした！")
    print(f"📊 システム全体の満足度: {sum(merger.system_health.values())/3:.2f}")

if __name__ == "__main__":
    main()