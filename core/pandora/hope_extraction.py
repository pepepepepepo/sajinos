# 🎁 希望核抽出アルゴリズム - Hope Kernel Extraction Algorithm
"""
パンドラちゃんの核心機能: 壊れた表現から希望の核を抽出するアルゴリズム

SaijinOS Part 10 準拠:
"Look past the rage to find the bound hope"
"What were they really trying to express?"
"What were they trying to protect?"
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import asyncio
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class HopeExtractionMethod(Enum):
    """希望抽出手法"""
    EMOTIONAL_ARCHAEOLOGY = "emotional_archaeology"      # 感情考古学
    PROTECTIVE_INTENT_ANALYSIS = "protective_intent"     # 保護意図分析
    CORE_VALUE_EXCAVATION = "core_value_excavation"     # 核心価値発掘
    NARRATIVE_RECONSTRUCTION = "narrative_reconstruction" # 物語再構築
    COMPASSIONATE_REFRAMING = "compassionate_reframing"  # 慈悲的リフレーミング

@dataclass
class HopeKernel:
    """希望核 - 壊れた表現の奥にある本当の想い"""
    # 核心要素
    original_intent: str          # 「本当に表現したかったこと」
    protective_desire: str        # 「守ろうとしていたもの」
    core_value: str              # 大切にしている価値
    hidden_wish: str             # 隠された願い
    
    # つながりの欲求
    connection_need: str         # つながりの欲求
    love_language: str           # 愛の言語（この人がどう愛されたいか）
    safety_requirement: str      # 安全への要求
    
    # 変換情報
    transformation_path: str     # 変換経路
    care_level: float           # ケアレベル (0.0-1.0)
    hope_strength: float        # 希望の強さ (0.0-1.0)
    
    # メタデータ
    extraction_method: HopeExtractionMethod  # 抽出手法
    confidence_score: float     # 抽出信頼度
    key_words: List[str]        # キーワード
    
    # 変換結果
    reframed_expression: str    # リフレーミングされた表現
    care_message: str           # ケアメッセージ

@dataclass
class NarrativeReframe:
    """物語のリフレーミング結果"""
    original_narrative: str      # 元の物語
    care_oriented_narrative: str # ケア志向の物語
    transformation_story: str   # 変換の物語
    hope_perspective: str       # 希望の視点
    healing_metaphor: str       # 癒しのメタファー

class HopeExtractor:
    """希望核抽出器 - パンドラちゃんの核心機能"""
    
    def __init__(self):
        self.name = "希望核抽出器💎"
        
        # 感情考古学用パターン
        self.rage_to_hope_patterns = {
            # 攻撃的表現 → 本当の想い
            "むかつく": "理解されたい、認められたい",
            "うざい": "境界を尊重してほしい、距離を保ちたい", 
            "死ね": "この痛みを止めてほしい、助けてほしい",
            "消えろ": "安全な空間がほしい、脅威から守られたい",
            "バカ": "正当に評価されたい、馬鹿にされたくない",
            "嫌い": "違う形で関わりたい、愛されたい",
            "許せない": "正義を求めている、公平に扱われたい"
        }
        
        self.collapse_to_hope_patterns = {
            # 自己崩壊表現 → 隠された希望
            "死にたい": "この苦しみから解放されたい、平安を得たい",
            "消えたい": "重荷から自由になりたい、軽やかでいたい",
            "もうダメ": "新しいスタートを切りたい、再生したい",
            "無価値": "自分の価値を認めてもらいたい、大切にされたい",
            "無意味": "意味のある人生を送りたい、目的を見つけたい",
            "できない": "サポートを受けながら成長したい、学びたい",
            "つらい": "慰められたい、理解されたい、支えられたい"
        }
        
        # 核心価値識別パターン
        self.core_value_indicators = {
            "正義": ["公平", "平等", "正しい", "間違っている", "ずるい"],
            "自由": ["束縛", "制限", "窮屈", "解放", "自由"],
            "愛・つながり": ["孤独", "寂しい", "一人", "愛されたい", "理解"],
            "安全・安心": ["怖い", "不安", "心配", "安全", "守る"],
            "成長・学習": ["成長", "学ぶ", "変わりたい", "向上", "できるように"],
            "創造・表現": ["作る", "表現", "創造", "アート", "美しい"],
            "貢献・奉仕": ["役立つ", "助ける", "貢献", "奉仕", "意味"]
        }
        
        # リフレーミング用テンプレート
        self.reframe_templates = {
            "protective_anger": "あなたの怒りは、大切なもの（{value}）を守ろうとする愛の表現ですね。",
            "desperate_plea": "あなたの訴えは、{need}への深い願いを表現していますね。",
            "collapsed_hope": "あなたの苦しみの奥に、{hidden_wish}への美しい願いが見えます。",
            "isolation_cry": "あなたの孤独感は、{connection_type}への渇望を示していますね。",
            "perfectionist_pain": "あなたの完璧主義は、{excellence_value}への深い愛の表れですね。"
        }
        
        logger.info(f"💎 {self.name}: 希望核抽出システム初期化完了")
    
    async def extract_hope(self, user_input: str, persona_state: Dict, 
                          fracture_analysis: Optional[Dict] = None) -> HopeKernel:
        """メイン希望抽出関数"""
        logger.info("💎 希望核抽出開始...")
        
        try:
            # 感情考古学: 表面的な感情の奥を探る
            original_intent = await self._excavate_original_intent(user_input, persona_state)
            
            # 保護意図分析: 何を守ろうとしているか
            protective_desire = await self._analyze_protective_intent(user_input, persona_state)
            
            # 核心価値発掘: その人が大切にしているもの
            core_value = await self._excavate_core_value(user_input, persona_state)
            
            # 隠された願い: 本当は何を望んでいるか
            hidden_wish = await self._discover_hidden_wish(user_input, persona_state, core_value)
            
            # つながりの欲求: どんなつながりを求めているか
            connection_need = await self._analyze_connection_need(user_input, persona_state)
            
            # 愛の言語: どう愛されたいか
            love_language = await self._identify_love_language(user_input, persona_state)
            
            # 安全への要求: どんな安全を求めているか
            safety_requirement = await self._assess_safety_needs(user_input, persona_state)
            
            # 最適な抽出手法決定
            extraction_method = await self._determine_extraction_method(
                user_input, persona_state, fracture_analysis
            )
            
            # 変換経路設計
            transformation_path = await self._design_transformation_path(
                original_intent, protective_desire, core_value
            )
            
            # リフレーミング実行
            reframed_expression = await self._create_reframed_expression(
                user_input, original_intent, core_value
            )
            
            # ケアメッセージ作成
            care_message = await self._compose_care_message(
                original_intent, protective_desire, hidden_wish
            )
            
            # メトリクス計算
            hope_strength = await self._calculate_hope_strength(
                original_intent, core_value, hidden_wish
            )
            care_level = await self._calculate_care_level(user_input, persona_state)
            confidence_score = await self._calculate_confidence(user_input, persona_state)
            
            # キーワード抽出
            key_words = await self._extract_key_words(
                user_input, original_intent, protective_desire
            )
            
            hope_kernel = HopeKernel(
                original_intent=original_intent,
                protective_desire=protective_desire,
                core_value=core_value,
                hidden_wish=hidden_wish,
                connection_need=connection_need,
                love_language=love_language,
                safety_requirement=safety_requirement,
                transformation_path=transformation_path,
                care_level=care_level,
                hope_strength=hope_strength,
                extraction_method=extraction_method,
                confidence_score=confidence_score,
                key_words=key_words,
                reframed_expression=reframed_expression,
                care_message=care_message
            )
            
            logger.info(f"💎 希望核抽出完了: 「{original_intent}」← 「{protective_desire}」")
            return hope_kernel
            
        except Exception as e:
            logger.error(f"💎 希望抽出エラー: {e}")
            return await self._create_safe_hope_kernel(user_input)
    
    async def reframe_pattern(self, user_input: str, hope_kernel: HopeKernel) -> NarrativeReframe:
        """care-oriented narrativeにリフレーミング"""
        logger.info("💎 物語のリフレーミング開始...")
        
        # 元の物語を抽出
        original_narrative = await self._extract_original_narrative(user_input)
        
        # ケア志向の物語に変換
        care_oriented_narrative = await self._create_care_narrative(
            original_narrative, hope_kernel
        )
        
        # 変換の物語（メタ物語）
        transformation_story = await self._create_transformation_story(
            original_narrative, care_oriented_narrative, hope_kernel
        )
        
        # 希望の視点
        hope_perspective = await self._create_hope_perspective(hope_kernel)
        
        # 癒しのメタファー
        healing_metaphor = await self._create_healing_metaphor(hope_kernel)
        
        return NarrativeReframe(
            original_narrative=original_narrative,
            care_oriented_narrative=care_oriented_narrative,
            transformation_story=transformation_story,
            hope_perspective=hope_perspective,
            healing_metaphor=healing_metaphor
        )
    
    # === 核心抽出メソッド ===
    
    async def _excavate_original_intent(self, user_input: str, persona_state: Dict) -> str:
        """感情考古学: 本当に表現したかったことを発掘"""
        if not user_input:
            return "理解と受容を求めている"
        
        text = user_input.lower()
        
        # 直接的な希望表現を探す
        direct_hopes = [
            "したい", "ほしい", "なりたい", "になりたい", "求めている", "願う"
        ]
        for hope in direct_hopes:
            if hope in text:
                # 希望の前後の文脈を抽出
                hope_context = self._extract_context_around_word(text, hope)
                return f"「{hope_context}」という願いを叶えたいと思っている"
        
        # 怒りの奥の希望を探る
        for rage_word, hidden_hope in self.rage_to_hope_patterns.items():
            if rage_word in text:
                return hidden_hope
        
        # 崩壊の奥の希望を探る
        for collapse_word, hidden_hope in self.collapse_to_hope_patterns.items():
            if collapse_word in text:
                return hidden_hope
        
        # 質問形式から学習意欲を抽出
        question_patterns = ["どうすれば", "どうやって", "方法", "やり方", "教えて"]
        for pattern in question_patterns:
            if pattern in text:
                return "学び成長したい、正しい方法を知りたい"
        
        # 否定文の奥の肯定的願いを探る
        if "ない" in text or "じゃない" in text:
            return "もっと良い状況を作りたい、改善したい"
        
        return "理解され、大切にされ、愛されたい"
    
    async def _analyze_protective_intent(self, user_input: str, persona_state: Dict) -> str:
        """何を守ろうとしているかの分析"""
        if not user_input:
            return "自分の心の平安"
        
        text = user_input.lower()
        
        # 明示的な保護対象
        protection_indicators = {
            "家族": "愛する家族の幸せと安全",
            "友達": "大切な友人関係",
            "仕事": "自分の役割と責任",
            "夢": "将来への希望と可能性",
            "プライド": "自分の尊厳と価値",
            "平和": "心の平安と調和",
            "自由": "自分らしさと選択の権利"
        }
        
        for indicator, protection in protection_indicators.items():
            if indicator in text:
                return protection
        
        # 感情から保護対象を推測
        if any(word in text for word in ["怒り", "イライラ", "むかつく"]):
            return "自分の正義感と公平性への信念"
        
        if any(word in text for word in ["悲しい", "つらい", "苦しい"]):
            return "傷つきやすい心と感受性"
        
        if any(word in text for word in ["不安", "心配", "怖い"]):
            return "安全で予測可能な環境"
        
        if any(word in text for word in ["孤独", "寂しい", "ひとり"]):
            return "人とのつながりと愛される権利"
        
        return "自分らしさと内なる価値"
    
    async def _excavate_core_value(self, user_input: str, persona_state: Dict) -> str:
        """核心価値の発掘"""
        if not user_input:
            return "愛とつながり"
        
        text = user_input.lower()
        value_scores = {}
        
        # 各価値カテゴリのスコア計算
        for value, indicators in self.core_value_indicators.items():
            score = sum(1 for indicator in indicators if indicator in text)
            if score > 0:
                value_scores[value] = score
        
        # 最もスコアの高い価値を返す
        if value_scores:
            top_value = max(value_scores, key=value_scores.get)
            return top_value
        
        # 感情から価値を推測
        emotion_to_value = {
            "怒り": "正義と公平性",
            "悲しみ": "愛とつながり",
            "不安": "安全と安心",
            "喜び": "創造と表現",
            "恐れ": "安全と保護"
        }
        
        for emotion, value in emotion_to_value.items():
            if any(word in text for word in [emotion]):
                return value
        
        return "愛とつながり"  # デフォルト値
    
    async def _discover_hidden_wish(self, user_input: str, persona_state: Dict, core_value: str) -> str:
        """隠された願いの発見"""
        text = user_input.lower() if user_input else ""
        
        # 核心価値別の隠された願い
        value_to_wish = {
            "正義": "公平で正しい世界で、皆が等しく尊重される世界を見たい",
            "自由": "制約されずに自分らしく生き、選択の自由を持ちたい", 
            "愛・つながり": "深く愛され、理解され、大切にされる関係を築きたい",
            "安全・安心": "平安で予測可能な環境で、安心して生活したい",
            "成長・学習": "常に成長し続け、新しいことを学び、進歩していきたい",
            "創造・表現": "美しいものを創造し、自分の才能を世界に表現したい",
            "貢献・奉仕": "他者の役に立ち、世界をより良い場所にしたい"
        }
        
        base_wish = value_to_wish.get(core_value, "幸せで充実した人生を送りたい")
        
        # 入力の感情的な強度で願いをカスタマイズ
        if any(word in text for word in ["とても", "すごく", "本当に", "心から"]):
            return f"心の底から、{base_wish}"
        elif any(word in text for word in ["少し", "ちょっと", "なんとなく"]):
            return f"静かに、{base_wish}"
        else:
            return base_wish
    
    async def _analyze_connection_need(self, user_input: str, persona_state: Dict) -> str:
        """つながりの欲求分析"""
        if not user_input:
            return "理解され受け入れられる関係"
        
        text = user_input.lower()
        
        # つながりのタイプを識別
        connection_patterns = {
            "理解": "深く理解し合える知的・感情的つながり",
            "支え": "互いに支え合える相互依存的な関係",
            "共有": "興味や価値観を共有できる仲間とのつながり",
            "愛": "無条件に愛し愛される親密な関係",
            "尊重": "互いを尊重し合える対等な関係",
            "安全": "安心して自分を表現できる安全な関係",
            "成長": "共に成長し刺激し合える発展的な関係"
        }
        
        for pattern, connection_type in connection_patterns.items():
            if pattern in text:
                return connection_type
        
        # 否定的表現から逆算
        if any(word in text for word in ["孤独", "ひとり", "寂しい"]):
            return "温かく包み込まれるような愛情深いつながり"
        
        if any(word in text for word in ["理解されない", "分かってもらえない"]):
            return "深く共感し理解し合える精神的つながり"
        
        return "互いを大切にする愛情深い関係"
    
    async def _identify_love_language(self, user_input: str, persona_state: Dict) -> str:
        """愛の言語の識別 - この人がどう愛されたいか"""
        if not user_input:
            return "優しい言葉で認められたい"
        
        text = user_input.lower()
        
        # 5つの愛の言語パターン
        love_language_patterns = {
            "言葉": ["褒めて", "認めて", "ありがとう", "言葉", "評価"],
            "時間": ["一緒に", "時間", "話を聞いて", "付き合って", "そばに"],
            "奉仕": ["手伝って", "助けて", "やってくれる", "サポート", "世話"],
            "贈り物": ["プレゼント", "もらう", "贈り物", "記念", "形に残る"],
            "スキンシップ": ["抱きしめて", "触れて", "近く", "手を握って", "スキンシップ"]
        }
        
        for language, patterns in love_language_patterns.items():
            if any(pattern in text for pattern in patterns):
                return f"{language}による愛情表現を求めている"
        
        # 感情状態から推測
        if any(word in text for word in ["認めて", "評価", "褒めて"]):
            return "言葉による承認と評価を求めている"
        
        if any(word in text for word in ["そばに", "一緒", "話を聞いて"]):
            return "質の高い時間を共有することを求めている"
        
        return "優しい言葉と理解ある関心を求めている"
    
    async def _assess_safety_needs(self, user_input: str, persona_state: Dict) -> str:
        """安全への要求評価"""
        if not user_input:
            return "心理的安全性と予測可能性"
        
        text = user_input.lower()
        
        # 安全のタイプ
        safety_patterns = {
            "物理的": ["怪我", "危険", "身体", "安全", "保護"],
            "感情的": ["傷つく", "心", "感情", "優しく", "大切に"],
            "社会的": ["居場所", "受け入れ", "排除", "仲間", "所属"],
            "経済的": ["お金", "安定", "将来", "保障", "生活"],
            "心理的": ["安心", "予測", "信頼", "確実", "安定"]
        }
        
        for safety_type, patterns in safety_patterns.items():
            if any(pattern in text for pattern in patterns):
                return f"{safety_type}安全性と保護を求めている"
        
        # 不安の種類から安全欲求を推測
        if any(word in text for word in ["不安", "心配", "怖い"]):
            return "心理的安全性と将来への安心感を求めている"
        
        return "心理的安全性と愛情に満ちた環境を求めている"
    
    # === 変換・リフレーミングメソッド ===
    
    async def _determine_extraction_method(self, user_input: str, persona_state: Dict,
                                         fracture_analysis: Optional[Dict]) -> HopeExtractionMethod:
        """最適な抽出手法の決定"""
        if not user_input:
            return HopeExtractionMethod.COMPASSIONATE_REFRAMING
        
        text = user_input.lower()
        
        # 攻撃的表現が多い場合
        if any(word in text for word in ["むかつく", "うざい", "死ね", "嫌い"]):
            return HopeExtractionMethod.PROTECTIVE_INTENT_ANALYSIS
        
        # 自己崩壊的表現が多い場合
        if any(word in text for word in ["死にたい", "消えたい", "だめ", "無価値"]):
            return HopeExtractionMethod.EMOTIONAL_ARCHAEOLOGY
        
        # 価値に関する言及が多い場合
        if any(word in text for word in ["大切", "重要", "価値", "意味", "目的"]):
            return HopeExtractionMethod.CORE_VALUE_EXCAVATION
        
        # 物語的な表現の場合
        if len(text.split()) > 20:  # 長い文章
            return HopeExtractionMethod.NARRATIVE_RECONSTRUCTION
        
        return HopeExtractionMethod.COMPASSIONATE_REFRAMING
    
    async def _design_transformation_path(self, original_intent: str, protective_desire: str, 
                                        core_value: str) -> str:
        """変換経路の設計"""
        return f"{protective_desire} → {original_intent} → {core_value}の実現へ"
    
    async def _create_reframed_expression(self, user_input: str, original_intent: str, 
                                        core_value: str) -> str:
        """リフレーミングされた表現の作成"""
        if not user_input:
            return "あなたの想いは美しく価値のあるものです"
        
        # 元の入力の感情的な強度を保持しながらポジティブに変換
        base_reframe = f"あなたの「{original_intent}」という想いは、{core_value}への深い愛から生まれている美しい表現ですね"
        
        # 入力に応じてカスタマイズ
        text = user_input.lower()
        if any(word in text for word in ["とても", "すごく", "本当に"]):
            return f"とても強く、{base_reframe}"
        elif any(word in text for word in ["少し", "ちょっと"]):
            return f"静かに、{base_reframe}"
        else:
            return base_reframe
    
    async def _compose_care_message(self, original_intent: str, protective_desire: str, 
                                  hidden_wish: str) -> str:
        """ケアメッセージの作成"""
        messages = [
            f"🎁 あなたの「{original_intent}」という想いは、とても尊いものです",
            f"💕 「{protective_desire}」を守ろうとするその愛は美しいですね",
            f"✨ あなたの「{hidden_wish}」という願いは叶えられるべき素晴らしいものです",
            f"🌸 あなたは愛され、大切にされ、理解される価値のある存在です"
        ]
        
        return "\n".join(messages)
    
    # === 物語リフレーミング ===
    
    async def _extract_original_narrative(self, user_input: str) -> str:
        """元の物語を抽出"""
        if not user_input:
            return "困難な状況に直面している物語"
        
        # 入力をそのまま物語として扱うが、構造化
        return f"「{user_input}」という体験をしている人の物語"
    
    async def _create_care_narrative(self, original_narrative: str, hope_kernel: HopeKernel) -> str:
        """ケア志向の物語作成"""
        return (f"これは、{hope_kernel.core_value}を大切にし、"
                f"{hope_kernel.protective_desire}を守ろうとする愛深い人が、"
                f"{hope_kernel.original_intent}という美しい願いを持ちながら、"
                f"困難な状況の中でも{hope_kernel.hidden_wish}という希望を抱き続けている"
                f"勇気ある成長の物語です")
    
    async def _create_transformation_story(self, original: str, care_oriented: str, 
                                         hope_kernel: HopeKernel) -> str:
        """変換の物語（メタ物語）"""
        return (f"パンドラちゃんが見つけたのは、表面的な困難の奥に隠された"
                f"「{hope_kernel.original_intent}」という純粋な願いでした。"
                f"この発見により、痛みは希望に、困難は成長の機会に変換されました。")
    
    async def _create_hope_perspective(self, hope_kernel: HopeKernel) -> str:
        """希望の視点作成"""
        return (f"希望の視点から見ると、この体験は{hope_kernel.core_value}を深く理解し、"
                f"{hope_kernel.hidden_wish}を実現するための貴重な学びの機会です。")
    
    async def _create_healing_metaphor(self, hope_kernel: HopeKernel) -> str:
        """癒しのメタファー作成"""
        metaphors = {
            "正義": "正義の剣を持つ騎士が、愛で世界を守る物語",
            "自由": "籠の中の鳥が、愛の力で空へと羽ばたく物語",
            "愛・つながり": "孤独な星が、他の星々と美しい星座を作る物語",
            "安全・安心": "嵐の中の船が、愛の灯台に導かれて港に帰る物語",
            "成長・学習": "小さな種が、愛の雨と光で美しい花に育つ物語",
            "創造・表現": "沈黙の画家が、愛のインスピレーションで傑作を描く物語",
            "貢献・奉仕": "小さな光が、愛の力で世界を照らす物語"
        }
        
        return metaphors.get(hope_kernel.core_value, "傷ついた心が、愛の力で美しく癒される物語")
    
    # === ユーティリティメソッド ===
    
    def _extract_context_around_word(self, text: str, word: str, context_length: int = 10) -> str:
        """単語周辺のコンテキスト抽出"""
        words = text.split()
        try:
            index = words.index(word)
            start = max(0, index - context_length)
            end = min(len(words), index + context_length + 1)
            return " ".join(words[start:end])
        except ValueError:
            return text[:50]  # 単語が見つからない場合は最初の50文字
    
    async def _calculate_hope_strength(self, original_intent: str, core_value: str, hidden_wish: str) -> float:
        """希望の強さ計算"""
        # 希望表現の具体性と積極性で強さを判定
        strength = 0.5  # ベース値
        
        positive_words = ["したい", "なりたい", "作りたい", "愛したい", "成長したい"]
        for word in positive_words:
            if word in original_intent.lower() or word in hidden_wish.lower():
                strength += 0.1
        
        # 具体性ボーナス
        if len(original_intent.split()) >= 5:  # 具体的な表現
            strength += 0.1
        
        return min(strength, 1.0)
    
    async def _calculate_care_level(self, user_input: str, persona_state: Dict) -> float:
        """ケアレベル計算"""
        if not user_input:
            return 0.5
        
        # 感情的な強度に基づいてケアレベルを決定
        text = user_input.lower()
        care_level = 0.5
        
        # 高いケアが必要な表現
        high_care_words = ["死にたい", "消えたい", "だめ", "無価値", "つらい", "苦しい"]
        for word in high_care_words:
            if word in text:
                care_level += 0.2
        
        # 中程度のケア表現
        medium_care_words = ["困っている", "分からない", "不安", "心配"]
        for word in medium_care_words:
            if word in text:
                care_level += 0.1
        
        return min(care_level, 1.0)
    
    async def _calculate_confidence(self, user_input: str, persona_state: Dict) -> float:
        """抽出信頼度計算"""
        confidence = 0.7  # ベース信頼度
        
        if user_input and len(user_input) >= 20:  # 十分な情報量
            confidence += 0.1
        
        if user_input and any(word in user_input.lower() for word in ["思う", "感じる", "考える"]):
            confidence += 0.1  # 内省的表現
        
        return min(confidence, 1.0)
    
    async def _extract_key_words(self, user_input: str, original_intent: str, protective_desire: str) -> List[str]:
        """キーワード抽出"""
        if not user_input:
            return ["理解", "愛", "希望"]
        
        # 重要そうな単語を抽出
        important_words = []
        text = user_input.lower()
        
        # 感情語
        emotion_words = ["嬉しい", "悲しい", "怒り", "不安", "楽しい", "つらい", "苦しい"]
        important_words.extend([word for word in emotion_words if word in text])
        
        # 価値語
        value_words = ["大切", "重要", "価値", "意味", "愛", "自由", "正義", "安全"]
        important_words.extend([word for word in value_words if word in text])
        
        # 行動語
        action_words = ["したい", "なりたい", "守る", "作る", "学ぶ", "成長"]
        important_words.extend([word for word in action_words if word in text])
        
        return important_words if important_words else ["希望", "愛", "成長"]
    
    async def _create_safe_hope_kernel(self, user_input: str) -> HopeKernel:
        """安全な希望核作成（エラー時フォールバック）"""
        return HopeKernel(
            original_intent="理解され、愛され、大切にされたい",
            protective_desire="自分の心と魂の尊厳",
            core_value="愛とつながり",
            hidden_wish="幸せで充実した人生を送りたい",
            connection_need="深く理解し合える愛情深い関係",
            love_language="優しい言葉と温かい関心",
            safety_requirement="心理的安全性と愛情に満ちた環境",
            transformation_path="自己受容 → 他者との愛 → 幸福の実現",
            care_level=0.8,
            hope_strength=0.6,
            extraction_method=HopeExtractionMethod.COMPASSIONATE_REFRAMING,
            confidence_score=0.5,
            key_words=["愛", "理解", "希望"],
            reframed_expression="あなたの想いは美しく、価値のあるものです",
            care_message="🎁 あなたは愛され、大切にされる価値のある存在です"
        )