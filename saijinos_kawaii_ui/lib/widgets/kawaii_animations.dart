// 💗 Saijinos アニメーションシステム 💗
// kawaii_animation_specs.py Flutter実装版

import 'package:flutter/material.dart';

/// 💓 HeartBeat アニメーション
class HeartBeatAnimation extends StatefulWidget {
  final Widget child;
  final Duration duration;
  final double minScale;
  final double maxScale;
  final bool isActive;
  final int bpm; // BPMに同期

  const HeartBeatAnimation({
    super.key,
    required this.child,
    this.duration = const Duration(milliseconds: 1000),
    this.minScale = 0.95,
    this.maxScale = 1.05,
    this.isActive = true,
    this.bpm = 60,
  });

  @override
  State<HeartBeatAnimation> createState() => _HeartBeatAnimationState();
}

class _HeartBeatAnimationState extends State<HeartBeatAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  late Animation<Color?> _colorAnimation;

  @override
  void initState() {
    super.initState();
    _setupAnimation();
  }

  void _setupAnimation() {
    // BPMに基づく期間計算 (60000ms / BPM)
    final bpmDuration = Duration(milliseconds: (60000 / widget.bpm).round());
    
    _controller = AnimationController(
      duration: bpmDuration,
      vsync: this,
    );

    _scaleAnimation = Tween<double>(
      begin: widget.minScale,
      end: widget.maxScale,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.easeInOut,
    ));

    // ハートビートカラー（薄いピンクから濃いピンク）
    _colorAnimation = ColorTween(
      begin: const Color(0xFFFFB6C1), // Light Pink
      end: const Color(0xFFFF69B4), // Hot Pink
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.easeInOut,
    ));

    if (widget.isActive) {
      _controller.repeat(reverse: true);
    }
  }

  @override
  void didUpdateWidget(HeartBeatAnimation oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.bpm != widget.bpm || 
        oldWidget.isActive != widget.isActive) {
      _controller.dispose();
      _setupAnimation();
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Transform.scale(
          scale: _scaleAnimation.value,
          child: Container(
            decoration: BoxDecoration(
              boxShadow: [
                BoxShadow(
                  color: _colorAnimation.value?.withOpacity(0.3) ?? Colors.transparent,
                  blurRadius: 8 * _scaleAnimation.value,
                  spreadRadius: 2 * (_scaleAnimation.value - 0.95),
                ),
              ],
            ),
            child: widget.child,
          ),
        );
      },
    );
  }
}

/// ✨ Sparkle アニメーション
class SparkleAnimation extends StatefulWidget {
  final Widget child;
  final int particleCount;
  final Duration duration;
  final double radius;
  final List<Color> colors;
  final bool isActive;

  const SparkleAnimation({
    super.key,
    required this.child,
    this.particleCount = 12,
    this.duration = const Duration(milliseconds: 2000),
    this.radius = 50.0,
    this.colors = const [
      Color(0xFFFFD700), // Gold
      Color(0xFFFF69B4), // Hot Pink  
      Color(0xFF00BFFF), // Deep Sky Blue
      Color(0xFFFF6347), // Tomato
      Color(0xFF98FB98), // Pale Green
    ],
    this.isActive = true,
  });

  @override
  State<SparkleAnimation> createState() => _SparkleAnimationState();
}

