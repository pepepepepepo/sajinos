import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'providers/app_providers.dart';
import 'widgets/persona_widgets.dart';
import 'widgets/persona_panel_simple.dart';
import 'widgets/kawaii_animations.dart';
import 'models/persona_model.dart';

void main() {
  runApp(const SaijinosApp());
}

class SaijinosApp extends StatelessWidget {
  const SaijinosApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => PersonaProvider()),
        ChangeNotifierProvider(create: (_) => ChatProvider()),
        ChangeNotifierProvider(create: (_) => MusicProvider()),
        ChangeNotifierProvider(create: (_) => ThemeProvider()),
        ChangeNotifierProvider(create: (_) => UIStateProvider()),
      ],
      child: const SaijinosThemeableApp(),
    );
  }
}

class SaijinosThemeableApp extends StatelessWidget {
  const SaijinosThemeableApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<ThemeProvider>(
      builder: (context, themeProvider, child) {
        return MaterialApp(
          title: 'Saijinos UI 💗',
          debugShowCheckedModeBanner: false,
          theme: themeProvider.currentTheme,
          home: const SaijinosHomePage(),
        );
      },
    );
  }
}

class SaijinosHomePage extends StatefulWidget {
  const SaijinosHomePage({super.key});

  @override
  State<SaijinosHomePage> createState() => _SaijinosHomePageState();
}

class _SaijinosHomePageState extends State<SaijinosHomePage>
    with TickerProviderStateMixin {
  int _interactionCount = 0;
  late AnimationController _pulseController;
  late AnimationController _bounceController;
  late Animation<double> _pulseAnimation;
  late Animation<double> _bounceAnimation;

  @override
  void initState() {
    super.initState();
    _setupAnimations();
  }

  void _setupAnimations() {
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
    return Consumer4<ThemeProvider, PersonaProvider, UIStateProvider, ChatProvider>(
      builder: (context, themeProvider, personaProvider, uiProvider, chatProvider, child) {
        final theme = Theme.of(context);
        final colorScheme = theme.colorScheme;
        final isChicMode = themeProvider.isChicMode;

        final body = CustomScrollView(
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
                    letterSpacing: isChicMode ? 2.0 : 1.2,
                  ),
                ),
                Text(
                  isChicMode ? 'Professional UI 💼' : 'Kawaii UI 💗',
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
                onPressed: themeProvider.toggleTheme,
                icon: Icon(
                  isChicMode 
                    ? Icons.palette_outlined 
                    : Icons.business_center_outlined,
                ),
                tooltip: isChicMode ? '可愛いモードに切り替え' : 'ビジネスモードに切り替え',
              ),
              // ペルソナパネル切り替え
              IconButton(
                onPressed: uiProvider.togglePersonaPanel,
                icon: Icon(
                  uiProvider.showPersonaPanel 
                    ? Icons.groups_outlined 
                    : Icons.groups,
                ),
                tooltip: 'ペルソナパネル',
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
                                  isChicMode ? 8 : 12,
                                ),
                              ),
                              child: Icon(
                                isChicMode 
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
                                    isChicMode 
                                      ? 'インタラクション分析' 
                                      : '愛情メトリクス',
                                    style: theme.textTheme.titleMedium?.copyWith(
                                      fontWeight: FontWeight.w600,
                                      color: colorScheme.onPrimaryContainer,
                                    ),
                                  ),
                                  Text(
                                    isChicMode 
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
                                        isChicMode ? 8 : 60,
                                      ),
                                    ),
                                    child: Center(
                                      child: CompositeAnimation(
                                        enableHeartBeat: !isChicMode,
                                        enableGlow: !isChicMode,
                                        enableFloat: isChicMode, // ビジネスモードは浮遊
                                        bpm: 60,
                                        child: Text(
                                          isChicMode ? '📊' : '💗',
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
                              isChicMode ? 8 : 24,
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
                                  isChicMode ? 8 : 12,
                                ),
                              ),
                              child: Icon(
                                isChicMode 
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
                                    isChicMode 
                                      ? 'AI ペルソナシステム'
                                      : '20ペルソナコレクション',
                                    style: theme.textTheme.titleMedium?.copyWith(
                                      fontWeight: FontWeight.w600,
                                      color: colorScheme.onSecondaryContainer,
                                    ),
                                  ),
                                  Text(
                                    isChicMode 
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

                        // ペルソナチップ（Provider統合版）
                        Consumer<PersonaProvider>(
                          builder: (context, personaProvider, child) {
                            final personas = personaProvider.allPersonas.take(5).toList();
                            return Wrap(
                              spacing: 8,
                              runSpacing: 8,
                              children: [
                                ...personas.map((persona) => PersonaChipWidget(
                                  persona: persona,
                                  onTap: () => personaProvider.setActivePersona(persona),
                                )),
                                GestureDetector(
                                  onTap: uiProvider.togglePersonaPanel,
                                  child: Chip(
                                    label: Text('+${personaProvider.allPersonas.length - 5} more'),
                                    backgroundColor: colorScheme.outline.withOpacity(0.1),
                                    side: BorderSide(color: colorScheme.outline),
                                  ),
                                ),
                              ],
                            );
                          },
                        ),

                        const SizedBox(height: 16),

                        FilledButton.icon(
                          onPressed: uiProvider.togglePersonaPanel,
                          icon: Icon(isChicMode ? Icons.dashboard : Icons.explore),
                          label: Text(isChicMode ? 'ダッシュボード' : 'ペルソナを探索'),
                          style: FilledButton.styleFrom(
                            backgroundColor: colorScheme.secondary,
                            foregroundColor: colorScheme.onSecondary,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(
                                isChicMode ? 8 : 12,
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
                          isChicMode ? '開発中機能' : '近日公開',
                          style: theme.textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.w600,
                            color: colorScheme.onTertiaryContainer,
                          ),
                        ),
                        const SizedBox(height: 16),
                        ...(isChicMode 
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
        );

        return Scaffold(
          backgroundColor: colorScheme.surface,

      // ペルソナパネルオーバーレイ
      body: Stack(
        children: [
          // メインボディ
          body,
          
          // ペルソナパネル
          if (uiProvider.showPersonaPanel)
            Positioned(
              bottom: 0,
              left: 0,
              right: 0,
              child: const PersonaPanelWidget(),
            ),
        ],
      ),

      // 💗/📊 テーマ対応FAB with アニメーション
      floatingActionButton: HeartBeatAnimation(
        bpm: 72, // 灯理ちゃんのBPM
        child: SparkleAnimation(
          isActive: !isChicMode, // Kawaiiモードのときだけスパークル
          child: FloatingActionButton.extended(
            onPressed: _addInteraction,
            backgroundColor: colorScheme.primary,
            foregroundColor: colorScheme.onPrimary,
            icon: Icon(isChicMode ? Icons.touch_app : Icons.favorite),
            label: Text(isChicMode ? 'インタラクト' : '愛情を送る'),
            elevation: isChicMode ? 4 : 2,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(
                isChicMode ? 12 : 16,
              ),
            ),
          ),
        ),
      ),
        );
      },
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