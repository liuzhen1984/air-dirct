# Flutter 安装和运行指南

## Flutter 未安装

当前系统未检测到 Flutter。以下是安装和运行应用的步骤。

---

## 方案 1: 安装 Flutter（推荐）

### macOS 安装步骤

#### 1. 下载 Flutter SDK

```bash
# 使用 Homebrew（推荐）
brew install --cask flutter

# 或手动下载
cd ~
git clone https://github.com/flutter/flutter.git -b stable
```

#### 2. 配置环境变量

如果手动安装，添加到 `~/.zshrc` 或 `~/.bash_profile`:

```bash
export PATH="$HOME/flutter/bin:$PATH"
```

然后重新加载：
```bash
source ~/.zshrc
```

#### 3. 验证安装

```bash
flutter --version
flutter doctor
```

#### 4. 安装依赖

根据 `flutter doctor` 输出安装缺失的依赖：

```bash
# iOS 开发（需要 Xcode）
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch

# Android 开发（需要 Android Studio）
# 下载 Android Studio: https://developer.android.com/studio
# 安装 Flutter 和 Dart 插件
```

---

## 方案 2: 使用 Docker（快速测试）

如果只想快速运行 Web 版本：

```bash
# 构建镜像
docker run --rm -v $(pwd)/app:/app -w /app cirrusci/flutter:stable \
  flutter pub get

# 运行 Web 版
docker run --rm -p 8080:8080 \
  -v $(pwd)/app:/app -w /app \
  cirrusci/flutter:stable \
  flutter run -d web-server --web-port=8080
```

访问 `http://localhost:8080`

---

## 方案 3: 使用 Android Studio / VS Code

### Android Studio

1. 下载并安装 [Android Studio](https://developer.android.com/studio)
2. 安装 Flutter 插件：
   - 打开 Android Studio
   - 进入 Preferences → Plugins
   - 搜索并安装 "Flutter"
3. 使用 Android Studio 打开 `app` 目录
4. 点击 Run 按钮

### VS Code

1. 安装 [VS Code](https://code.visualstudio.com/)
2. 安装 Flutter 扩展：
   - 打开 VS Code
   - 进入 Extensions (⌘+Shift+X)
   - 搜索并安装 "Flutter"
3. 打开 `app` 目录
4. 按 F5 运行

---

## 运行应用

### 安装完 Flutter 后

```bash
cd /Users/zliu/IdeaProjects/air-dirct/app

# 1. 安装依赖
flutter pub get

# 2. 查看可用设备
flutter devices

# 3. 运行应用
flutter run                 # 自动选择设备
flutter run -d chrome       # 运行在 Chrome 浏览器
flutter run -d macos        # 运行在 macOS 桌面
```

### 热重载

应用运行后：
- 按 `r` - 热重载
- 按 `R` - 热重启
- 按 `q` - 退出
- 按 `h` - 帮助

---

## 常见问题

### Q: flutter doctor 报错 "Xcode not found"

**A**: 安装 Xcode
```bash
# 从 App Store 安装 Xcode
xcode-select --install
```

### Q: "No devices available"

**A**: 启动模拟器或连接设备
```bash
# iOS 模拟器
open -a Simulator

# 列出可用的 iOS 模拟器
xcrun simctl list devices

# 启动特定模拟器
xcrun simctl boot "iPhone 15"
```

### Q: "CocoaPods not installed"

**A**: 安装 CocoaPods
```bash
sudo gem install cocoapods
```

### Q: Android 许可证未接受

**A**: 接受许可证
```bash
flutter doctor --android-licenses
```

---

## 预览效果（无需 Flutter）

如果暂时无法安装 Flutter，你可以：

1. **查看代码结构**: 所有代码已经完整实现
2. **先运行后端**:
   ```bash
   cd /Users/zliu/IdeaProjects/air-dirct/server
   npm install
   npm run dev
   ```
3. **使用 curl 测试 API**:
   ```bash
   curl -X POST http://localhost:3000/api/search \
     -H "Content-Type: application/json" \
     -d '{"query":"hello"}'
   ```

---

## 构建 Web 版本（生产环境）

```bash
cd app
flutter build web --release

# 输出目录: app/build/web
# 可部署到任何静态托管服务（Vercel, Netlify, GitHub Pages）
```

使用 Python 快速预览：
```bash
cd app/build/web
python3 -m http.server 8000
# 访问 http://localhost:8000
```

---

## Flutter 学习资源

- 官方文档: https://docs.flutter.dev/
- 中文文档: https://flutter.cn/
- Flutter Codelabs: https://codelabs.developers.google.com/?product=flutter
- Flutter 示例: https://flutter.github.io/samples/

---

## 下一步

安装完 Flutter 后，运行：

```bash
cd /Users/zliu/IdeaProjects/air-dirct/app
flutter pub get
flutter run -d chrome
```

应用将在浏览器中启动，你会看到极简的搜索界面！
