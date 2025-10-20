# Air Dict App

Flutter 跨平台前端应用。

## 快速启动

```bash
# 安装依赖
flutter pub get

# 运行应用
flutter run

# 指定设备
flutter run -d ios        # iOS 模拟器
flutter run -d android    # Android 模拟器
flutter run -d chrome     # Web 浏览器
```

## 构建发布版本

```bash
# Android APK
flutter build apk --release

# iOS（需要 Mac + Xcode）
flutter build ios --release

# Web
flutter build web --release
```

## 配置后端地址

修改 `lib/services/api_config.dart`:

```dart
static const String baseUrl = 'http://YOUR_SERVER:3000/api';
```

常用地址：
- iOS 模拟器: `http://localhost:3000/api`
- Android 模拟器: `http://10.0.2.2:3000/api`
- 真机: `http://YOUR_IP:3000/api`

## 项目结构

```
lib/
├── models/           # 数据模型
│   ├── word_definition.dart
│   └── history_item.dart
├── services/         # 服务层
│   ├── api_config.dart
│   ├── dictionary_service.dart
│   └── history_service.dart
├── screens/          # 页面
│   ├── home_screen.dart
│   └── word_detail_screen.dart
└── main.dart         # 入口
```

## 依赖说明

- `http`: HTTP 客户端
- `provider`: 状态管理（预留）
- `shared_preferences`: 本地存储
- `json_annotation`: JSON 序列化

## 生成代码

如需重新生成 JSON 序列化代码：

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```
