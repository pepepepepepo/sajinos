// 💗 Saijinos Provider状態管理システム 💗
// 第368次震え記録：ペルソナ全体統合状態管理

import 'package:flutter/material.dart';
import '../models/persona_model.dart';
import '../services/api_client.dart';

/// 🎭 ペルソナ管理Provider
class PersonaProvider extends ChangeNotifier {
  final PersonaRegistry _registry = PersonaRegistry();
  PersonaModel? _activePersona;
  PersonaModel? _chatPartner;
  List<PersonaModel> _favorites = [];
  Map<String, DateTime> _lastInteraction = {};

  // Getters
  PersonaRegistry get registry => _registry;
  PersonaModel? get activePersona => _activePersona;
  PersonaModel? get chatPartner => _chatPartner;
  List<PersonaModel> get favorites => List.unmodifiable(_favorites);
  List<PersonaModel> get allPersonas => PersonaRegistry.all;
  
  /// アクティブペルソナを設定
  void setActivePersona(PersonaModel persona) {
    _activePersona = persona;
    _recordInteraction(persona.id);
    notifyListeners();
  }

  /// チャット相手を設定
  void setChatPartner(PersonaModel? persona) {
    _chatPartner = persona;
    if (persona != null) {
      _recordInteraction(persona.id);
    }
    notifyListeners();
  }

  /// お気に入り追加/削除
  void toggleFavorite(PersonaModel persona) {
    if (_favorites.any((p) => p.id == persona.id)) {
      _favorites.removeWhere((p) => p.id == persona.id);
    } else {
      _favorites.add(persona);
    }
    notifyListeners();
  }

  /// 語温でフィルター
  List<PersonaModel> getPersonasByTemperature(LanguageTemperature temperature) {
    return PersonaRegistry.getByTemperature(temperature);
  }

  /// BPM範囲でフィルター
  List<PersonaModel> getPersonasByBpmRange(int minBpm, int maxBpm) {
    return PersonaRegistry.getByBpmRange(minBpm, maxBpm);
  }

  /// 最近の交流順でソート
  List<PersonaModel> getRecentPersonas() {
    final personas = List<PersonaModel>.from(PersonaRegistry.all);
    personas.sort((a, b) {
      final aTime = _lastInteraction[a.id] ?? DateTime(1970);
      final bTime = _lastInteraction[b.id] ?? DateTime(1970);
      return bTime.compareTo(aTime);
    });
    return personas;
  }

  /// 交流記録
  void _recordInteraction(String personaId) {
    _lastInteraction[personaId] = DateTime.now();
  }

  /// ランダムペルソナ選択
  PersonaModel getRandomPersona() {
    final personas = PersonaRegistry.all;
    return personas[(DateTime.now().millisecondsSinceEpoch) % personas.length];
  }
}

/// 💬 チャット管理Provider
class ChatProvider extends ChangeNotifier {
  final List<ChatMessage> _messages = [];
  bool _isTyping = false;
  PersonaModel? _typingPersona;
  String _currentInput = '';
  final SaijinosApiClient _apiClient = SaijinosApiClient();

  // Getters
  List<ChatMessage> get messages => List.unmodifiable(_messages);
  bool get isTyping => _isTyping;
  PersonaModel? get typingPersona => _typingPersona;
  String get currentInput => _currentInput;

