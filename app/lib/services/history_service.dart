import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/history_item.dart';

/// 历史记录服务 - 管理本地搜索历史
class HistoryService {
  static const String _historyKey = 'search_history';
  static const int _maxHistorySize = 50; // 最多保存 50 条

  final SharedPreferences _prefs;

  HistoryService(this._prefs);

  /// 获取历史记录
  /// [limit] 返回数量限制（默认 5 条用于首页展示）
  Future<List<HistoryItem>> getHistory({int limit = 5}) async {
    final historyJson = _prefs.getString(_historyKey);
    if (historyJson == null) return [];

    final List<dynamic> decoded = jsonDecode(historyJson);
    final history = decoded
        .map((json) => HistoryItem.fromJson(json))
        .toList();

    // 按时间戳降序排列
    history.sort((a, b) => b.timestamp.compareTo(a.timestamp));

    return history.take(limit).toList();
  }

  /// 添加到历史记录（带智能去重）
  Future<void> addToHistory(String word) async {
    final history = await _getAllHistory();

    // 简化版去重：基于词根（lemma）
    // TODO: 后续可集成编辑距离算法
    final lemma = _simpleLemmatize(word);

    // 查找是否存在相似记录
    final existingIndex = history.indexWhere(
      (item) => item.lemma == lemma || item.word.toLowerCase() == word.toLowerCase(),
    );

    if (existingIndex != -1) {
      // 更新现有记录
      final existing = history[existingIndex];
      final variants = Set<String>.from(existing.variants)..add(word);
      variants.remove(existing.word); // 移除当前主词

      history[existingIndex] = existing.copyWith(
        timestamp: DateTime.now().millisecondsSinceEpoch,
        frequency: existing.frequency + 1,
        variants: variants.toList(),
      );
    } else {
      // 添加新记录
      history.insert(
        0,
        HistoryItem(
          word: word,
          lemma: lemma,
          timestamp: DateTime.now().millisecondsSinceEpoch,
          variants: [],
          frequency: 1,
        ),
      );
    }

    // 限制大小
    if (history.length > _maxHistorySize) {
      history.removeRange(_maxHistorySize, history.length);
    }

    await _saveHistory(history);
  }

  /// 清空历史记录
  Future<void> clearHistory() async {
    await _prefs.remove(_historyKey);
  }

  /// 删除单个历史记录
  Future<void> removeHistoryItem(String word) async {
    final history = await _getAllHistory();
    history.removeWhere((item) => item.word == word);
    await _saveHistory(history);
  }

  // ========== 私有方法 ==========

  Future<List<HistoryItem>> _getAllHistory() async {
    final historyJson = _prefs.getString(_historyKey);
    if (historyJson == null) return [];

    final List<dynamic> decoded = jsonDecode(historyJson);
    return decoded.map((json) => HistoryItem.fromJson(json)).toList();
  }

  Future<void> _saveHistory(List<HistoryItem> history) async {
    final encoded = jsonEncode(history.map((item) => item.toJson()).toList());
    await _prefs.setString(_historyKey, encoded);
  }

  /// 简单词形还原（基础版本）
  /// TODO: 集成 NLP 库实现更准确的还原
  String _simpleLemmatize(String word) {
    final lower = word.toLowerCase();

    // 移除常见后缀
    if (lower.endsWith('ing') && lower.length > 5) {
      return lower.substring(0, lower.length - 3);
    }
    if (lower.endsWith('ed') && lower.length > 4) {
      return lower.substring(0, lower.length - 2);
    }
    if (lower.endsWith('s') && lower.length > 2) {
      return lower.substring(0, lower.length - 1);
    }

    return lower;
  }
}
