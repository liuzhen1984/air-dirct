import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/word_definition.dart';
import '../models/search_response.dart';
import 'api_config.dart';

/// 词典服务类 - 负责与后端 API 交互
class DictionaryService {
  final http.Client _client;

  DictionaryService({http.Client? client}) : _client = client ?? http.Client();

  /// 搜索单词（支持多语言输入）
  /// [query] 用户输入的单词或短语
  /// 返回搜索响应（包含英文或中文结果）
  Future<SearchResponse> searchWord(String query) async {
    try {
      final url = Uri.parse('${ApiConfig.baseUrl}${ApiConfig.searchEndpoint}');

      final response = await _client
          .post(
            url,
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({'query': query}),
          )
          .timeout(ApiConfig.timeout);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return SearchResponse.fromJson(data);
      } else if (response.statusCode == 404) {
        final data = jsonDecode(response.body);
        final detail = data['detail'] as String? ?? 'Word not found';
        throw DictionaryException(detail);
      } else {
        throw DictionaryException(
          'Failed to search word: ${response.statusCode}',
        );
      }
    } catch (e) {
      if (e is DictionaryException) rethrow;
      throw DictionaryException('Network error: $e');
    }
  }

  /// 获取英文单词释义（仅英文查询）
  Future<WordDefinition> getDefinition(String word) async {
    try {
      final url = Uri.parse(
        '${ApiConfig.baseUrl}${ApiConfig.definitionEndpoint}/$word',
      );

      final response = await _client
          .get(url)
          .timeout(ApiConfig.timeout);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return WordDefinition.fromJson(data);
      } else if (response.statusCode == 404) {
        throw DictionaryException('Word not found: $word');
      } else {
        throw DictionaryException(
          'Failed to get definition: ${response.statusCode}',
        );
      }
    } catch (e) {
      if (e is DictionaryException) rethrow;
      throw DictionaryException('Network error: $e');
    }
  }

  /// 翻译文本（非英文 -> 英文）
  Future<String> translate(String text, String sourceLang) async {
    try {
      final url = Uri.parse('${ApiConfig.baseUrl}${ApiConfig.translateEndpoint}');

      final response = await _client
          .post(
            url,
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'text': text,
              'sourceLang': sourceLang,
              'targetLang': 'en',
            }),
          )
          .timeout(ApiConfig.timeout);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['translatedText'] as String;
      } else {
        throw DictionaryException(
          'Translation failed: ${response.statusCode}',
        );
      }
    } catch (e) {
      if (e is DictionaryException) rethrow;
      throw DictionaryException('Translation error: $e');
    }
  }

  void dispose() {
    _client.close();
  }
}

/// 词典服务异常
class DictionaryException implements Exception {
  final String message;

  DictionaryException(this.message);

  @override
  String toString() => 'DictionaryException: $message';
}
