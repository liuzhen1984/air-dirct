import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'screens/home_screen.dart';
import 'services/history_service.dart';

void main() {
  // 优化启动：立即运行 UI，后台加载服务
  runApp(const AirDictApp());
}

class AirDictApp extends StatelessWidget {
  const AirDictApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Air Dict',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
        // 优化字体渲染
        fontFamily: 'Roboto',
      ),
      home: const _HomeWrapper(),
    );
  }
}

/// 延迟加载 SharedPreferences 的包装器
class _HomeWrapper extends StatefulWidget {
  const _HomeWrapper({Key? key}) : super(key: key);

  @override
  State<_HomeWrapper> createState() => _HomeWrapperState();
}

class _HomeWrapperState extends State<_HomeWrapper> {
  HistoryService? _historyService;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _initializeServices();
  }

  /// 异步初始化服务（不阻塞 UI 渲染）
  Future<void> _initializeServices() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      setState(() {
        _historyService = HistoryService(prefs);
        _isLoading = false;
      });
    } catch (e) {
      debugPrint('Failed to initialize services: $e');
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      // 显示极简加载界面
      return const Scaffold(
        backgroundColor: Color(0xFFF5F5F5),
        body: Center(
          child: CircularProgressIndicator(strokeWidth: 2),
        ),
      );
    }

    if (_historyService == null) {
      // 初始化失败，使用临时服务
      return Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, size: 48, color: Colors.red),
              const SizedBox(height: 16),
              const Text('Failed to initialize app'),
              const SizedBox(height: 8),
              ElevatedButton(
                onPressed: () {
                  setState(() {
                    _isLoading = true;
                  });
                  _initializeServices();
                },
                child: const Text('Retry'),
              ),
            ],
          ),
        ),
      );
    }

    return HomeScreen(historyService: _historyService!);
  }
}
