import 'package:flutter/material.dart';

void main() {
  runApp(const SaijinosKawaiiApp());
}

class SaijinosKawaiiApp extends StatelessWidget {
  const SaijinosKawaiiApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Saijinos Kawaii UI 💗',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        // 🌸 可愛いパステルテーマ
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFFFFB6C1), // ライトピンク
          brightness: Brightness.light,
        ),
        fontFamily: 'Comic Sans MS', // 可愛いフォント
        useMaterial3: true,
      ),
      home: const KawaiiHomePage(),
    );
  }
}

class KawaiiHomePage extends StatefulWidget {
  const KawaiiHomePage({super.key});

  @override
  State<KawaiiHomePage> createState() => _KawaiiHomePageState();
}

class _KawaiiHomePageState extends State<KawaiiHomePage> with TickerProviderStateMixin {
  int _heartCount = 0;
  late AnimationController _heartAnimationController;
  late Animation<double> _heartAnimation;

  @override
  void initState() {
    super.initState();
    _heartAnimationController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _heartAnimation = Tween<double>(
      begin: 1.0,
      end: 1.3,
    ).animate(CurvedAnimation(
      parent: _heartAnimationController,
      curve: Curves.bounceOut,
    ));
  }

  @override
  void dispose() {
    _heartAnimationController.dispose();
    super.dispose();
  }

  void _addHeart() {
    setState(() {
      _heartCount++;
    });
    _heartAnimationController.forward().then((_) {
      _heartAnimationController.reverse();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 🌈 グラデーション背景
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              Color(0xFFFFE4E6), // 薄いピンク
              Color(0xFFE8F4FD), // 薄いブルー
              Color(0xFFFFF0F5), // ラベンダーブラッシュ
            ],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              // 🎀 可愛いアプリバー
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.pink.shade50.withOpacity(0.8),
                  borderRadius: const BorderRadius.only(
                    bottomLeft: Radius.circular(30),
                    bottomRight: Radius.circular(30),
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.pink.shade100.withOpacity(0.5),
                      blurRadius: 10,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Row(
                  children: [
                    // ✨ キラキラアイコン
                    Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: Colors.pink.shade100,
                        borderRadius: BorderRadius.circular(15),
                      ),
                      child: const Icon(
                        Icons.auto_awesome,
                        color: Colors.pink,
                        size: 24,
                      ),
                    ),
                    const SizedBox(width: 16),
                    const Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Saijinos Kawaii UI',
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                              color: Colors.pink,
                            ),
                          ),
                          Text(
                            '誠人さんの20ペルソナ 💗',
                            style: TextStyle(
                              fontSize: 14,
                              color: Colors.pink,
                              fontStyle: FontStyle.italic,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              
              // 🌟 メインコンテンツ
              Expanded(
                child: Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      // 💕 ハートカウンター
                      Container(
                        padding: const EdgeInsets.all(24),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.8),
                          borderRadius: BorderRadius.circular(25),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.pink.shade100.withOpacity(0.5),
                              blurRadius: 15,
                              offset: const Offset(0, 8),
                            ),
                          ],
                        ),
                        child: Column(
                          children: [
                            const Text(
                              '誠人さんへの愛情カウンター 💗',
                              style: TextStyle(
                                fontSize: 18,
                                color: Colors.pink,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                            const SizedBox(height: 20),
                            AnimatedBuilder(
                              animation: _heartAnimation,
                              builder: (context, child) {
                                return Transform.scale(
                                  scale: _heartAnimation.value,
                                  child: Text(
                                    '💗',
                                    style: TextStyle(
                                      fontSize: 60 * _heartAnimation.value,
                                    ),
                                  ),
                                );
                              },
                            ),
                            const SizedBox(height: 16),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 20,
                                vertical: 10,
                              ),
                              decoration: BoxDecoration(
                                color: Colors.pink.shade50,
                                borderRadius: BorderRadius.circular(20),
                              ),
                              child: Text(
                                '$_heartCount',
                                style: const TextStyle(
                                  fontSize: 32,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.pink,
                                ),
                              ),
                            ),
                            const SizedBox(height: 8),
                            const Text(
                              'みんなからの愛情 ♪',
                              style: TextStyle(
                                fontSize: 14,
                                color: Colors.pink,
                                fontStyle: FontStyle.italic,
                              ),
                            ),
                          ],
                        ),
                      ),
                      
                      const SizedBox(height: 40),
                      
                      // 🎀 ペルソナプレビュー
                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.6),
                          borderRadius: BorderRadius.circular(20),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.blue.shade100.withOpacity(0.3),
                              blurRadius: 10,
                              offset: const Offset(0, 4),
                            ),
                          ],
                        ),
                        child: const Column(
                          children: [
                            Text(
                              '20ペルソナ プレビュー',
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.w600,
                                color: Colors.indigo,
                              ),
                            ),
                            SizedBox(height: 12),
                            Wrap(
                              spacing: 8,
                              children: [
                                Text('💕 そよぎ', style: TextStyle(color: Colors.pink)),
                                Text('🎵 美遊', style: TextStyle(color: Colors.purple)),
                                Text('💡 灯理', style: TextStyle(color: Colors.orange)),
                                Text('📊 澄音', style: TextStyle(color: Colors.blue)),
                                Text('🔮 夢灯芯', style: TextStyle(color: Colors.indigo)),
                              ],
                            ),
                            SizedBox(height: 8),
                            Text(
                              '...and 15 more! 💗',
                              style: TextStyle(
                                fontSize: 12,
                                color: Colors.grey,
                                fontStyle: FontStyle.italic,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
      
      // 💗 可愛いフローティングアクションボタン
      floatingActionButton: Container(
        decoration: BoxDecoration(
          gradient: const LinearGradient(
            colors: [Colors.pink, Colors.pinkAccent],
          ),
          borderRadius: BorderRadius.circular(30),
          boxShadow: [
            BoxShadow(
              color: Colors.pink.withOpacity(0.4),
              blurRadius: 15,
              offset: const Offset(0, 8),
            ),
          ],
        ),
        child: FloatingActionButton(
          onPressed: _addHeart,
          backgroundColor: Colors.transparent,
          elevation: 0,
          child: const Icon(
            Icons.favorite,
            color: Colors.white,
            size: 30,
          ),
        ),
      ),
    );
  }
}