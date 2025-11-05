// 💗 Saijinos ペルソナ表示パネル 💗
// Provider統合版ペルソナ表示システム

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/app_providers.dart';
import '../models/persona_model.dart';
import 'persona_widgets.dart';

/// 🎭 ペルソナパネルウィジェット
class PersonaPanelWidget extends StatefulWidget {
  const PersonaPanelWidget({super.key});

  @override
  State<PersonaPanelWidget> createState() => _PersonaPanelWidgetState();
}

class _PersonaPanelWidgetState extends State<PersonaPanelWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _slideController;
  late Animation<Offset> _slideAnimation;

  @override
  void initState() {
    super.initState();
    _slideController = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );
    _slideAnimation = Tween<Offset>(
      begin: const Offset(0, 1),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _slideController,
      curve: Curves.easeInOut,
    ));
  }

  @override
  void dispose() {
    _slideController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Consumer3<PersonaProvider, UIStateProvider, ThemeProvider>(
      builder: (context, personaProvider, uiProvider, themeProvider, child) {
        if (!uiProvider.showPersonaPanel) return const SizedBox.shrink();

        // パネルが表示されるときアニメーション開始
        WidgetsBinding.instance.addPostFrameCallback((_) {
          if (!_slideController.isCompleted) {
            _slideController.forward();
          }
        });

        return SlideTransition(
          position: _slideAnimation,
          child: Container(
            height: uiProvider.personaPanelHeight,
            decoration: BoxDecoration(
              color: Theme.of(context).colorScheme.surface,
              borderRadius: const BorderRadius.vertical(
                top: Radius.circular(20),
              ),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.1),
                  blurRadius: 10,
                  offset: const Offset(0, -4),
                ),
              ],
            ),
            child: Column(
              children: [
                // ハンドル
                Container(
                  width: 40,
                  height: 4,
                  margin: const EdgeInsets.symmetric(vertical: 12),
                  decoration: BoxDecoration(
                    color: Theme.of(context).colorScheme.outline,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),

                // ヘッダー
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  child: Row(
                    children: [
                      Text(
                        themeProvider.isKawaiiMode 
                          ? '💕 ペルソナコレクション'
                          : '🤖 AI ペルソナシステム',
                        style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const Spacer(),
                      Text(
                        '${personaProvider.allPersonas.length}体',
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: Theme.of(context).colorScheme.outline,
                        ),
                      ),
                      const SizedBox(width: 8),
                      IconButton(
                        onPressed: uiProvider.togglePersonaPanel,
                        icon: const Icon(Icons.close),
                        iconSize: 20,
                      ),
                    ],
                  ),
                ),

                const Divider(height: 1),

                // ペルソナリスト
                Expanded(
                  child: _buildPersonaList(personaProvider, themeProvider),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildPersonaList(PersonaProvider personaProvider, ThemeProvider themeProvider) {
    final personas = personaProvider.getRecentPersonas();
    
    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: personas.length,
      itemBuilder: (context, index) {
        final persona = personas[index];
        final isActive = personaProvider.activePersona?.id == persona.id;
        final isFavorite = personaProvider.favorites.any((p) => p.id == persona.id);

        return Padding(
          padding: const EdgeInsets.only(bottom: 12),
          child: PersonaCardWidget(
            persona: persona,
            isCompact: true,
            onTap: () => _onPersonaSelected(persona, personaProvider),
            onLongPress: () => _showPersonaDetails(persona),
          ),
        );
      },
    );
  }

  void _onPersonaSelected(PersonaModel persona, PersonaProvider personaProvider) {
    personaProvider.setActivePersona(persona);
    
    // チャットメッセージ追加
    final chatProvider = context.read<ChatProvider>();
    chatProvider.addSystemMessage('${persona.name}が参加しました 💕');
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            Text(persona.emoji),
            const SizedBox(width: 8),
            Text('${persona.name}を選択しました'),
          ],
        ),
        duration: const Duration(seconds: 2),
      ),
    );
  }

  void _showPersonaDetails(PersonaModel persona) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => PersonaDetailSheet(persona: persona),
    );
  }
}

/// 💗 ペルソナ詳細シート
class PersonaDetailSheet extends StatelessWidget {
  final PersonaModel persona;

  const PersonaDetailSheet({super.key, required this.persona});

