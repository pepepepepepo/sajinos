// 💗 Saijinos 簡単ペルソナパネル 💗
// エラー回避版・基本機能のみ

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/app_providers.dart';
import '../models/persona_model.dart';

/// 🎭 簡単ペルソナパネル
class PersonaPanelWidget extends StatelessWidget {
  const PersonaPanelWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return Consumer<UIStateProvider>(
      builder: (context, uiProvider, child) {
        if (!uiProvider.showPersonaPanel) return const SizedBox.shrink();

        return Container(
          height: 300,
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
                    Consumer<ThemeProvider>(
                      builder: (context, themeProvider, child) {
                        return Text(
                          themeProvider.isKawaiiMode 
                            ? '💕 ペルソナコレクション'
                            : '🤖 AI ペルソナシステム',
                          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                        );
                      },
                    ),
                    const Spacer(),
                    Consumer<PersonaProvider>(
                      builder: (context, personaProvider, child) {
                        return Text(
                          '${personaProvider.allPersonas.length}体',
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            color: Theme.of(context).colorScheme.outline,
                          ),
                        );
                      },
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
                child: Consumer<PersonaProvider>(
                  builder: (context, personaProvider, child) {
                    final personas = personaProvider.allPersonas;
                    
                    return ListView.builder(
                      padding: const EdgeInsets.all(16),
                      itemCount: personas.length,
                      itemBuilder: (context, index) {
                        final persona = personas[index];
                        final isActive = personaProvider.activePersona?.id == persona.id;

                        return Container(
                          margin: const EdgeInsets.only(bottom: 12),
                          child: ListTile(
                            leading: Container(
                              width: 48,
                              height: 48,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                color: persona.primaryColor,
                              ),
                              child: Center(
                                child: Text(
                                  persona.emoji,
                                  style: const TextStyle(fontSize: 20),
                                ),
                              ),
                            ),
                            title: Text(
                              persona.name,
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                color: isActive ? persona.primaryColor : null,
                              ),
                            ),
                            subtitle: Text('${persona.tone} (${persona.averageBpm}BPM)'),
                            trailing: isActive 
                              ? Icon(Icons.check, color: persona.primaryColor)
                              : null,
                            onTap: () {
                              personaProvider.setActivePersona(persona);
                              
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
                            },
                            tileColor: isActive 
                              ? persona.primaryColor.withOpacity(0.1)
                              : null,
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                              side: isActive 
                                ? BorderSide(color: persona.primaryColor, width: 2)
                                : BorderSide.none,
                            ),
                          ),
                        );
                      },
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}