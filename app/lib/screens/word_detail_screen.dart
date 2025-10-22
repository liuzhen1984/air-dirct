import 'package:flutter/material.dart';
import '../models/search_response.dart';
import '../services/dictionary_service.dart';

/// 单词详情页 - 展示释义
class WordDetailScreen extends StatefulWidget {
  final String query;

  const WordDetailScreen({
    Key? key,
    required this.query,
  }) : super(key: key);

  @override
  State<WordDetailScreen> createState() => _WordDetailScreenState();
}

class _WordDetailScreenState extends State<WordDetailScreen> {
  final DictionaryService _dictionaryService = DictionaryService();
  SearchResponse? _searchResponse;
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _loadDefinition();
  }

  Future<void> _loadDefinition() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      // 调用后端 API 查询单词
      final response = await _dictionaryService.searchWord(widget.query);
      setState(() {
        _searchResponse = response;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black87),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return const Center(
        child: CircularProgressIndicator(),
      );
    }

    if (_errorMessage != null) {
      return _buildError();
    }

    if (_searchResponse == null) {
      return const Center(
        child: Text('No results found'),
      );
    }

    // 根据是否为中文输入展示不同的结果
    if (_searchResponse!.isChinese) {
      return _buildChineseResult();
    } else {
      return _buildEnglishResult();
    }
  }

  Widget _buildError() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.error_outline,
              size: 64,
              color: Colors.red[300],
            ),
            const SizedBox(height: 16),
            const Text(
              'Failed to load definition',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              _errorMessage ?? 'Unknown error',
              style: TextStyle(
                fontSize: 14,
                color: Colors.grey[600],
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: _loadDefinition,
              icon: const Icon(Icons.refresh),
              label: const Text('Retry'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(
                  horizontal: 24,
                  vertical: 12,
                ),
              ),
            ),
            const SizedBox(height: 16),
            Text(
              'Tip: Make sure the server is running at ${_dictionaryService.runtimeType}',
              style: TextStyle(
                fontSize: 12,
                color: Colors.grey[500],
                fontStyle: FontStyle.italic,
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  /// 构建英文单词查询结果
  Widget _buildEnglishResult() {
    final result = _searchResponse!.englishResult!;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 单词标题
          Text(
            result.word,
            style: const TextStyle(
              fontSize: 36,
              fontWeight: FontWeight.bold,
            ),
          ),

          // 音标
          if (result.phonetic != null) ...[
            const SizedBox(height: 8),
            Text(
              result.phonetic!,
              style: TextStyle(
                fontSize: 18,
                color: Colors.grey[700],
                fontStyle: FontStyle.italic,
              ),
            ),
          ],

          const SizedBox(height: 32),

          // 释义列表
          ...result.meanings.asMap().entries.map((entry) {
            final index = entry.key;
            final meaning = entry.value;

            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (index > 0) const SizedBox(height: 20),
                _SimpleMeaningCard(meaning: meaning),
              ],
            );
          }).toList(),
        ],
      ),
    );
  }

  /// 构建中文翻译结果
  Widget _buildChineseResult() {
    final result = _searchResponse!.chineseResult!;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 原始中文查询
          Text(
            _searchResponse!.query,
            style: const TextStyle(
              fontSize: 36,
              fontWeight: FontWeight.bold,
            ),
          ),

          const SizedBox(height: 12),

          // 语言标识
          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: 12,
              vertical: 6,
            ),
            decoration: BoxDecoration(
              color: Colors.blue[50],
              borderRadius: BorderRadius.circular(12),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(
                  Icons.translate,
                  size: 16,
                  color: Colors.blue[700],
                ),
                const SizedBox(width: 6),
                Text(
                  'Chinese to English',
                  style: TextStyle(
                    fontSize: 13,
                    color: Colors.blue[700],
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 32),

          // 翻译结果标题
          Text(
            'English Translations',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w600,
              color: Colors.grey[800],
            ),
          ),

          const SizedBox(height: 16),

          // 翻译结果列表
          ...result.translations.asMap().entries.map((entry) {
            final index = entry.key;
            final translation = entry.value;

            return Container(
              margin: const EdgeInsets.only(bottom: 12),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(
                  color: Colors.blue[200]!,
                  width: 2,
                ),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.05),
                    blurRadius: 8,
                    offset: const Offset(0, 2),
                  ),
                ],
              ),
              child: Row(
                children: [
                  // 序号或图标
                  Container(
                    width: 32,
                    height: 32,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      color: Colors.blue[100],
                      shape: BoxShape.circle,
                    ),
                    child: result.translations.length > 1
                        ? Text(
                            '${index + 1}',
                            style: TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.bold,
                              color: Colors.blue[800],
                            ),
                          )
                        : Icon(
                            Icons.check,
                            size: 18,
                            color: Colors.blue[800],
                          ),
                  ),

                  const SizedBox(width: 16),

                  // 翻译内容
                  Expanded(
                    child: Text(
                      translation,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w500,
                        height: 1.4,
                      ),
                    ),
                  ),
                ],
              ),
            );
          }).toList(),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _dictionaryService.dispose();
    super.dispose();
  }
}

/// 简化的词义卡片
class _SimpleMeaningCard extends StatelessWidget {
  final SimpleMeaning meaning;

  const _SimpleMeaningCard({required this.meaning});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: Colors.grey[300]!,
          width: 1.5,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 词性标签
          Container(
            padding: const EdgeInsets.symmetric(
              horizontal: 10,
              vertical: 4,
            ),
            decoration: BoxDecoration(
              color: Colors.green[100],
              borderRadius: BorderRadius.circular(6),
            ),
            child: Text(
              meaning.pos,
              style: TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w600,
                color: Colors.green[800],
              ),
            ),
          ),

          const SizedBox(height: 12),

          // 中文释义
          Text(
            meaning.meaning,
            style: const TextStyle(
              fontSize: 16,
              height: 1.6,
              color: Colors.black87,
            ),
          ),
        ],
      ),
    );
  }
}
