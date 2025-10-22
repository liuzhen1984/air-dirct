/// API 配置类
class ApiConfig {
  // 后端服务地址（预留，待 server 实现）
  static const String baseUrl = 'http://localhost:3000/api';

  // 超时设置
  static const Duration timeout = Duration(seconds: 10);

  // API 端点
  static const String searchEndpoint = '/search';
  static const String translateEndpoint = '/translate';
  static const String definitionEndpoint = '/definition';
}
