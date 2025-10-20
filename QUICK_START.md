# 🚀 Air Dict - 快速开始指南

## 一键启动

### 步骤 1: 启动后端服务

```bash
cd server
./run.sh
```

**看到这个输出说明成功**:
```
🚀 Starting Air Dict Python Server with uv...
📚 Syncing dependencies with uv...
🎉 Starting server...
INFO:     Uvicorn running on http://0.0.0.0:3000
INFO:     Application startup complete.
```

测试后端是否正常：
```bash
curl http://localhost:3000/health
# 应返回: {"status":"healthy"}

curl -X POST http://localhost:3000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"hello"}'
# 应返回单词释义（当 API 可用时）
```

---

### 步骤 2: 安装 Flutter（如果还没有）

**macOS** (推荐使用 Homebrew):
```bash
brew install --cask flutter
flutter doctor
```

验证安装：
```bash
flutter --version
# 应显示 Flutter 3.x.x
```

---

### 步骤 3: 运行 Flutter 应用

```bash
# 终端 2: 运行应用
cd /Users/zliu/IdeaProjects/air-dirct/app

# 安装依赖（首次运行）
flutter pub get

# 运行应用
flutter run -d chrome      # 在浏览器运行（最快）
# 或
flutter run -d ios         # 在 iOS 模拟器运行
# 或
flutter run -d android     # 在 Android 模拟器运行
# 或
flutter run -d macos       # 在 macOS 桌面运行
```

**首次运行可能需要 2-3 分钟编译，后续启动会很快！**

---

## 📱 选择运行设备

### 查看可用设备
```bash
flutter devices
```

可能的输出：
```
Chrome (web)       • chrome       • web-javascript • Google Chrome 120.0
macOS (desktop)    • macos        • darwin-arm64   • macOS 14.0
iPhone 15 (mobile) • simulator    • ios            • iOS 17.0
```

### Web 浏览器（推荐用于开发）

```bash
flutter run -d chrome
```

**优点**:
- ✅ 启动最快（~10 秒）
- ✅ 热重载迅速
- ✅ DevTools 方便调试
- ✅ 无需模拟器

**启动后**:
- 浏览器自动打开 `http://localhost:xxxxx`
- 按 `r` 热重载
- 按 `R` 热重启
- 按 `q` 退出

---

### iOS 模拟器

**启动模拟器**:
```bash
# 打开 Simulator.app
open -a Simulator

# 或从命令行启动特定模拟器
xcrun simctl list devices
xcrun simctl boot "iPhone 15"
```

**运行应用**:
```bash
flutter run -d ios
```

**注意**:
- iOS 模拟器使用 `localhost` 连接后端
- 无需修改 API 地址

---

### Android 模拟器

**启动模拟器**:
```bash
# 在 Android Studio 中启动 AVD
# 或使用命令行
emulator -avd Pixel_7_API_34
```

**修改 API 地址**:
Android 模拟器需要使用 `10.0.2.2` 代替 `localhost`

编辑 `app/lib/services/api_config.dart`:
```dart
static const String baseUrl = 'http://10.0.2.2:3000/api';
```

**运行应用**:
```bash
flutter run -d android
```

---

### macOS 桌面应用

```bash
flutter run -d macos
```

**优点**:
- ✅ 原生桌面体验
- ✅ 快捷键支持
- ✅ 独立窗口

---

## 🎨 开发体验

### 热重载（Hot Reload）

应用运行后，修改代码并保存，然后：
- 按 `r` - 热重载（保持状态）
- 按 `R` - 热重启（重置状态）

**示例**:
1. 修改 `home_screen.dart` 中的标题文字
2. 保存文件
3. 按 `r`
4. 立即看到变化（< 1 秒）

---

### 调试技巧

**1. 打印日志**:
```dart
print('Debug: $_searchController.text');
debugPrint('Warning: API call failed');
```

**2. 使用 DevTools**:
```bash
# 应用运行时，访问提示的 URL
# 例如: http://127.0.0.1:9100
```

**3. 查看网络请求**:
```dart
// 在 dictionary_service.dart 中已有日志
print('Calling API: ${ApiConfig.baseUrl}');
```

---

## 🔧 常见问题

### Q1: "No devices available"