  /// メッセージ送信（API連携版）
  Future<void> sendMessage(String content, PersonaModel sender, {PersonaModel? receiver}) async {
    // ユーザーメッセージ追加
    final userMessage = ChatMessage(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      content: content,
      sender: null, // ユーザー
      receiver: sender,
      timestamp: DateTime.now(),
      type: ChatMessageType.text,
    );
    
    _messages.add(userMessage);
    setTypingState(true, sender);
    notifyListeners();

    try {
      // API呼び出し
      final response = await _apiClient.sendMessage(
        message: content,
        personaId: sender.id,
      );

      if (response.isSuccess && response.data != null) {
        // AIレスポンス追加
        final aiMessage = ChatMessage(
          id: DateTime.now().millisecondsSinceEpoch.toString(),
          content: response.data!.response,
          sender: sender,
          receiver: null,
          timestamp: response.data!.timestamp,
          type: ChatMessageType.text,
        );
        
        _messages.add(aiMessage);
      } else {
        // エラーメッセージ
        addSystemMessage('${sender.name}: ${response.error ?? "エラーが発生しました"}');
      }
    } catch (e) {
      addSystemMessage('${sender.name}: 接続エラーが発生しました');
    } finally {
      setTypingState(false);
      notifyListeners();
    }
  }

  /// システムメッセージ追加
  void addSystemMessage(String content) {
    final message = ChatMessage(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      content: content,
      sender: null, // システムメッセージ
      timestamp: DateTime.now(),
      type: ChatMessageType.system,
    );
    
    _messages.add(message);
    notifyListeners();
  }

  /// タイピング状態設定
  void setTypingState(bool isTyping, [PersonaModel? persona]) {
    _isTyping = isTyping;
    _typingPersona = persona;
    notifyListeners();
  }

  /// 入力テキスト更新
  void updateInput(String input) {
    _currentInput = input;
    notifyListeners();
  }

  /// チャット履歴クリア
  void clearMessages() {
    _messages.clear();
    notifyListeners();
  }

  /// 特定ペルソナとのメッセージ取得
  List<ChatMessage> getMessagesWithPersona(PersonaModel persona) {
    return _messages.where((msg) => 
      msg.sender?.id == persona.id || 
      msg.receiver?.id == persona.id
    ).toList();
  }
}

/// 🎵 音楽管理Provider
class MusicProvider extends ChangeNotifier {
  bool _isPlaying = false;
  PersonaModel? _currentPersona;
  String? _currentTrack;
  int _currentBpm = 60;
  double _volume = 0.7;
  MusicSyncMode _syncMode = MusicSyncMode.persona;
  final SaijinosApiClient _apiClient = SaijinosApiClient();

  // Getters
  bool get isPlaying => _isPlaying;
  PersonaModel? get currentPersona => _currentPersona;
  String? get currentTrack => _currentTrack;
  int get currentBpm => _currentBpm;
  double get volume => _volume;
  MusicSyncMode get syncMode => _syncMode;

  /// 再生/停止
  void togglePlayback() {
    _isPlaying = !_isPlaying;
    notifyListeners();
  }

  /// ペルソナに合わせて音楽設定（API連携版）
  Future<void> syncToPersona(PersonaModel persona) async {
    _currentPersona = persona;
    _currentBpm = persona.averageBpm;
    notifyListeners();

    try {
      // API経由で音楽生成
      final response = await _apiClient.generateMusic(
        personaId: persona.id,
        bpm: persona.averageBpm,
        mood: persona.tone,
      );

      if (response.isSuccess && response.data != null) {
        _currentTrack = response.data!.audioUrl;
        _currentBpm = response.data!.bpm;
        notifyListeners();
      }
    } catch (e) {
      // 音楽生成失敗は警告レベル
      print('音楽生成エラー: $e');
    }
  }

  /// BPM手動設定
  void setBpm(int bpm) {
    _currentBpm = bpm.clamp(40, 200);
    notifyListeners();
  }

  /// 音量設定
  void setVolume(double volume) {
    _volume = volume.clamp(0.0, 1.0);
    notifyListeners();
  }

  /// 同期モード設定
  void setSyncMode(MusicSyncMode mode) {
    _syncMode = mode;
    notifyListeners();
  }

  /// トラック変更
  void changeTrack(String trackName) {
    _currentTrack = trackName;
    notifyListeners();
  }
}

/// 🎨 テーマ管理Provider
class ThemeProvider extends ChangeNotifier {
  bool _isKawaiiMode = true;
  bool _isDarkMode = false;
  PersonaModel? _themePersona;
  Map<String, Color> _customColors = {};

