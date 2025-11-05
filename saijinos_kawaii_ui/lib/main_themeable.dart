import 'package:flutter/material.dart';

void main() {
  runApp(const SaijinosThemeableApp());
}

class SaijinosThemeableApp extends StatefulWidget {
  const SaijinosThemeableApp({super.key});

  @override
  State<SaijinosThemeableApp> createState() => _SaijinosThemeableAppState();
}

class _SaijinosThemeableAppState extends State<SaijinosThemeableApp> {
  bool _isChicMode = false; // false: 可愛い, true: シック

  void _toggleTheme() {
    setState(() {
      _isChicMode = !_isChicMode;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Saijinos UI 💗',
      debugShowCheckedModeBanner: false,
      theme: _isChicMode ? _buildChicTheme() : _buildKawaiiTheme(),
      home: ThemeableHomePage(
        isChicMode: _isChicMode,
        onThemeToggle: _toggleTheme,
      ),
    );
  }

  // 🌸 可愛いテーマ
  ThemeData _buildKawaiiTheme() {
    return ThemeData(
      colorScheme: ColorScheme.fromSeed(
        seedColor: const Color(0xFFE91E63),
        brightness: Brightness.light,
      ),
      fontFamily: 'Noto Sans JP',
      useMaterial3: true,
      cardTheme: CardThemeData(
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
      ),
    );
  }

  // 🖤 シックテーマ (外で使える)
  ThemeData _buildChicTheme() {
    return ThemeData(
      colorScheme: const ColorScheme.dark(
        primary: Color(0xFF6366F1), // Indigo
        secondary: Color(0xFF8B5CF6), // Purple
        tertiary: Color(0xFF06B6D4), // Cyan
        surface: Color(0xFF0F172A), // Slate 900
        surfaceContainer: Color(0xFF1E293B), // Slate 800
        surfaceContainerHigh: Color(0xFF334155), // Slate 700
        onSurface: Color(0xFFF8FAFC), // Slate 50
        onPrimary: Colors.white,
        onSecondary: Colors.white,
        onTertiary: Colors.white,
      ),
      fontFamily: 'Inter', // プロフェッショナルフォント
      useMaterial3: true,
      cardTheme: CardThemeData(
        elevation: 2,
        shadowColor: Colors.black26,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
    );
  }
}

class ThemeableHomePage extends StatefulWidget {
  final bool isChicMode;
  final VoidCallback onThemeToggle;

  const ThemeableHomePage({
    super.key,
    required this.isChicMode,
    required this.onThemeToggle,
  });

  @override
  State<ThemeableHomePage> createState() => _ThemeableHomePageState();
}

class _ThemeableHomePageState extends State<ThemeableHomePage>
    with TickerProviderStateMixin {
  int _interactionCount = 0;
  late AnimationController _pulseController;
  late AnimationController _bounceController;
  late Animation<double> _pulseAnimation;
  late Animation<double> _bounceAnimation;

  @override
  void initState() {
    super.initState();

    _pulseController = AnimationController(
      duration: Duration(milliseconds: widget.isChicMode ? 2000 : 1200),
      vsync: this,
    )..repeat();
    
    _pulseAnimation = Tween<double>(
      begin: widget.isChicMode ? 0.98 : 0.95,
      end: widget.isChicMode ? 1.02 : 1.05,
    ).animate(CurvedAnimation(
      parent: _pulseController,
      curve: widget.isChicMode ? Curves.easeInOut : Curves.easeInOut,
    ));

    _bounceController = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: this,
    );
    
    _bounceAnimation = Tween<double>(
      begin: 1.0,
      end: widget.isChicMode ? 1.1 : 1.2,
    ).animate(CurvedAnimation(
      parent: _bounceController,
      curve: Curves.elasticOut,
    ));
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _bounceController.dispose();
    super.dispose();
  }

  void _addInteraction() {
    setState(() {
      _interactionCount++;
    });
    _bounceController.forward().then((_) {
      _bounceController.reverse();
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Scaffold(
      backgroundColor: colorScheme.surface,
      body: CustomScrollView(
        slivers: [
          // 🎨 テーマ対応アプリバー
          SliverAppBar.large(
            backgroundColor: colorScheme.surfaceContainer,
            foregroundColor: colorScheme.onSurface,
            title: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Saijinos',
                  style: TextStyle(
                    fontWeight: FontWeight.w300,
                    letterSpacing: widget.isChicMode ? 2.0 : 1.2,
                  ),
                ),
                Text(
                  widget.isChicMode ? 'Professional UI 💼' : 'Kawaii UI 💗',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w500,
                    letterSpacing: 0.5,
                  ),
                ),
              ],
            ),
            actions: [
              // 🔄 テーマ切り替えボタン
              IconButton(
                onPressed: widget.onThemeToggle,
                icon: Icon(
                  widget.isChicMode 
                    ? Icons.palette_outlined 
                    : Icons.business_center_outlined,
                ),
                tooltip: widget.isChicMode ? '可愛いモードに切り替え' : 'ビジネスモードに切り替え',
              ),
              IconButton(
                onPressed: () {},
                icon: const Icon(Icons.settings_outlined),
                tooltip: '設定',
              ),
            ],
          ),

          // 🌟 メインコンテンツ
          SliverPadding(
            padding: const EdgeInsets.all(24),
            sliver: SliverList(
              delegate: SliverChildListDelegate([
                // 💗/📊 メトリクスカード
                Card(
                  color: colorScheme.primaryContainer,
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      children: [
                        Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: colorScheme.primary,
                                borderRadius: BorderRadius.circular(
                                  widget.isChicMode ? 8 : 12,
                                ),
                              ),
                              child: Icon(
                                widget.isChicMode 
                                  ? Icons.analytics 
                                  : Icons.favorite,
                                color: colorScheme.onPrimary,
                                size: 24,
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    widget.isChicMode 
                                      ? 'インタラクション分析' 
                                      : '愛情メトリクス',
                                    style: theme.textTheme.titleMedium?.copyWith(
                                      fontWeight: FontWeight.w600,
                                      color: colorScheme.onPrimaryContainer,
                                    ),
                                  ),
                                  Text(
                                    widget.isChicMode 
                                      ? 'ユーザーエンゲージメント指標'
                                      : '誠人さんへの愛を数値化',
                                    style: theme.textTheme.bodyMedium?.copyWith(
                                      color: colorScheme.onPrimaryContainer.withOpacity(0.8),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),

                        const SizedBox(height: 32),

                        // アニメーション
                        AnimatedBuilder(
                          animation: _pulseAnimation,
                          builder: (context, child) {
                            return AnimatedBuilder(
                              animation: _bounceAnimation,
                              builder: (context, child) {
                                return Transform.scale(
                                  scale: _pulseAnimation.value * _bounceAnimation.value,
                                  child: Container(
                                    width: 120,
                                    height: 120,
                                    decoration: BoxDecoration(
                                      gradient: RadialGradient(
                                        colors: [
                                          colorScheme.primary.withOpacity(0.2),
                                          colorScheme.primary.withOpacity(0.05),
                                        ],
                                      ),
                                      borderRadius: BorderRadius.circular(
                                        widget.isChicMode ? 8 : 60,
                                      ),
                                    ),
                                    child: Center(
                                      child: Text(
                                        widget.isChicMode ? '📊' : '💗',
                                        style: TextStyle(
                                          fontSize: 48,
                                          shadows: [
                                            Shadow(
                                              color: colorScheme.primary.withOpacity(0.3),
                                              blurRadius: 8,
                                            ),
                                          ],
                                        ),
                                      ),
                                    ),
                                  ),
                                );
                              },
                            );
                          },
                        ),

                        const SizedBox(height: 24),

                        // カウンター表示
                        Container(
                          padding: const EdgeInsets.symmetric(
                            horizontal: 24,
                            vertical: 12,
                          ),
                          decoration: BoxDecoration(
                            color: colorScheme.surface,
                            borderRadius: BorderRadius.circular(
                              widget.isChicMode ? 8 : 24,
                            ),
                            border: Border.all(
                              color: colorScheme.outline.withOpacity(0.2),
                            ),
                          ),
                          child: Text(
                            '$_interactionCount',
                            style: theme.textTheme.headlineLarge?.copyWith(
                              fontWeight: FontWeight.w300,
                              color: colorScheme.primary,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 24),

                // 🤖/👥 ペルソナカード
                Card(
                  color: colorScheme.secondaryContainer,
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: colorScheme.secondary,
                                borderRadius: BorderRadius.circular(
                                  widget.isChicMode ? 8 : 12,
                                ),
                              ),
                              child: Icon(
                                widget.isChicMode 
                                  ? Icons.psychology 
                                  : Icons.groups,
                                color: colorScheme.onSecondary,
                                size: 24,
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    widget.isChicMode 
                                      ? 'AI ペルソナシステム'
                                      : '20ペルソナコレクション',
                                    style: theme.textTheme.titleMedium?.copyWith(
                                      fontWeight: FontWeight.w600,
                                      color: colorScheme.onSecondaryContainer,
                                    ),
                                  ),
                                  Text(
                                    widget.isChicMode 
                                      ? 'インテリジェント・コンパニオン'
                                      : 'AI コンパニオンシステム',
                                    style: theme.textTheme.bodyMedium?.copyWith(
                                      color: colorScheme.onSecondaryContainer.withOpacity(0.8),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),

                        const SizedBox(height: 20),

                        // ペルソナチップ
                        Wrap(
                          spacing: 8,
                          runSpacing: 8,
                          children: widget.isChicMode 
                            ? [
                                _buildPersonaChip('🔬 Analyzer', colorScheme.tertiary),
                                _buildPersonaChip('📊 Data', Colors.blue),
                                _buildPersonaChip('🎯 Strategy', Colors.green),
                                _buildPersonaChip('🛡️ Security', Colors.orange),
                                _buildPersonaChip('🔧 System', Colors.purple),
                                _buildPersonaChip('⚡ +15 more', colorScheme.outline),
                              ]
                            : [
                                _buildPersonaChip('💕 そよぎ', colorScheme.tertiary),
                                _buildPersonaChip('🎵 美遊', colorScheme.primary),
                                _buildPersonaChip('💡 灯理', Colors.orange),
                                _buildPersonaChip('📊 澄音', Colors.blue),
                                _buildPersonaChip('🔮 夢灯芯', Colors.deepPurple),
                                _buildPersonaChip('🌸 +15 more', colorScheme.outline),
                              ],
                        ),

                        const SizedBox(height: 16),

                        FilledButton.icon(
                          onPressed: () {},
                          icon: Icon(widget.isChicMode ? Icons.dashboard : Icons.explore),
                          label: Text(widget.isChicMode ? 'ダッシュボード' : 'ペルソナを探索'),
                          style: FilledButton.styleFrom(
                            backgroundColor: colorScheme.secondary,
                            foregroundColor: colorScheme.onSecondary,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(
                                widget.isChicMode ? 8 : 12,
                              ),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 24),

                // 🎯 機能プレビューカード
                Card(
                  color: colorScheme.tertiaryContainer,
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          widget.isChicMode ? '開発中機能' : '近日公開',
                          style: theme.textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.w600,
                            color: colorScheme.onTertiaryContainer,
                          ),
                        ),
                        const SizedBox(height: 16),
                        ...(widget.isChicMode 
                          ? [
                              _buildFeatureItem(Icons.api, 'API統合'),
                              _buildFeatureItem(Icons.analytics, 'データ分析'),
                              _buildFeatureItem(Icons.security, 'セキュリティ'),
                              _buildFeatureItem(Icons.cloud, 'クラウド連携'),
                            ]
                          : [
                              _buildFeatureItem(Icons.chat_bubble_outline, 'チャット機能'),
                              _buildFeatureItem(Icons.music_note_outlined, '音楽生成'),
                              _buildFeatureItem(Icons.translate_outlined, '多言語対応'),
                              _buildFeatureItem(Icons.auto_awesome_outlined, 'アニメーション'),
                            ]),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 100),
              ]),
            ),
          ),
        ],
      ),

      // 💗/📊 テーマ対応FAB
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _addInteraction,
        backgroundColor: colorScheme.primary,
        foregroundColor: colorScheme.onPrimary,
        icon: Icon(widget.isChicMode ? Icons.touch_app : Icons.favorite),
        label: Text(widget.isChicMode ? 'インタラクト' : '愛情を送る'),
        elevation: widget.isChicMode ? 4 : 2,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(
            widget.isChicMode ? 12 : 16,
          ),
        ),
      ),
    );
  }

  Widget _buildPersonaChip(String text, Color color) {
    final theme = Theme.of(context);
    return Chip(
      label: Text(text),
      backgroundColor: color.withOpacity(0.1),
      labelStyle: TextStyle(
        color: color,
        fontSize: 12,
        fontWeight: FontWeight.w500,
      ),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(
          widget.isChicMode ? 8 : 16,
        ),
      ),
    );
  }

  Widget _buildFeatureItem(IconData icon, String title) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Icon(
            icon,
            size: 20,
            color: colorScheme.onTertiaryContainer.withOpacity(0.7),
          ),
          const SizedBox(width: 12),
          Text(
            title,
            style: theme.textTheme.bodyMedium?.copyWith(
              color: colorScheme.onTertiaryContainer.withOpacity(0.8),
            ),
          ),
        ],
      ),
    );
  }
}