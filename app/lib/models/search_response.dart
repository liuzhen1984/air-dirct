/// 简化的词义模型
class SimpleMeaning {
  final String pos; // 词性 (part of speech)
  final String meaning; // 中文释义

  SimpleMeaning({
    required this.pos,
    required this.meaning,
  });

  factory SimpleMeaning.fromJson(Map<String, dynamic> json) {
    return SimpleMeaning(
      pos: json['pos'] as String,
      meaning: json['meaning'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'pos': pos,
      'meaning': meaning,
    };
  }
}

/// 英文单词查询结果
class EnglishResult {
  final String word;
  final String? phonetic;
  final List<SimpleMeaning> meanings;

  EnglishResult({
    required this.word,
    this.phonetic,
    required this.meanings,
  });

  factory EnglishResult.fromJson(Map<String, dynamic> json) {
    return EnglishResult(
      word: json['word'] as String,
      phonetic: json['phonetic'] as String?,
      meanings: (json['meanings'] as List)
          .map((m) => SimpleMeaning.fromJson(m as Map<String, dynamic>))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'word': word,
      'phonetic': phonetic,
      'meanings': meanings.map((m) => m.toJson()).toList(),
    };
  }
}

/// 中文翻译结果
class ChineseResult {
  final List<String> translations; // 翻译结果列表

  ChineseResult({
    required this.translations,
  });

  factory ChineseResult.fromJson(Map<String, dynamic> json) {
    return ChineseResult(
      translations: (json['translations'] as List)
          .map((t) => t as String)
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'translations': translations,
    };
  }
}

/// 搜索响应模型 - 匹配后端 /api/search 接口
class SearchResponse {
  final String query; // 原始查询
  final bool isChinese; // 是否为中文输入
  final EnglishResult? englishResult; // 英文查询结果
  final ChineseResult? chineseResult; // 中文查询结果

  SearchResponse({
    required this.query,
    required this.isChinese,
    this.englishResult,
    this.chineseResult,
  });

  /// 从 JSON 解析
  factory SearchResponse.fromJson(Map<String, dynamic> json) {
    return SearchResponse(
      query: json['query'] as String,
      isChinese: json['is_chinese'] as bool,
      englishResult: json['english_result'] != null
          ? EnglishResult.fromJson(json['english_result'] as Map<String, dynamic>)
          : null,
      chineseResult: json['chinese_result'] != null
          ? ChineseResult.fromJson(json['chinese_result'] as Map<String, dynamic>)
          : null,
    );
  }

  /// 转换为 JSON
  Map<String, dynamic> toJson() {
    return {
      'query': query,
      'is_chinese': isChinese,
      'english_result': englishResult?.toJson(),
      'chinese_result': chineseResult?.toJson(),
    };
  }
}
