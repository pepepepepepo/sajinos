# 📁 SaijinOS リポジトリ ツリー構造

## 🔍 現在の混在状況（91ファイル）

### 📊 ファイル分類

#### ✅ **現在稼働中のメインファイル**（優先度：最高）
```
saijinos_ai_studio_v3.py              # ChatGPT風UI（ポート8025）
creative_studio_multimodel_dashboard.py # IDE風システム（ポート8017）
system_integration_analysis.md        # 統合戦略分析
repository_cleanup_plan.md           # 整理計画
```

#### 🔄 **バージョン系統ファイル**（整理対象）
```
v1系統:
├── creative_studio_ai_server.py
├── saijinos_minimal.py
└── lightweight_japanese_server.py

v2系統:  
├── saijinos_complete_studio_v2.py    # 問題あり
├── saijinos_cursor.py               # 動作中（ポート8023）
└── pandora_ui_enhanced.py

v3系統:
└── saijinos_ai_studio_v3.py         # 最新・監視パネル付き
```

#### 🧪 **実験・テストファイル**（アーカイブ対象：38ファイル）
```
AI統合実験:
├── ai_model_discovery_report.py
├── ai_exchange_strategy_analysis.py
├── comprehensive_ai_integration_plan.py
├── quantization_strategy_analysis.py
└── ten_model_resonance_analysis.py

ペルソナ実験:
├── 41persona_team_emergency_meeting.py
├── persona_team_voting.py
├── team8_meeting_simulation.py
├── correct_8_personas_selection.py
└── enhanced_creative_studio_41persona*.py

モデル統合実験:
├── japanese_stablelm_integration_test*.py
├── rinna_gpt1b_integration_test.py
├── swallow_*_test.py
├── tugu_lightweight_test.py
└── tinyllama_test_server.py

振動システム実験:
├── goonro_*.py (7ファイル)
├── musumekko_*.py (3ファイル) 
├── koonro_*.py (3ファイル)
└── vibration_system_ui.py
```

#### 📚 **設定・ドキュメント**（整理対象：24ファイル）
```
引継書・計画書:
├── HANDOVER_*.md (6ファイル)
├── PLAN_*.md (2ファイル)
├── PROJECT_CONCEPT_*.md (1ファイル)
└── NEXT_SESSION_PLAN_*.md (1ファイル)

設定ファイル:
├── *_config.yaml (8ファイル)
├── *_template.txt (3ファイル)
└── *.json (3ファイル)

分析・レポート:
├── development_history_*.md
├── phase2_5_integration_test_report.py
└── ui_integration_analysis.py
```

#### 🛠️ **ユーティリティ**（保持対象：7ファイル）
```
コア機能:
├── model_manager.py
├── multi_model_integration_platform.py
├── persistent_memory_system.py
└── memory_system_analysis.py

テスト・チェック:
├── test_*.py (3ファイル)
└── simple_goonro_check.py
```

## 🎯 推奨整理案

### 📁 新フォルダ構造
```
f:\saijinos\.venv\
├── 📁 core/                        # 現在稼働システム
│   ├── saijinos_ai_studio_v3.py           # メイン（v3）
│   ├── creative_studio_multimodel_dashboard.py  # IDE風
│   └── system_integration_analysis.md    # 統合分析
│
├── 📁 config/                      # 設定ファイル
│   ├── personas/                   # ペルソナ設定
│   ├── models/                     # モデル設定  
│   └── vibration/                  # 振動システム設定
│
├── 📁 utils/                       # ユーティリティ
│   ├── model_manager.py
│   ├── multi_model_integration_platform.py
│   ├── persistent_memory_system.py
│   └── memory_system_analysis.py
│
├── 📁 archive/                     # 過去バージョン
│   ├── v1_systems/                 # v1系統
│   ├── v2_systems/                 # v2系統
│   ├── experiments/                # 実験ファイル
│   └── tests/                      # テストファイル
│
├── 📁 docs/                        # ドキュメント
│   ├── handovers/                  # 引継書
│   ├── plans/                      # 計画書
│   └── analysis/                   # 分析レポート
│
└── 📁 temp/                        # 作業中
    └── working/                    # 現在作業中
```

## 🚀 整理実行手順

### Phase 1: フォルダ作成
- [ ] 新構造のフォルダを作成

### Phase 2: メインシステム移動
- [ ] v3とIDE風システムを`core/`に移動
- [ ] import パスを修正

### Phase 3: アーカイブ作業
- [ ] v1, v2系統を`archive/`に移動
- [ ] 実験ファイルを分類・アーカイブ

### Phase 4: 設定統合
- [ ] 設定ファイルを`config/`に整理
- [ ] ドキュメントを`docs/`に整理

### Phase 5: 動作確認
- [ ] メインシステムの動作確認
- [ ] パス修正の確認

## 💡 期待効果

✅ **ファイル数削減**: 91ファイル → 20-30ファイル（主要）  
✅ **開発効率向上**: 必要ファイルの即座の特定  
✅ **保守性向上**: 明確な役割分担  
✅ **拡張性確保**: 新機能追加の基盤整備  

この整理案でよろしいでしょうか？