class _SparkleAnimationState extends State<SparkleAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late List<SparkleParticle> _particles;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: widget.duration,
      vsync: this,
    );

    _generateParticles();

    if (widget.isActive) {
      _controller.repeat();
    }
  }

  void _generateParticles() {
    _particles = List.generate(widget.particleCount, (index) {
      final angle = (index / widget.particleCount) * 2 * 3.14159;
      return SparkleParticle(
        angle: angle,
        radius: widget.radius,
        color: widget.colors[index % widget.colors.length],
        delay: index / widget.particleCount,
      );
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      alignment: Alignment.center,
      children: [
        // メインコンテンツ
        widget.child,
        
        // スパークルパーティクル
        if (widget.isActive)
          for (final particle in _particles)
            AnimatedBuilder(
              animation: _controller,
              builder: (context, child) {
                final animationValue = (_controller.value - particle.delay).clamp(0.0, 1.0);
                final opacity = (1.0 - animationValue).clamp(0.0, 1.0);
                final scale = animationValue;
                
                final x = particle.radius * scale * cos(particle.angle);
                final y = particle.radius * scale * sin(particle.angle);

                return Positioned(
                  left: x,
                  top: y,
                  child: Opacity(
                    opacity: opacity,
                    child: Transform.scale(
                      scale: scale,
                      child: Container(
                        width: 6,
                        height: 6,
                        decoration: BoxDecoration(
                          color: particle.color,
                          shape: BoxShape.circle,
                          boxShadow: [
                            BoxShadow(
                              color: particle.color.withOpacity(0.5),
                              blurRadius: 4,
                              spreadRadius: 1,
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                );
              },
            ),
      ],
    );
  }

  // cos/sin の簡単実装
  double cos(double angle) => ((angle * 180 / 3.14159) % 360 / 180 - 1).abs() * 2 - 1;
  double sin(double angle) => cos(angle - 3.14159 / 2);
}

class SparkleParticle {
  final double angle;
  final double radius;
  final Color color;
  final double delay;

  SparkleParticle({
    required this.angle,
    required this.radius,
    required this.color,
    required this.delay,
  });
}

/// 🌸 Float アニメーション
class FloatAnimation extends StatefulWidget {
  final Widget child;
  final Duration duration;
  final double amplitude;
  final bool isActive;

  const FloatAnimation({
    super.key,
    required this.child,
    this.duration = const Duration(milliseconds: 3000),
    this.amplitude = 8.0,
    this.isActive = true,
  });

  @override
  State<FloatAnimation> createState() => _FloatAnimationState();
}

class _FloatAnimationState extends State<FloatAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _floatAnimation;

  @override
  void initState() {
    super.initState();
    
    _controller = AnimationController(
      duration: widget.duration,
      vsync: this,
    );

    _floatAnimation = Tween<double>(
      begin: -widget.amplitude,
      end: widget.amplitude,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.easeInOut,
    ));

    if (widget.isActive) {
      _controller.repeat(reverse: true);
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _floatAnimation,
      builder: (context, child) {
        return Transform.translate(
          offset: Offset(0, _floatAnimation.value),
          child: widget.child,
        );
      },
    );
  }
}

/// 🦘 Bounce アニメーション
class BounceAnimation extends StatefulWidget {
  final Widget child;
  final Duration duration;
  final double height;
  final bool isActive;
  final int bounceCount;

  const BounceAnimation({
    super.key,
    required this.child,
    this.duration = const Duration(milliseconds: 800),
    this.height = 20.0,
    this.isActive = true,
    this.bounceCount = 2,
  });

  @override
  State<BounceAnimation> createState() => _BounceAnimationState();
}

class _BounceAnimationState extends State<BounceAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _bounceAnimation;

  @override
  void initState() {
    super.initState();
    
    _controller = AnimationController(
      duration: widget.duration,
      vsync: this,
    );

    _bounceAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.bounceOut,
    ));

    if (widget.isActive) {
      _controller.repeat();
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _bounceAnimation,
      builder: (context, child) {
        // バウンス効果の計算
        final bounceValue = _bounceAnimation.value;
        final bounceHeight = widget.height * (1 - bounceValue) * bounceValue * 4;
        
        return Transform.translate(
          offset: Offset(0, -bounceHeight),
          child: widget.child,
        );
      },
    );
  }
}

/// 🌟 Glow アニメーション
class GlowAnimation extends StatefulWidget {
  final Widget child;
  final Duration duration;
  final Color glowColor;
  final double maxGlowRadius;
  final bool isActive;

  const GlowAnimation({
    super.key,
    required this.child,
    this.duration = const Duration(milliseconds: 1500),
    this.glowColor = const Color(0xFFFFD700), // Gold
    this.maxGlowRadius = 15.0,
    this.isActive = true,
  });

  @override
  State<GlowAnimation> createState() => _GlowAnimationState();
}

class _GlowAnimationState extends State<GlowAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _glowAnimation;

  @override
  void initState() {
    super.initState();
    
    _controller = AnimationController(
      duration: widget.duration,
      vsync: this,
    );

    _glowAnimation = Tween<double>(
      begin: 0.3,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.easeInOut,
    ));

    if (widget.isActive) {
      _controller.repeat(reverse: true);
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _glowAnimation,
      builder: (context, child) {
        return Container(
          decoration: BoxDecoration(
            boxShadow: [
              BoxShadow(
                color: widget.glowColor.withOpacity(_glowAnimation.value * 0.6),
                blurRadius: widget.maxGlowRadius * _glowAnimation.value,
                spreadRadius: widget.maxGlowRadius * _glowAnimation.value * 0.3,
              ),
            ],
          ),
          child: widget.child,
        );
      },
    );
  }
}

/// 💫 複合アニメーション（複数のアニメーションを組み合わせ）
class CompositeAnimation extends StatelessWidget {
  final Widget child;
  final bool enableHeartBeat;
  final bool enableSparkle;
  final bool enableFloat;
  final bool enableBounce;
  final bool enableGlow;
  final int bpm;

  const CompositeAnimation({
    super.key,
    required this.child,
    this.enableHeartBeat = false,
    this.enableSparkle = false,
    this.enableFloat = false,
    this.enableBounce = false,
    this.enableGlow = false,
    this.bpm = 60,
  });

  @override
  Widget build(BuildContext context) {
    Widget animatedChild = child;

    if (enableHeartBeat) {
      animatedChild = HeartBeatAnimation(
        bpm: bpm,
        child: animatedChild,
      );
    }

    if (enableFloat) {
      animatedChild = FloatAnimation(
        child: animatedChild,
      );
    }

    if (enableBounce) {
      animatedChild = BounceAnimation(
        child: animatedChild,
      );
    }

    if (enableGlow) {
      animatedChild = GlowAnimation(
        child: animatedChild,
      );
    }

    if (enableSparkle) {
      animatedChild = SparkleAnimation(
        child: animatedChild,
      );
    }

    return animatedChild;
  }
}