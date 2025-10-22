/// 历史记录项 - 轻量级版本（手动 JSON 解析）
class HistoryItem {
  final String word;
  final String lemma;
  final int timestamp;
  final List<String> variants;
  final int frequency;

  HistoryItem({
    required this.word,
    required this.lemma,
    required this.timestamp,
    this.variants = const [],
    this.frequency = 1,
  });

  /// 从 JSON 解析
  factory HistoryItem.fromJson(Map<String, dynamic> json) {
    return HistoryItem(
      word: json['word'] as String,
      lemma: json['lemma'] as String,
      timestamp: json['timestamp'] as int,
      variants: (json['variants'] as List<dynamic>?)
              ?.map((v) => v as String)
              .toList() ??
          [],
      frequency: json['frequency'] as int? ?? 1,
    );
  }

  /// 转换为 JSON
  Map<String, dynamic> toJson() {
    return {
      'word': word,
      'lemma': lemma,
      'timestamp': timestamp,
      'variants': variants,
      'frequency': frequency,
    };
  }

  /// 创建更新后的副本
  HistoryItem copyWith({
    String? word,
    String? lemma,
    int? timestamp,
    List<String>? variants,
    int? frequency,
  }) {
    return HistoryItem(
      word: word ?? this.word,
      lemma: lemma ?? this.lemma,
      timestamp: timestamp ?? this.timestamp,
      variants: variants ?? this.variants,
      frequency: frequency ?? this.frequency,
    );
  }
}
