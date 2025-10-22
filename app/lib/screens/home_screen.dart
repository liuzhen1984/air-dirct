import 'package:flutter/material.dart';
import '../models/history_item.dart';
import '../services/history_service.dart';
import 'word_detail_screen.dart';

/// 首页 - Google 风格极简设计
class HomeScreen extends StatefulWidget {
  final HistoryService historyService;

  const HomeScreen({
    Key? key,
    required this.historyService,
  }) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _searchController = TextEditingController();
  List<HistoryItem> _history = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    final history = await widget.historyService.getHistory(limit: 5);
    setState(() {
      _history = history;
    });
  }

  Future<void> _handleSearch(String query) async {
    if (query.trim().isEmpty) return;

    setState(() {
      _isLoading = true;
    });

    try {
      // 添加到历史记录
      await widget.historyService.addToHistory(query.trim());

      // 导航到详情页
      if (mounted) {
        await Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => WordDetailScreen(
              query: query.trim(),
            ),
          ),
        );

        // 返回后刷新历史记录
        await _loadHistory();
      }
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(horizontal: 24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Logo / Title
                const Text(
                  'Air Dict',
                  style: TextStyle(
                    fontSize: 48,
                    fontWeight: FontWeight.w300,
                    letterSpacing: -1,
                  ),
                ),
                const SizedBox(height: 48),

                // 搜索框
                Container(
                  constraints: const BoxConstraints(maxWidth: 600),
                  child: TextField(
                    controller: _searchController,
                    decoration: InputDecoration(
                      hintText: 'Enter a word in any language...',
                      prefixIcon: const Icon(Icons.search),
                      suffixIcon: _searchController.text.isNotEmpty
                          ? IconButton(
                              icon: const Icon(Icons.clear),
                              onPressed: () {
                                setState(() {
                                  _searchController.clear();
                                });
                              },
                            )
                          : null,
                      filled: true,
                      fillColor: Colors.white,
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(28),
                        borderSide: BorderSide(
                          color: Colors.grey[300]!,
                          width: 1.5,
                        ),
                      ),
                      enabledBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(28),
                        borderSide: BorderSide(
                          color: Colors.grey[300]!,
                          width: 1.5,
                        ),
                      ),
                      focusedBorder: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(28),
                        borderSide: const BorderSide(
                          color: Colors.blue,
                          width: 2,
                        ),
                      ),
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 24,
                        vertical: 16,
                      ),
                    ),
                    style: const TextStyle(fontSize: 16),
                    textInputAction: TextInputAction.search,
                    onChanged: (value) => setState(() {}),
                    onSubmitted: _handleSearch,
                  ),
                ),

                const SizedBox(height: 32),

                // 历史记录
                if (_history.isNotEmpty) ...[
                  const Text(
                    'Recent Searches',
                    style: TextStyle(
                      fontSize: 14,
                      color: Colors.grey,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Wrap(
                    spacing: 8,
                    runSpacing: 8,
                    alignment: WrapAlignment.center,
                    children: _history.map((item) {
                      return _HistoryChip(
                        item: item,
                        onTap: () {
                          _searchController.text = item.word;
                          _handleSearch(item.word);
                        },
                        onDelete: () async {
                          await widget.historyService.removeHistoryItem(item.word);
                          await _loadHistory();
                        },
                      );
                    }).toList(),
                  ),
                ],

                // Loading indicator
                if (_isLoading) ...[
                  const SizedBox(height: 32),
                  const CircularProgressIndicator(),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }
}

/// 历史记录卡片
class _HistoryChip extends StatelessWidget {
  final HistoryItem item;
  final VoidCallback onTap;
  final VoidCallback onDelete;

  const _HistoryChip({
    required this.item,
    required this.onTap,
    required this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,
      borderRadius: BorderRadius.circular(20),
      elevation: 2,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(20),
        child: Container(
          padding: const EdgeInsets.symmetric(
            horizontal: 16,
            vertical: 10,
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                item.word,
                style: const TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w500,
                ),
              ),
              if (item.variants.isNotEmpty) ...[
                const SizedBox(width: 6),
                Text(
                  '+${item.variants.length}',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[600],
                  ),
                ),
              ],
              const SizedBox(width: 8),
              GestureDetector(
                onTap: onDelete,
                child: Icon(
                  Icons.close,
                  size: 16,
                  color: Colors.grey[600],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