**A**: 启动设备
```bash
# Chrome
flutter run -d chrome

# iOS 模拟器
open -a Simulator

# 检查设备
flutter devices
```

---

### Q2: "Failed to connect to localhost:3000"

**A**: 确保后端正在运行
```bash
# 检查后端进程
lsof -i :3000

# 启动后端
cd server && ./run.sh
```

---

### Q3: iOS 模拟器报错 "Could not find iPhone simulator"

**A**: 安装 Xcode 并接受许可证
```bash
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch
sudo xcodebuild -license accept
```

---

### Q4: Android 无法连接后端

**A**: 使用 `10.0.2.2` 代替 `localhost`
```dart
// app/lib/services/api_config.dart
static const String baseUrl = 'http://10.0.2.2:3000/api';
```

---

### Q5: "Waiting for another flutter command"

**A**: 删除锁文件
```bash
rm ~/.flutter/bin/cache/lockfile
```

---

## 📦 构建生产版本

### iOS App

```bash
cd app
flutter build ios --release

# 输出位置: build/ios/iphoneos/Runner.app
# 需要 Xcode 签名和上传到 App Store
```

**App Store 发布**:
1. 在 Xcode 中打开 `ios/Runner.xcworkspace`
2. 选择 Product → Archive
3. 上传到 App Store Connect

---

### Android APK

```bash
flutter build apk --release

# 输出位置: build/app/outputs/flutter-apk/app-release.apk
```

**优化**: 按架构分包（减小体积）
```bash
flutter build apk --split-per-abi --release

# 生成 3 个 APK:
# - app-armeabi-v7a-release.apk (~10MB)
# - app-arm64-v8a-release.apk (~12MB)
# - app-x86_64-release.apk (~14MB)
```

---

### Web 部署

```bash
flutter build web --release

# 输出目录: build/web/
```

**部署到 Vercel**:
```bash
npm install -g vercel
cd build/web
vercel deploy
```

**部署到 Netlify**:
```bash
# 拖拽 build/web 文件夹到 netlify.com
# 或使用 Netlify CLI
netlify deploy --dir=build/web
```

---

## 🎯 性能测试

### 启动时间测试

```bash
flutter run --profile --trace-startup
```

查看输出中的 `timeToFirstFrame` 值

**优化后预期值**:
- Debug: ~800ms
- Profile: ~400ms
- Release: ~300ms

---

### 应用体积检查

```bash
# iOS
ls -lh build/ios/iphoneos/Runner.app

# Android
ls -lh build/app/outputs/flutter-apk/app-release.apk

# Web
du -sh build/web
```

**优化后预期值**:
- iOS: ~12MB
- Android: ~15MB (universal) / ~10MB (arm64)
- Web: ~2MB (gzipped)

---

## 📚 下一步

### 1. 熟悉代码结构
```
app/lib/
├── main.dart              # 入口
├── models/                # 数据模型
├── services/              # API + 历史记录
└── screens/               # 页面 UI
```

### 2. 修改 API 地址（生产环境）
```dart
// app/lib/services/api_config.dart
static const String baseUrl = 'https://your-api.com/api';
```

### 3. 添加新功能
- 阅读 `DESIGN.md` 了解设计思路
- 参考 `OPTIMIZATION.md` 学习优化技巧

### 4. 发布应用
- iOS: App Store
- Android: Google Play
- Web: Vercel/Netlify

---

## 🆘 获取帮助

**问题排查顺序**:
1. 查看终端错误信息
2. 运行 `flutter doctor` 检查环境
3. 查看 `DESIGN.md` 和 `README.md`
4. Google 搜索错误信息
5. 提交 Issue

**有用的命令**:
```bash
flutter doctor -v          # 详细诊断
flutter clean              # 清理缓存
flutter pub get            # 更新依赖
flutter upgrade            # 升级 Flutter
```

---

## ✅ 检查清单

开始开发前确保：
- [ ] Flutter 已安装（`flutter --version`）
- [ ] 后端正在运行（访问 `http://localhost:3000/health`）
- [ ] 设备已连接（`flutter devices`）
- [ ] 依赖已安装（`flutter pub get`）

然后运行：
```bash
flutter run -d chrome
```

享受开发吧！ 🎉
