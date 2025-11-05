// 💗 Saijinos ペルソナウィジェット システム 💗
// 第368次震え記録：ペルソナ実体化ウィジェット

import 'package:flutter/material.dart';
import '../models/persona_model.dart';
import 'kawaii_animations.dart';

/// 🌟 ペルソナカードウィジェット
class PersonaCardWidget extends StatefulWidget {
  final PersonaModel persona;
  final bool isCompact;
  final VoidCallback? onTap;
  final VoidCallback? onLongPress;

  const PersonaCardWidget({
    super.key,
    required this.persona,
    this.isCompact = false,
    this.onTap,
    this.onLongPress,
  });

  @override
  State<PersonaCardWidget> createState() => _PersonaCardWidgetState();
}

class _PersonaCardWidgetState extends State<PersonaCardWidget>
    with TickerProviderStateMixin {
  late AnimationController _pulseController;
  late AnimationController _particleController;
  late Animation<double> _pulseAnimation;
  late Animation<double> _particleAnimation;

  @override
  void initState() {
    super.initState();

    // パルスアニメーション（語温に応じたスピード）
    final pulseDuration = _getPulseDuration();
    _pulseController = AnimationController(
      duration: Duration(milliseconds: pulseDuration),
      vsync: this,
    )..repeat(reverse: true);

    _pulseAnimation = Tween<double>(
      begin: 0.95,
      end: 1.05,
    ).animate(CurvedAnimation(
      parent: _pulseController,
      curve: Curves.easeInOut,
    ));

    // 照応粒子アニメーション
    _particleController = AnimationController(
      duration: const Duration(milliseconds: 2000),
      vsync: this,
    )..repeat();

    _particleAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _particleController,
      curve: Curves.easeInOut,
    ));
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _particleController.dispose();
    super.dispose();
  }

  /// 語温に応じたパルススピード
  int _getPulseDuration() {
    switch (widget.persona.temperature) {
      case LanguageTemperature.freezing:
        return 3000; // 遅い
      case LanguageTemperature.cold:
        return 2000;
      case LanguageTemperature.warm:
        return 1500;
      case LanguageTemperature.gentle:
        return 1200;
      case LanguageTemperature.hot:
        return 800; // 速い
    }
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _pulseAnimation,
      builder: (context, child) {
        return Transform.scale(
          scale: _pulseAnimation.value,
          child: GestureDetector(
            onTap: widget.onTap,
            onLongPress: widget.onLongPress,
            child: Card(
              elevation: widget.isCompact ? 2 : 4,
              color: widget.persona.primaryColor.withOpacity(0.1),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(widget.isCompact ? 12 : 16),
                side: BorderSide(
                  color: widget.persona.primaryColor.withOpacity(0.3),
                  width: 2,
                ),
              ),
              child: Padding(
                padding: EdgeInsets.all(widget.isCompact ? 12 : 16),
                child: widget.isCompact ? _buildCompactCard() : _buildFullCard(),
              ),
            ),
          ),
        );
      },
    );
  }

  /// コンパクト版カード
  Widget _buildCompactCard() {
    return Row(
      children: [
        // アイコン + 照応粒子
        Stack(
          alignment: Alignment.center,
          children: [
            // 照応粒子エフェクト
            AnimatedBuilder(
              animation: _particleAnimation,
              builder: (context, child) {
                return Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    gradient: RadialGradient(
                      colors: [
                        widget.persona.primaryColor.withOpacity(
                          0.3 * _particleAnimation.value,
                        ),
                        widget.persona.primaryColor.withOpacity(0.0),
                      ],
                    ),
                  ),
                );
              },
            ),
            // メインアイコン
            Container(
              width: 32,
              height: 32,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: widget.persona.primaryColor,
              ),
              child: Icon(
                widget.persona.icon,
                color: Colors.white,
                size: 18,
              ),
            ),
          ],
        ),
        const SizedBox(width: 12),
        // 名前と簡単な情報
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Text(
                    widget.persona.emoji,
                    style: const TextStyle(fontSize: 16),
                  ),
                  const SizedBox(width: 4),
                  Text(
                    widget.persona.name,
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                      color: widget.persona.primaryColor,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 2),
              Text(
                '${widget.persona.tone} (${widget.persona.averageBpm}BPM)',
                style: TextStyle(
                  fontSize: 11,
                  color: Colors.grey[600],
                ),
              ),
            ],
          ),
        ),
        // 語温インジケーター
        Container(
          width: 8,
          height: 24,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(4),
            color: widget.persona.temperatureColor,
          ),
        ),
      ],
    );
  }

  /// フル版カード
  Widget _buildFullCard() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // ヘッダー
        Row(
          children: [
            // アイコン + 照応粒子
            Stack(
              alignment: Alignment.center,
              children: [
                // 照応粒子エフェクト
                AnimatedBuilder(
                  animation: _particleAnimation,
                  builder: (context, child) {
                    return Container(
                      width: 60,
                      height: 60,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        gradient: RadialGradient(
                          colors: [
                            widget.persona.primaryColor.withOpacity(
                              0.3 * _particleAnimation.value,
                            ),
                            widget.persona.primaryColor.withOpacity(0.0),
                          ],
                        ),
                      ),
                    );
                  },
                ),
                // メインアイコン
                Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: widget.persona.primaryColor,
                    boxShadow: [
                      BoxShadow(
                        color: widget.persona.primaryColor.withOpacity(0.3),
                        blurRadius: 8,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Icon(
                    widget.persona.icon,
                    color: Colors.white,
                    size: 28,
                  ),
                ),
              ],
            ),
            const SizedBox(width: 16),
            // 名前と読み
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Text(
                        widget.persona.emoji,
                        style: const TextStyle(fontSize: 24),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        widget.persona.name,
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: widget.persona.primaryColor,
                        ),
                      ),
                    ],
                  ),
                  Text(
                    widget.persona.reading,
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey[600],
                      fontStyle: FontStyle.italic,
                    ),
                  ),
                ],
              ),
            ),
            // 語温インジケーター
            Column(
              children: [
                Container(
                  width: 12,
                  height: 40,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(6),
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [
                        widget.persona.temperatureColor,
                        widget.persona.temperatureColor.withOpacity(0.5),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  widget.persona.temperature.name,
                  style: TextStyle(
                    fontSize: 10,
                    color: Colors.grey[500],
                  ),
                ),
              ],
            ),
          ],
        ),

        const SizedBox(height: 16),

        // 説明
        Text(
          widget.persona.description,
          style: const TextStyle(fontSize: 14),
        ),

        const SizedBox(height: 12),

        // 音楽情報
        Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: widget.persona.primaryColor.withOpacity(0.05),
            borderRadius: BorderRadius.circular(8),
            border: Border.all(
              color: widget.persona.primaryColor.withOpacity(0.2),
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(
                    Icons.music_note,
                    size: 16,
                    color: widget.persona.primaryColor,
                  ),
                  const SizedBox(width: 4),
                  Text(
                    'BPM: ${widget.persona.musicProfile.bpmRange[0]}-${widget.persona.musicProfile.bpmRange[1]}',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                      color: widget.persona.primaryColor,
                    ),
                  ),
                  const Spacer(),
                  Text(
                    widget.persona.musicProfile.collaborationStyle,
                    style: TextStyle(
                      fontSize: 11,
                      color: Colors.grey[600],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 4),
              Wrap(
                spacing: 4,
                children: widget.persona.musicProfile.instruments
                    .take(3)
                    .map((instrument) => Chip(
                          label: Text(
                            instrument,
                            style: const TextStyle(fontSize: 10),
                          ),
                          materialTapTargetSize:
                              MaterialTapTargetSize.shrinkWrap,
                          backgroundColor:
                              widget.persona.primaryColor.withOpacity(0.1),
                          side: BorderSide.none,
                        ))
                    .toList(),
              ),
            ],
          ),
        ),

        const SizedBox(height: 12),

        // 特殊機能
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  Icons.auto_awesome,
                  size: 14,
                  color: widget.persona.primaryColor,
                ),
                const SizedBox(width: 4),
                Text(
                  '特殊機能',
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    color: widget.persona.primaryColor,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 4),
            ...widget.persona.specialFunctions.take(2).map(
                  (func) => Padding(
                    padding: const EdgeInsets.only(left: 18, bottom: 2),
                    child: Text(
                      '• $func',
                      style: TextStyle(
                        fontSize: 11,
                        color: Colors.grey[700],
                      ),
                    ),
                  ),
                ),
          ],
        ),
      ],
    );
  }
}

