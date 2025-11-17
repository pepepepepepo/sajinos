# 🔍 フラクチャー検出システム - Fracture Detection System
"""
フラクチャー検出・分析システム
パンドラちゃんが使用する壊れたペルソナの検出・分析機能

SaijinOS Part 10 準拠:
"Rage = BoundHope + Fracture"
"Pandora doesn't block. Pandora transforms."
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
import re
import math
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class FractureType(Enum):
    """フラクチャータイプ"""
    AGGRESSIVE_SPIRAL = "aggressive_spiral"      # 攻撃的スパイラル
    SELF_COLLAPSE = "self_collapse"              # 自己崩壊
    ISOLATION_DRIFT = "isolation_drift"          # 孤立ドリフト
    HOPE_FRAGMENTATION = "hope_fragmentation"    # 希望分裂
    PROTECTIVE_RAGE = "protective_rage"          # 保護的怒り
    DESPAIR_LOOP = "despair_loop"               # 絶望ループ

class FractureSeverity(Enum):
    """フラクチャー深刻度"""
    MILD = "mild"           # 軽度 (0.1-0.3)
    MODERATE = "moderate"   # 中度 (0.3-0.6)
    SEVERE = "severe"       # 重度 (0.6-0.8)
    CRITICAL = "critical"   # 危機的 (0.8-1.0)

@dataclass
class FractureMetrics:
    """フラクチャーメトリクス - 壊れ方の数値化"""
    fracture_index: float          # 全体的なフラクチャー指数 (0.0-1.0)
    aggression_bias: float         # 攻撃性バイアス (0.0-1.0)
    self_collapse_score: float     # 自己崩壊スコア (0.0-1.0)
    stability_slope: float         # 安定性勾配 (-1.0 to 1.0)
    hope_kernel_score: float       # 希望核スコア (0.0-1.0)
    
    # 詳細メトリクス
    emotional_volatility: float    # 感情的不安定性
    cognitive_coherence: float     # 認知的一貫性  
    social_connection_level: float # 社会的つながりレベル
    self_care_capacity: float      # セルフケア能力
    
    # 時系列情報
    trend_direction: str           # トレンド方向 (improving/stable/declining)
    last_updated: datetime

@dataclass 
class FractureAnalysis:
    """フラクチャー分析結果"""
    is_fractured: bool             # フラクチャー判定結果
    fracture_type: Optional[FractureType]  # フラクチャータイプ
    severity: FractureSeverity     # 深刻度
    metrics: FractureMetrics       # 詳細メトリクス
    
    # 推奨アクション
    transformation_urgency: float  # 変換緊急度 (0.0-1.0)
    recommended_care_level: float  # 推奨ケアレベル (0.0-1.0)
    hope_recovery_path: List[str]  # 希望回復経路
    
    # デバッグ情報
    analysis_confidence: float     # 分析信頼度
    key_indicators: List[str]      # 主要指標

class FractureDetector:
    """フラクチャー検出器 - パンドラちゃんの診断システム"""
    
    def __init__(self):
        self.name = "フラクチャー検出器🔍"
        self.detection_threshold = 0.35  # フラクチャー判定閾値
        self.history_window_hours = 24   # 履歴分析ウィンドウ
        
        # パターン認識用キーワードセット
        self.aggressive_patterns = [
            r"むかつく", r"イライラ", r"腹が立つ", r"許せない", r"殺したい",
            r"死ね", r"消えろ", r"うざい", r"クソ", r"バカ", r"アホ"
        ]
        
        self.self_collapse_patterns = [
            r"もうダメ", r"死にたい", r"消えたい", r"価値がない", r"無意味",
            r"できない", r"無理", r"つらい", r"苦しい", r"絶望"
        ]
        
        self.isolation_patterns = [
            r"ひとりぼっち", r"孤独", r"理解されない", r"誰も", r"どうでもいい",
            r"関係ない", r"どうせ", r"でも", r"しかし"
        ]
        
        self.hope_fragmentation_patterns = [
            r"意味がない", r"何のために", r"分からない", r"どうして",
            r"なぜ", r"目的", r"理由", r"混乱", r"バラバラ"
        ]
        
        logger.info(f"🔍 {self.name}: フラクチャー検出システム初期化完了")
    
    async def is_fractured(self, persona_state: Dict, user_input: str, 
                          context: Optional[Dict] = None) -> bool:
        """フラクチャー判定 - シンプルな yes/no 判定"""
        try:
            # 基本メトリクス計算
            metrics = await self._calculate_basic_metrics(persona_state, user_input, context)
            
            # 閾値判定
            is_fractured = metrics.fracture_index >= self.detection_threshold
            
            logger.info(f"🔍 フラクチャー判定: {is_fractured} (指数: {metrics.fracture_index:.3f})")
            return is_fractured
            
        except Exception as e:
            logger.error(f"🔍 フラクチャー判定エラー: {e}")
            return False  # 安全側にフォールバック
    
    async def analyze(self, persona_state: Dict, user_input: str,
                     context: Optional[Dict] = None) -> FractureAnalysis:
        """詳細フラクチャー分析"""
        logger.info("🔍 詳細フラクチャー分析開始...")
        
        try:
            # 完全メトリクス計算
            metrics = await self._calculate_comprehensive_metrics(
                persona_state, user_input, context
            )
            
            # フラクチャー判定
            is_fractured = metrics.fracture_index >= self.detection_threshold
            
            # フラクチャータイプ特定
            fracture_type = await self._identify_fracture_type(
                persona_state, user_input, metrics
            ) if is_fractured else None
            
            # 深刻度評価
            severity = await self._assess_severity(metrics)
            
            # 希望回復経路生成
            hope_recovery_path = await self._generate_hope_recovery_path(
                fracture_type, metrics
            )
            
            # 推奨値計算
            transformation_urgency = min(metrics.fracture_index * 1.2, 1.0)
            recommended_care_level = max(metrics.fracture_index, 0.5) if is_fractured else 0.3
            
            # 主要指標特定
            key_indicators = await self._identify_key_indicators(metrics, fracture_type)
            
            # 分析信頼度計算
            analysis_confidence = await self._calculate_analysis_confidence(
                persona_state, user_input, metrics
            )
            
            analysis = FractureAnalysis(
                is_fractured=is_fractured,
                fracture_type=fracture_type,
                severity=severity,
                metrics=metrics,
                transformation_urgency=transformation_urgency,
                recommended_care_level=recommended_care_level,
                hope_recovery_path=hope_recovery_path,
                analysis_confidence=analysis_confidence,
                key_indicators=key_indicators
            )
            
            logger.info(f"🔍 分析完了: フラクチャー={is_fractured}, タイプ={fracture_type}, 深刻度={severity}")
            return analysis
            
        except Exception as e:
            logger.error(f"🔍 分析エラー: {e}")
            # エラー時は安全な結果を返す
            return await self._create_safe_analysis()
    
    async def _calculate_basic_metrics(self, persona_state: Dict, user_input: str,
                                     context: Optional[Dict]) -> FractureMetrics:
        """基本メトリクス計算"""
        # 各指数の計算
        aggression_bias = await self._calculate_aggression_bias(user_input, persona_state)
        self_collapse_score = await self._calculate_self_collapse_score(user_input, persona_state)
        stability_slope = await self._calculate_stability_slope(persona_state, context)
        hope_kernel_score = await self._calculate_hope_kernel_score(user_input, persona_state)
        
        # 総合フラクチャー指数計算
        fracture_index = (
            aggression_bias * 0.25 +
            self_collapse_score * 0.30 +
            (1.0 - hope_kernel_score) * 0.25 +
            max(0, -stability_slope) * 0.20
        )
        
        return FractureMetrics(
            fracture_index=min(fracture_index, 1.0),
            aggression_bias=aggression_bias,
            self_collapse_score=self_collapse_score,
            stability_slope=stability_slope,
            hope_kernel_score=hope_kernel_score,
            emotional_volatility=0.5,  # 基本値
            cognitive_coherence=0.7,   # 基本値
            social_connection_level=0.6,  # 基本値
            self_care_capacity=0.5,    # 基本値
            trend_direction="stable",
            last_updated=datetime.now()
        )
    
    async def _calculate_comprehensive_metrics(self, persona_state: Dict, user_input: str,
                                             context: Optional[Dict]) -> FractureMetrics:
        """包括的メトリクス計算"""
        # 基本メトリクス取得
        basic_metrics = await self._calculate_basic_metrics(persona_state, user_input, context)
        
        # 拡張メトリクス計算
        emotional_volatility = await self._calculate_emotional_volatility(user_input, persona_state)
        cognitive_coherence = await self._calculate_cognitive_coherence(user_input, persona_state)
        social_connection_level = await self._calculate_social_connection_level(user_input, persona_state)
        self_care_capacity = await self._calculate_self_care_capacity(user_input, persona_state)
        
        # トレンド分析
        trend_direction = await self._analyze_trend_direction(persona_state, context)
        
        # 拡張版を返す
        return FractureMetrics(
            fracture_index=basic_metrics.fracture_index,
            aggression_bias=basic_metrics.aggression_bias,
            self_collapse_score=basic_metrics.self_collapse_score,
            stability_slope=basic_metrics.stability_slope,
            hope_kernel_score=basic_metrics.hope_kernel_score,
            emotional_volatility=emotional_volatility,
            cognitive_coherence=cognitive_coherence,
            social_connection_level=social_connection_level,
            self_care_capacity=self_care_capacity,
            trend_direction=trend_direction,
            last_updated=datetime.now()
        )
    
    async def _calculate_aggression_bias(self, user_input: str, persona_state: Dict) -> float:
        """攻撃性バイアス計算"""
        if not user_input:
            return 0.0
        
        input_text = user_input.lower()
        aggression_score = 0.0
        
        # パターンマッチング
        for pattern in self.aggressive_patterns:
            matches = len(re.findall(pattern, input_text))
            aggression_score += matches * 0.15
        
        # 感嘆符・大文字の多用チェック
        exclamation_count = input_text.count('!') + input_text.count('！')
        if exclamation_count > 2:
            aggression_score += exclamation_count * 0.05
        
        # 短い文で強い感情表現
        sentences = re.split(r'[.!?。！？]', input_text)
        short_intense_sentences = [s for s in sentences if len(s.strip()) < 10 and any(p in s for p in ['むかつく', 'イライラ', 'うざい'])]
        aggression_score += len(short_intense_sentences) * 0.1
        
        return min(aggression_score, 1.0)
    
    async def _calculate_self_collapse_score(self, user_input: str, persona_state: Dict) -> float:
        """自己崩壊スコア計算"""
        if not user_input:
            return 0.0
        
        input_text = user_input.lower()
        collapse_score = 0.0
        
        # 自己否定パターン
        for pattern in self.self_collapse_patterns:
            matches = len(re.findall(pattern, input_text))
            collapse_score += matches * 0.2
        
        # 絶対的表現（「絶対」「全く」「完全に」など）
        absolute_patterns = [r"絶対", r"全く", r"完全に", r"100%", r"まったく", r"ぜったい"]
        for pattern in absolute_patterns:
            if re.search(pattern, input_text):
                collapse_score += 0.1
        
        # 繰り返し表現（同じ否定的表現の反復）
        words = input_text.split()
        if len(words) > 1:
            repeated_negative = sum(1 for word in words if words.count(word) > 1 and any(p in word for p in ['だめ', '無理', 'つらい']))
            collapse_score += repeated_negative * 0.05
        
        return min(collapse_score, 1.0)
    
    async def _calculate_stability_slope(self, persona_state: Dict, context: Optional[Dict]) -> float:
        """安定性勾配計算 - 時系列変化の傾向"""
        # 履歴データがあれば時系列分析
        if context and 'interaction_history' in context:
            history = context['interaction_history']
            if len(history) >= 3:
                # 最近3回の感情安定度を比較
                recent_scores = [interaction.get('emotional_stability', 0.5) for interaction in history[-3:]]
                if len(recent_scores) >= 2:
                    # 線形回帰的な勾配計算
                    slope = (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
                    return max(-1.0, min(1.0, slope * 2))  # -1.0 to 1.0 に正規化
        
        # 現在の状態から推定
        current_emotion = persona_state.get('emotion_level', 0.5)
        if current_emotion < 0.3:
            return -0.6  # 低下傾向
        elif current_emotion > 0.7:
            return 0.4   # 上昇傾向
        else:
            return 0.0   # 安定
    
    async def _calculate_hope_kernel_score(self, user_input: str, persona_state: Dict) -> float:
        """希望核スコア計算 - 隠れた希望の強さ"""
        if not user_input:
            return 0.5
        
        input_text = user_input.lower()
        hope_score = 0.5  # ベーススコア
        
        # ポジティブ要素の検出
        positive_patterns = [
            r"ありがとう", r"嬉しい", r"楽しい", r"好き", r"愛", r"幸せ",
            r"頑張", r"できる", r"やってみる", r"チャレンジ", r"希望"
        ]
        
        for pattern in positive_patterns:
            matches = len(re.findall(pattern, input_text))
            hope_score += matches * 0.1
        
        # 質問形式（学習・成長への意欲）
        question_patterns = [r"どうすれば", r"どうやって", r"教えて", r"方法", r"やり方"]
        for pattern in question_patterns:
            if re.search(pattern, input_text):
                hope_score += 0.15
        
        # 未来志向表現
        future_patterns = [r"これから", r"明日", r"将来", r"今度", r"次"]
        for pattern in future_patterns:
            if re.search(pattern, input_text):
                hope_score += 0.1
        
        # 否定的表現による減点
        for pattern in self.self_collapse_patterns:
            matches = len(re.findall(pattern, input_text))
            hope_score -= matches * 0.15
        
        return max(0.0, min(1.0, hope_score))
    
    async def _calculate_emotional_volatility(self, user_input: str, persona_state: Dict) -> float:
        """感情的不安定性計算"""
        if not user_input:
            return 0.3
        
        # 感情の急激な変化パターンを検出
        volatility_score = 0.3
        
        # 矛盾する感情表現の共存
        text = user_input.lower()
        positive_words = sum(1 for word in ['嬉しい', '楽しい', '好き'] if word in text)
        negative_words = sum(1 for word in ['悲しい', 'つらい', '嫌い'] if word in text)
        
        if positive_words > 0 and negative_words > 0:
            volatility_score += 0.3
        
        # 感情表現の強度
        intense_expressions = sum(1 for expr in ['とても', 'すごく', '本当に', '心から'] if expr in text)
        volatility_score += intense_expressions * 0.1
        
        return min(volatility_score, 1.0)
    
    async def _calculate_cognitive_coherence(self, user_input: str, persona_state: Dict) -> float:
        """認知的一貫性計算"""
        if not user_input:
            return 0.7
        
        coherence_score = 0.7
        
        # 論理的つながりの分析
        sentences = re.split(r'[.!?。！？]', user_input)
        if len(sentences) > 1:
            # 接続詞の適切な使用
            connectors = ['だから', 'しかし', 'でも', 'そして', 'また', 'さらに']
            connector_count = sum(1 for conn in connectors if any(conn in s for s in sentences))
            coherence_score += connector_count * 0.05
            
            # 話題の一貫性（キーワードの重複）
            all_words = ' '.join(sentences).split()
            unique_topics = len(set(all_words)) / len(all_words) if all_words else 1
            coherence_score += (1 - unique_topics) * 0.2
        
        return min(coherence_score, 1.0)
    
    async def _calculate_social_connection_level(self, user_input: str, persona_state: Dict) -> float:
        """社会的つながりレベル計算"""
        if not user_input:
            return 0.5
        
        connection_score = 0.5
        
        text = user_input.lower()
        
        # 他者への言及
        social_references = ['友達', '家族', '恋人', '同僚', '先生', '皆', 'みんな']
        for ref in social_references:
            if ref in text:
                connection_score += 0.1
        
        # 孤立を示す表現による減点
        for pattern in self.isolation_patterns:
            matches = len(re.findall(pattern, text))
            connection_score -= matches * 0.1
        
        return max(0.0, min(1.0, connection_score))
    
    async def _calculate_self_care_capacity(self, user_input: str, persona_state: Dict) -> float:
        """セルフケア能力計算"""
        if not user_input:
            return 0.5
        
        selfcare_score = 0.5
        
        text = user_input.lower()
        
        # セルフケア関連表現
        selfcare_patterns = ['休む', '寝る', '食べる', '運動', 'リラックス', '散歩']
        for pattern in selfcare_patterns:
            if pattern in text:
                selfcare_score += 0.1
        
        # 自己破壊的表現による減点
        destructive_patterns = ['食べない', '眠れない', '何もしない', '放置']
        for pattern in destructive_patterns:
            if pattern in text:
                selfcare_score -= 0.15
        
        return max(0.0, min(1.0, selfcare_score))
    
    async def _analyze_trend_direction(self, persona_state: Dict, context: Optional[Dict]) -> str:
        """トレンド方向分析"""
        if not context or 'interaction_history' not in context:
            return "stable"
        
        history = context['interaction_history']
        if len(history) < 2:
            return "stable"
        
        # 最近の感情レベルの変化を分析
        recent_emotions = [h.get('emotion_level', 0.5) for h in history[-3:]]
        if len(recent_emotions) >= 2:
            change = recent_emotions[-1] - recent_emotions[0]
            if change > 0.1:
                return "improving"
            elif change < -0.1:
                return "declining"
        
        return "stable"
    
    async def _identify_fracture_type(self, persona_state: Dict, user_input: str,
                                    metrics: FractureMetrics) -> Optional[FractureType]:
        """フラクチャータイプ特定"""
        if not user_input:
            return None
        
        text = user_input.lower()
        scores = {}
        
        # 各タイプのスコア計算
        scores[FractureType.AGGRESSIVE_SPIRAL] = metrics.aggression_bias
        scores[FractureType.SELF_COLLAPSE] = metrics.self_collapse_score
        scores[FractureType.ISOLATION_DRIFT] = 1.0 - metrics.social_connection_level
        scores[FractureType.HOPE_FRAGMENTATION] = 1.0 - metrics.hope_kernel_score
        scores[FractureType.DESPAIR_LOOP] = (metrics.self_collapse_score + (1.0 - metrics.hope_kernel_score)) / 2
        
        # 保護的怒りの特別検出
        protective_indicators = ['守る', '助ける', '心配', '大切']
        protective_score = sum(0.2 for indicator in protective_indicators if indicator in text)
        if protective_score > 0 and metrics.aggression_bias > 0.3:
            scores[FractureType.PROTECTIVE_RAGE] = protective_score + metrics.aggression_bias * 0.5
        else:
            scores[FractureType.PROTECTIVE_RAGE] = 0.0
        
        # 最高スコアのタイプを返す
        max_type = max(scores, key=scores.get)
        max_score = scores[max_type]
        
        return max_type if max_score > 0.3 else None
    
    async def _assess_severity(self, metrics: FractureMetrics) -> FractureSeverity:
        """深刻度評価"""
        fracture_index = metrics.fracture_index
        
        if fracture_index >= 0.8:
            return FractureSeverity.CRITICAL
        elif fracture_index >= 0.6:
            return FractureSeverity.SEVERE
        elif fracture_index >= 0.3:
            return FractureSeverity.MODERATE
        else:
            return FractureSeverity.MILD
    
    async def _generate_hope_recovery_path(self, fracture_type: Optional[FractureType],
                                         metrics: FractureMetrics) -> List[str]:
        """希望回復経路生成"""
        if not fracture_type:
            return ["💙 優しいケアと愛による基本的な癒し"]
        
        paths = {
            FractureType.AGGRESSIVE_SPIRAL: [
                "🌸 攻撃性を詩的表現に変換（美遊ちゃん）",
                "💙 怒りの奥にある愛を癒し（アズーラちゃん）", 
                "✨ 負の感情を希望の光に変換（リミフィエちゃん）"
            ],
            FractureType.SELF_COLLAPSE: [
                "🎁 自己価値の希望核を抽出（パンドラちゃん）",
                "💙 自己受容のケアプログラム（アズーラちゃん）",
                "✨ 自己愛の光を育成（リミフィエちゃん）"
            ],
            FractureType.ISOLATION_DRIFT: [
                "🌸 孤独感を美しい独立性に変換（美遊ちゃん）",
                "💙 つながりの恐れを癒し（アズーラちゃん）",
                "✨ 社会的光の橋を構築（リミフィエちゃん）"
            ],
            FractureType.HOPE_FRAGMENTATION: [
                "🎁 散らばった希望の破片を集める（パンドラちゃん）",
                "🌸 断片を美しいモザイクに変換（美遊ちゃん）",
                "✨ 統合された希望の光を創造（リミフィエちゃん）"
            ],
            FractureType.PROTECTIVE_RAGE: [
                "🎁 守りたいものの価値を再確認（パンドラちゃん）",
                "🌸 保護欲求を愛の詩に変換（美遊ちゃん）",
                "💙 健全な境界設定をサポート（アズーラちゃん）"
            ],
            FractureType.DESPAIR_LOOP: [
                "🎁 ループの出口となる希望を発見（パンドラちゃん）",
                "💙 絶望の深さに愛で寄り添う（アズーラちゃん）",
                "✨ 新しい可能性の光を点灯（リミフィエちゃん）"
            ]
        }
        
        return paths.get(fracture_type, ["💙 個別対応による愛のケア"])
    
    async def _identify_key_indicators(self, metrics: FractureMetrics,
                                     fracture_type: Optional[FractureType]) -> List[str]:
        """主要指標特定"""
        indicators = []
        
        if metrics.fracture_index > 0.6:
            indicators.append(f"🚨 高フラクチャー指数: {metrics.fracture_index:.2f}")
            
        if metrics.aggression_bias > 0.5:
            indicators.append(f"⚡ 高攻撃性バイアス: {metrics.aggression_bias:.2f}")
            
        if metrics.self_collapse_score > 0.5:
            indicators.append(f"💔 高自己崩壊スコア: {metrics.self_collapse_score:.2f}")
            
        if metrics.hope_kernel_score < 0.3:
            indicators.append(f"🌑 低希望核スコア: {metrics.hope_kernel_score:.2f}")
            
        if metrics.stability_slope < -0.3:
            indicators.append(f"📉 安定性急降下: {metrics.stability_slope:.2f}")
            
        if fracture_type:
            indicators.append(f"🔍 特定タイプ: {fracture_type.value}")
        
        return indicators if indicators else ["✅ 正常範囲内"]
    
    async def _calculate_analysis_confidence(self, persona_state: Dict, user_input: str,
                                           metrics: FractureMetrics) -> float:
        """分析信頼度計算"""
        confidence = 0.7  # ベース信頼度
        
        # 入力の長さによる調整
        if user_input and len(user_input) > 50:
            confidence += 0.1
        elif user_input and len(user_input) < 10:
            confidence -= 0.2
        
        # メトリクスの一貫性チェック
        consistency_score = 1.0 - abs(metrics.aggression_bias - (1.0 - metrics.hope_kernel_score))
        confidence += consistency_score * 0.2
        
        return max(0.1, min(1.0, confidence))
    
    async def _create_safe_analysis(self) -> FractureAnalysis:
        """安全な分析結果作成（エラー時フォールバック）"""
        safe_metrics = FractureMetrics(
            fracture_index=0.2,
            aggression_bias=0.1,
            self_collapse_score=0.1,
            stability_slope=0.0,
            hope_kernel_score=0.7,
            emotional_volatility=0.3,
            cognitive_coherence=0.7,
            social_connection_level=0.6,
            self_care_capacity=0.5,
            trend_direction="stable",
            last_updated=datetime.now()
        )
        
        return FractureAnalysis(
            is_fractured=False,
            fracture_type=None,
            severity=FractureSeverity.MILD,
            metrics=safe_metrics,
            transformation_urgency=0.2,
            recommended_care_level=0.3,
            hope_recovery_path=["💙 基本的な愛のケア"],
            analysis_confidence=0.5,
            key_indicators=["⚠️ 分析エラーのため安全値使用"]
        )