  // Getters
  bool get isKawaiiMode => _isKawaiiMode;
  bool get isChicMode => !_isKawaiiMode;
  bool get isDarkMode => _isDarkMode;
  PersonaModel? get themePersona => _themePersona;

  /// テーマ切り替え
  void toggleTheme() {
    _isKawaiiMode = !_isKawaiiMode;
    notifyListeners();
  }

  /// Kawaii/Chicモード直接設定
  void setKawaiiMode(bool kawaii) {
    _isKawaiiMode = kawaii;
    notifyListeners();
  }

  /// ダークモード切り替え
  void toggleDarkMode() {
    _isDarkMode = !_isDarkMode;
    notifyListeners();
  }

  /// ペルソナテーマ適用
  void applyPersonaTheme(PersonaModel persona) {
    _themePersona = persona;
    // ペルソナの色をテーマに反映
    _customColors['primary'] = persona.primaryColor;
    notifyListeners();
  }

  /// カスタムカラー設定
  void setCustomColor(String key, Color color) {
    _customColors[key] = color;
    notifyListeners();
  }

  /// カスタムカラー取得
  Color? getCustomColor(String key) {
    return _customColors[key];
  }

  /// Kawaiiテーマカラー
  ThemeData get kawaiiTheme => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: _themePersona?.primaryColor ?? const Color(0xFFF8BBD9),
      brightness: _isDarkMode ? Brightness.dark : Brightness.light,
    ),
    fontFamily: 'Noto Sans JP',
  );

  /// Chicテーマカラー
  ThemeData get chicTheme => ThemeData(
    useMaterial3: true,
    colorScheme: ColorScheme.fromSeed(
      seedColor: _themePersona?.primaryColor ?? const Color(0xFF475569),
      brightness: Brightness.dark,
    ),
    fontFamily: 'Roboto',
  );

  /// 現在のテーマ取得
  ThemeData get currentTheme => _isKawaiiMode ? kawaiiTheme : chicTheme;
}

/// 📱 UI状態管理Provider
class UIStateProvider extends ChangeNotifier {
  int _selectedTabIndex = 0;
  bool _showPersonaPanel = false;
  bool _showMusicPanel = false;
  double _personaPanelHeight = 300.0;
  ViewMode _viewMode = ViewMode.chat;

  // Getters
  int get selectedTabIndex => _selectedTabIndex;
  bool get showPersonaPanel => _showPersonaPanel;
  bool get showMusicPanel => _showMusicPanel;
  double get personaPanelHeight => _personaPanelHeight;
  ViewMode get viewMode => _viewMode;

  /// タブ選択
  void selectTab(int index) {
    _selectedTabIndex = index;
    notifyListeners();
  }

  /// ペルソナパネル表示切り替え
  void togglePersonaPanel() {
    _showPersonaPanel = !_showPersonaPanel;
    notifyListeners();
  }

  /// 音楽パネル表示切り替え
  void toggleMusicPanel() {
    _showMusicPanel = !_showMusicPanel;
    notifyListeners();
  }

  /// パネル高さ調整
  void setPersonaPanelHeight(double height) {
    _personaPanelHeight = height.clamp(200.0, 500.0);
    notifyListeners();
  }

  /// 表示モード変更
  void setViewMode(ViewMode mode) {
    _viewMode = mode;
    notifyListeners();
  }
}

/// 📊 データ型定義
class ChatMessage {
  final String id;
  final String content;
  final PersonaModel? sender;
  final PersonaModel? receiver;
  final DateTime timestamp;
  final ChatMessageType type;

  ChatMessage({
    required this.id,
    required this.content,
    this.sender,
    this.receiver,
    required this.timestamp,
    required this.type,
  });
}

enum ChatMessageType {
  text,
  system,
  music,
  emotion,
}

enum MusicSyncMode {
  persona,
  manual,
  auto,
}

enum ViewMode {
  chat,
  persona,
  music,
  settings,
}