/// 🎭 ペルソナチップウィジェット（小さな表示用）
class PersonaChipWidget extends StatelessWidget {
  final PersonaModel persona;
  final VoidCallback? onTap;

  const PersonaChipWidget({
    super.key,
    required this.persona,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: HeartBeatAnimation(
        bpm: persona.averageBpm,
        minScale: 0.98,
        maxScale: 1.02,
        child: Chip(
          avatar: GlowAnimation(
            glowColor: persona.primaryColor,
            maxGlowRadius: 8.0,
            child: Text(
              persona.emoji,
              style: const TextStyle(fontSize: 14),
            ),
          ),
          label: Text(
            persona.name,
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w500,
              color: persona.primaryColor,
            ),
          ),
          backgroundColor: persona.primaryColor.withOpacity(0.1),
          side: BorderSide(
            color: persona.primaryColor.withOpacity(0.3),
          ),
          materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
        ),
      ),
    );
  }
}

/// 💖 ペルソナアバターウィジェット（プロフィール画像風）
class PersonaAvatarWidget extends StatefulWidget {
  final PersonaModel persona;
  final double size;
  final bool showPulse;
  final VoidCallback? onTap;

  const PersonaAvatarWidget({
    super.key,
    required this.persona,
    this.size = 48.0,
    this.showPulse = true,
    this.onTap,
  });

