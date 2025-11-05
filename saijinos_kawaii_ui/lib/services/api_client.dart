// 💗 Saijinos FastAPI 連携システム 💗
// FlutterとFastAPIバックエンドを統合

import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/persona_model.dart';

/// 🌐 API設定
class ApiConfig {
  static const String baseUrl = 'http://127.0.0.1:8000';
  static const String apiVersion = '/api/v1';
  static const Duration timeout = Duration(seconds: 30);
  
  static String get apiBaseUrl => '$baseUrl$apiVersion';
}

/// 📡 APIクライアント
class SaijinosApiClient {
  final http.Client _client = http.Client();

  /// 💬 チャット送信
  Future<ApiResponse<ChatResponseData>> sendMessage({
    required String message,
    required String personaId,
    String? conversationId,
  }) async {
    try {
      final response = await _client.post(
        Uri.parse('${ApiConfig.apiBaseUrl}/chat'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: jsonEncode({
          'message': message,
          'persona_id': personaId,
          'conversation_id': conversationId,
          'timestamp': DateTime.now().toIso8601String(),
        }),
      ).timeout(ApiConfig.timeout);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return ApiResponse.success(ChatResponseData.fromJson(data));
      } else {
        return ApiResponse.error('チャットエラー: ${response.statusCode}');
      }
    } catch (e) {
      return ApiResponse.error('ネットワークエラー: $e');
    }
  }

  /// 🎭 ペルソナ情報取得
  Future<ApiResponse<List<PersonaApiData>>> getPersonas() async {
    try {
      final response = await _client.get(
        Uri.parse('${ApiConfig.apiBaseUrl}/personas'),
        headers: {
          'Accept': 'application/json',
        },
      ).timeout(ApiConfig.timeout);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final personas = (data['personas'] as List)
            .map((json) => PersonaApiData.fromJson(json))
            .toList();
        return ApiResponse.success(personas);
      } else {
        return ApiResponse.error('ペルソナ取得エラー: ${response.statusCode}');
      }
    } catch (e) {
      return ApiResponse.error('ネットワークエラー: $e');
    }
  }

  /// 🎵 音楽生成
  Future<ApiResponse<MusicGenerationData>> generateMusic({
    required String personaId,
    required int bpm,
    required String mood,
    int duration = 30,
  }) async {
    try {
      final response = await _client.post(
        Uri.parse('${ApiConfig.apiBaseUrl}/music/generate'),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: jsonEncode({
          'persona_id': personaId,
          'bpm': bpm,
          'mood': mood,
          'duration_seconds': duration,
        }),
      ).timeout(ApiConfig.timeout);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return ApiResponse.success(MusicGenerationData.fromJson(data));
      } else {
        return ApiResponse.error('音楽生成エラー: ${response.statusCode}');
      }
    } catch (e) {
      return ApiResponse.error('ネットワークエラー: $e');
    }
  }

  /// 📊 メトリクス送信
  Future<ApiResponse<bool>> sendMetrics({
    required String eventType,
    required Map<String, dynamic> data,
  }) async {
    try {
      final response = await _client.post(
        Uri.parse('${ApiConfig.apiBaseUrl}/metrics'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'event_type': eventType,
          'data': data,
          'timestamp': DateTime.now().toIso8601String(),
        }),
      ).timeout(ApiConfig.timeout);

      return ApiResponse.success(response.statusCode == 200);
    } catch (e) {
      // メトリクスは失敗してもアプリ動作に影響しない
      return ApiResponse.success(false);
    }
  }

  void dispose() {
    _client.close();
  }
}

/// 📨 API レスポンス
class ApiResponse<T> {
  final bool isSuccess;
  final T? data;
  final String? error;

  ApiResponse.success(this.data) 
      : isSuccess = true, error = null;

  ApiResponse.error(this.error) 
      : isSuccess = false, data = null;
}

/// 💬 チャット レスポンス
class ChatResponseData {
  final String response;
  final String personaId;
  final String conversationId;
  final double temperature;
  final List<String> emotions;
  final DateTime timestamp;

  ChatResponseData({
    required this.response,
    required this.personaId,
    required this.conversationId,
    required this.temperature,
    required this.emotions,
    required this.timestamp,
  });

  factory ChatResponseData.fromJson(Map<String, dynamic> json) {
    return ChatResponseData(
      response: json['response'] ?? '',
      personaId: json['persona_id'] ?? '',
      conversationId: json['conversation_id'] ?? '',
      temperature: (json['temperature'] ?? 0.0).toDouble(),
      emotions: List<String>.from(json['emotions'] ?? []),
      timestamp: DateTime.parse(json['timestamp']),
    );
  }
}

/// 🎭 ペルソナ API データ
class PersonaApiData {
  final String id;
  final String name;
  final String reading;
  final String tone;
  final int bpm;
  final List<String> specialties;
  final bool isActive;

  PersonaApiData({
    required this.id,
    required this.name,
    required this.reading,
    required this.tone,
    required this.bpm,
    required this.specialties,
    required this.isActive,
  });

  factory PersonaApiData.fromJson(Map<String, dynamic> json) {
    return PersonaApiData(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      reading: json['reading'] ?? '',
      tone: json['tone'] ?? '',
      bpm: json['bpm'] ?? 60,
      specialties: List<String>.from(json['specialties'] ?? []),
      isActive: json['is_active'] ?? false,
    );
  }
}

/// 🎵 音楽生成データ
class MusicGenerationData {
  final String trackId;
  final String audioUrl;
  final int bpm;
  final String key;
  final List<String> instruments;
  final int durationSeconds;

  MusicGenerationData({
    required this.trackId,
    required this.audioUrl,
    required this.bpm,
    required this.key,
    required this.instruments,
    required this.durationSeconds,
  });

  factory MusicGenerationData.fromJson(Map<String, dynamic> json) {
    return MusicGenerationData(
      trackId: json['track_id'] ?? '',
      audioUrl: json['audio_url'] ?? '',
      bpm: json['bpm'] ?? 60,
      key: json['key'] ?? 'C major',
      instruments: List<String>.from(json['instruments'] ?? []),
      durationSeconds: json['duration_seconds'] ?? 30,
    );
  }
}