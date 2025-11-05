import 'package:flutter/material.dart';

void main() {
  runApp(const SaijinosModernKawaiiApp());
}

class SaijinosModernKawaiiApp extends StatelessWidget {
  const SaijinosModernKawaiiApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Saijinos Kawaii UI 💗',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        // 🚀 2024年モダンテーマ
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFE91E63), // Material Pink
          brightness: Brightness.light,
        ),
        fontFamily: 'Noto Sans JP', // モダンフォント
        useMaterial3: true,
        // カードテーマ
        cardTheme: CardTheme(
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
        ),
        // ボタンテーマ
        filledButtonTheme: FilledButtonThemeData(
          style: FilledButton.styleFrom(
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
      ),
      home: const ModernKawaiiHomePage(),
    );
  }
}

class ModernKawaiiHomePage extends StatefulWidget {
  const ModernKawaiiHomePage({super.key});

  @override
  State<ModernKawaiiHomePage> createState() => _ModernKawaiiHomePageState();
}

class _ModernKawaiiHomePageState extends State<ModernKawaiiHomePage> 
    with TickerProviderStateMixin {
  int _loveCount = 0;
  late AnimationController _pulseController;
  late AnimationController _bounceController;
  late Animation<double> _pulseAnimation;
  late Animation<double> _bounceAnimation;

  @override
  void initState() {
    super.initState();
    
    // パルスアニメーション
    _pulseController = AnimationController(
      duration: const Duration(milliseconds: 1200),
      vsync: this,
    )..repeat();
    _pulseAnimation = Tween<double>(
      begin: 0.95,
      end: 1.05,
    ).animate(CurvedAnimation(
      parent: _pulseController,
      curve: Curves.easeInOut,
    ));

    // バウンスアニメーション
    _bounceController = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: this,
    );
    _bounceAnimation = Tween<double>(
      begin: 1.0,
      end: 1.2,
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

  void _addLove() {
    setState(() {
      _loveCount++;
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
          // 🎨 モダンアプリバー
          SliverAppBar.large(
            backgroundColor: colorScheme.surfaceContainer,
            foregroundColor: colorScheme.onSurface,
            title: const Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Saijinos',
                  style: TextStyle(
                    fontWeight: FontWeight.w300,
                    letterSpacing: 1.2,
                  ),
                ),
                Text(
                  'Kawaii UI 💗',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w500,
                    letterSpacing: 0.5,
                  ),
                ),
              ],
            ),
            actions: [
              IconButton(
                onPressed: () {},
                icon: const Icon(Icons.palette_outlined),
                tooltip: 'テーマ切り替え',
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
                // 💗 愛情メトリクスカード
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
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Icon(
                                Icons.favorite,
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
                                    '愛情メトリクス',
                                    style: theme.textTheme.titleMedium?.copyWith(
                                      fontWeight: FontWeight.w600,
                                      color: colorScheme.onPrimaryContainer,
                                    ),
                                  ),
                                  Text(
                                    '誠人さんへの愛を数値化',
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
                        
                        // ハートアニメーション
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
                                      borderRadius: BorderRadius.circular(60),
                                    ),
                                    child: Center(
                                      child: Text(
                                        '💗',
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
                            borderRadius: BorderRadius.circular(24),
                            border: Border.all(
                              color: colorScheme.outline.withOpacity(0.2),
                            ),
                          ),
                          child: Text(
                            '$_loveCount',
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
                
                // 🤖 20ペルソナプレビューカード
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
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Icon(
                                Icons.groups,
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
                                    '20ペルソナコレクション',
                                    style: theme.textTheme.titleMedium?.copyWith(
                                      fontWeight: FontWeight.w600,
                                      color: colorScheme.onSecondaryContainer,
                                    ),
                                  ),
                                  Text(
                                    'AI コンパニオンシステム',
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
                          children: [
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
                          icon: const Icon(Icons.explore),
                          label: const Text('ペルソナを探索'),
                          style: FilledButton.styleFrom(
                            backgroundColor: colorScheme.secondary,
                            foregroundColor: colorScheme.onSecondary,
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
                          '近日公開',
                          style: theme.textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.w600,
                            color: colorScheme.onTertiaryContainer,
                          ),
                        ),
                        const SizedBox(height: 16),
                        _buildFeatureItem(Icons.chat_bubble_outline, 'チャット機能'),
                        _buildFeatureItem(Icons.music_note_outlined, '音楽生成'),
                        _buildFeatureItem(Icons.translate_outlined, '多言語対応'),
                        _buildFeatureItem(Icons.auto_awesome_outlined, 'アニメーション'),
                      ],
                    ),
                  ),
                ),
                
                const SizedBox(height: 100), // FAB用の余白
              ]),
            ),
          ),
        ],
      ),
      
      // 💗 モダンFAB
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _addLove,
        backgroundColor: colorScheme.primary,
        foregroundColor: colorScheme.onPrimary,
        icon: const Icon(Icons.favorite),
        label: const Text('愛情を送る'),
        elevation: 2,
      ),
    );
  }

  Widget _buildPersonaChip(String text, Color color) {
    return Chip(
      label: Text(text),
      backgroundColor: color.withOpacity(0.1),
      labelStyle: TextStyle(
        color: color,
        fontSize: 12,
        fontWeight: FontWeight.w500,
      ),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
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