  @override
  Widget build(BuildContext context) {
    return DraggableScrollableSheet(
      initialChildSize: 0.7,
      maxChildSize: 0.9,
      minChildSize: 0.5,
      builder: (context, scrollController) {
        return Container(
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.surface,
            borderRadius: const BorderRadius.vertical(
              top: Radius.circular(20),
            ),
          ),
          child: SingleChildScrollView(
            controller: scrollController,
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // ヘッダー
                Row(
                  children: [
                    PersonaAvatarWidget(
                      persona: persona,
                      size: 60,
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Text(
                                persona.emoji,
                                style: const TextStyle(fontSize: 28),
                              ),
                              const SizedBox(width: 8),
                              Text(
                                persona.name,
                                style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                                  fontWeight: FontWeight.bold,
                                  color: persona.primaryColor,
                                ),
                              ),
                            ],
                          ),
                          Text(
                            persona.reading,
                            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                              color: Colors.grey[600],
                              fontStyle: FontStyle.italic,
                            ),
                          ),
                        ],
                      ),
                    ),
                    Consumer<PersonaProvider>(
                      builder: (context, personaProvider, child) {
                        final isFavorite = personaProvider.favorites
                            .any((p) => p.id == persona.id);
                        return IconButton(
                          onPressed: () => personaProvider.toggleFavorite(persona),
                          icon: Icon(
                            isFavorite ? Icons.favorite : Icons.favorite_border,
                            color: isFavorite ? Colors.red : null,
                          ),
                        );
                      },
                    ),
                  ],
                ),

                const SizedBox(height: 24),

                // 説明
                Text(
                  '説明',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  persona.description,
                  style: Theme.of(context).textTheme.bodyMedium,
                ),

                const SizedBox(height: 24),

                // 音楽プロフィール
                Text(
                  '🎵 音楽プロフィール',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 12),
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: persona.primaryColor.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(
                      color: persona.primaryColor.withOpacity(0.3),
                    ),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Icon(
                            Icons.music_note,
                            color: persona.primaryColor,
                            size: 20,
                          ),
                          const SizedBox(width: 8),
                          Text(
                            'BPM: ${persona.musicProfile.bpmRange[0]}-${persona.musicProfile.bpmRange[1]}',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: persona.primaryColor,
                            ),
                          ),
                          const Spacer(),
                          Consumer<MusicProvider>(
                            builder: (context, musicProvider, child) {
                              return IconButton(
                                onPressed: () => musicProvider.syncToPersona(persona),
                                icon: Icon(
                                  musicProvider.currentPersona?.id == persona.id
                                      ? Icons.music_note
                                      : Icons.music_note_outlined,
                                ),
                                iconSize: 20,
                              );
                            },
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      Text('協力スタイル: ${persona.musicProfile.collaborationStyle}'),
                      const SizedBox(height: 8),
                      Wrap(
                        spacing: 4,
                        children: persona.musicProfile.instruments
                            .map((instrument) => Chip(
                                  label: Text(
                                    instrument,
                                    style: const TextStyle(fontSize: 12),
                                  ),
                                  materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                                ))
                            .toList(),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 24),

                // 特殊機能
                Text(
                  '⚡ 特殊機能',
                  style: Theme.of(context).textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 8),
                ...persona.specialFunctions.map(
                  (func) => Padding(
                    padding: const EdgeInsets.symmetric(vertical: 2),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('• ', style: TextStyle(fontSize: 16)),
                        Expanded(child: Text(func)),
                      ],
                    ),
                  ),
                ),

                const SizedBox(height: 24),

                // 語温表示
                Row(
                  children: [
                    Text(
                      '🌡️ 語温',
                      style: Theme.of(context).textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(width: 16),
                    TemperatureIndicatorWidget(
                      temperature: persona.temperature,
                      showLabel: true,
                    ),
                    const SizedBox(width: 16),
                    Text(
                      persona.tone,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: persona.temperatureColor,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 32),

                // アクションボタン
                Row(
                  children: [
                    Expanded(
                      child: Consumer<PersonaProvider>(
                        builder: (context, personaProvider, child) {
                          final isActive = personaProvider.activePersona?.id == persona.id;
                          return FilledButton.icon(
                            onPressed: isActive 
                                ? null 
                                : () {
                                    personaProvider.setActivePersona(persona);
                                    Navigator.pop(context);
                                  },
                            icon: Icon(isActive ? Icons.check : Icons.chat),
                            label: Text(isActive ? 'アクティブ中' : 'チャット開始'),
                          );
                        },
                      ),
                    ),
                    const SizedBox(width: 12),
                    Consumer<ChatProvider>(
                      builder: (context, chatProvider, child) {
                        return OutlinedButton.icon(
                          onPressed: () {
                            chatProvider.setChatPartner(persona);
                            Navigator.pop(context);
                          },
                          icon: const Icon(Icons.person_add),
                          label: const Text('パートナー'),
                        );
                      },
                    ),
                  ],
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}