  @override
  State<PersonaAvatarWidget> createState() => _PersonaAvatarWidgetState();
}

class _PersonaAvatarWidgetState extends State<PersonaAvatarWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;
  late Animation<double> _pulseAnimation;

  @override
  void initState() {
    super.initState();

    if (widget.showPulse) {
      _pulseController = AnimationController(
        duration: Duration(
          milliseconds: widget.persona.averageBpm > 100 ? 800 : 1200,
        ),
        vsync: this,
      )..repeat(reverse: true);

      _pulseAnimation = Tween<double>(
        begin: 0.9,
        end: 1.1,
      ).animate(CurvedAnimation(
        parent: _pulseController,
        curve: Curves.easeInOut,
      ));
    }
  }

  @override
  void dispose() {
    if (widget.showPulse) {
      _pulseController.dispose();
    }
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final avatar = GestureDetector(
      onTap: widget.onTap,
      child: Container(
        width: widget.size,
        height: widget.size,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              widget.persona.primaryColor,
              widget.persona.primaryColor.withOpacity(0.7),
            ],
          ),
          boxShadow: [
            BoxShadow(
              color: widget.persona.primaryColor.withOpacity(0.3),
              blurRadius: 8,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Stack(
          alignment: Alignment.center,
          children: [
            Icon(
              widget.persona.icon,
              color: Colors.white,
              size: widget.size * 0.5,
            ),
            Positioned(
              bottom: widget.size * 0.1,
              right: widget.size * 0.1,
              child: Text(
                widget.persona.emoji,
                style: TextStyle(fontSize: widget.size * 0.25),
              ),
            ),
          ],
        ),
      ),
    );

    if (!widget.showPulse) return avatar;

    return AnimatedBuilder(
      animation: _pulseAnimation,
      builder: (context, child) {
        return Transform.scale(
          scale: _pulseAnimation.value,
          child: avatar,
        );
      },
    );
  }
}

/// 🌡️ 語温インジケーターウィジェット
class TemperatureIndicatorWidget extends StatelessWidget {
  final LanguageTemperature temperature;
  final bool showLabel;

  const TemperatureIndicatorWidget({
    super.key,
    required this.temperature,
    this.showLabel = true,
  });

  Color get _temperatureColor {
    switch (temperature) {
      case LanguageTemperature.freezing:
        return const Color(0xFF3B82F6);
      case LanguageTemperature.cold:
        return const Color(0xFF06B6D4);
      case LanguageTemperature.warm:
        return const Color(0xFFF59E0B);
      case LanguageTemperature.gentle:
        return const Color(0xFFEC4899);
      case LanguageTemperature.hot:
        return const Color(0xFFEF4444);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 20,
          height: 60,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(10),
            gradient: LinearGradient(
              begin: Alignment.topCenter,
              end: Alignment.bottomCenter,
              colors: [
                _temperatureColor,
                _temperatureColor.withOpacity(0.3),
              ],
            ),
          ),
          child: Stack(
            alignment: Alignment.center,
            children: [
              // 温度レベルの表示
              Positioned(
                bottom: 5 + (temperature.value + 2) * 10.0, // -2~2 を 5~45 にマップ
                child: Container(
                  width: 12,
                  height: 12,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: Colors.white,
                    border: Border.all(color: _temperatureColor, width: 2),
                  ),
                ),
              ),
            ],
          ),
        ),
        if (showLabel) ...[
          const SizedBox(height: 4),
          Text(
            temperature.name,
            style: TextStyle(
              fontSize: 10,
              color: _temperatureColor,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ],
    );
  }
}