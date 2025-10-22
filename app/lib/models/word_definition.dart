/// 单词释义模型 - 轻量级版本（手动 JSON 解析）
class WordDefinition {
  final String word;
  final String? phonetic;
  final String? chinese; // 中文翻译
  final List<Meaning> meanings;
  final String? translatedFrom;

  WordDefinition({
    required this.word,
    this.phonetic,
    this.chinese,
    required this.meanings,
    this.translatedFrom,
  });

  /// 从 JSON 解析
  factory WordDefinition.fromJson(Map<String, dynamic> json) {
    return WordDefinition(
      word: json['word'] as String,
      phonetic: json['phonetic'] as String?,
      chinese: json['chinese'] as String?,
      meanings: (json['meanings'] as List<dynamic>)
          .map((m) => Meaning.fromJson(m as Map<String, dynamic>))
          .toList(),
      translatedFrom: json['translatedFrom'] as String?,
    );
  }

  /// 转换为 JSON
  Map<String, dynamic> toJson() {
    return {
      'word': word,
      'phonetic': phonetic,
      'chinese': chinese,
      'meanings': meanings.map((m) => m.toJson()).toList(),
      'translatedFrom': translatedFrom,
    };
  }
}

/// 词义分组（按词性）
class Meaning {
  final String partOfSpeech;
  final List<Definition> definitions;

  Meaning({
    required this.partOfSpeech,
    required this.definitions,
  });

  factory Meaning.fromJson(Map<String, dynamic> json) {
    return Meaning(
      partOfSpeech: json['part_of_speech'] as String? ?? json['partOfSpeech'] as String,
      definitions: (json['definitions'] as List<dynamic>)
          .map((d) => Definition.fromJson(d as Map<String, dynamic>))
          .toList(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'partOfSpeech': partOfSpeech,
      'definitions': definitions.map((d) => d.toJson()).toList(),
    };
  }
}

/// 具体定义
class Definition {
  final String definition;
  final String? definitionChinese; // 释义的中文翻译
  final String? example;
  final String? exampleChinese; // 例句的中文翻译

  Definition({
    required this.definition,
    this.definitionChinese,
    this.example,
    this.exampleChinese,
  });

  factory Definition.fromJson(Map<String, dynamic> json) {
    return Definition(
      definition: json['definition'] as String,
      definitionChinese: json['definition_chinese'] as String?,
      example: json['example'] as String?,
      exampleChinese: json['example_chinese'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'definition': definition,
      'definition_chinese': definitionChinese,
      'example': example,
      'example_chinese': exampleChinese,
    };
  }
}
