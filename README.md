# 360° 全景照片浏览器

一个完全免费、**离线可用**的 360° 全景照片浏览器，支持安卓 / iPhone「安装为 App」。
适合浏览大疆无人机等设备拍摄的等距柱状投影（Equirectangular）全景照片——
图片完全在本地浏览器处理，**不会上传到任何服务器**。

---

## 📂 文件结构

```
panorama-viewer/
├── index.html          主页面（全景浏览 + UI）
├── manifest.json       PWA 应用清单
├── sw.js               Service Worker（离线缓存核心）
├── serve.py            本地测试服务器（可选）
├── make_icons.py       重新生成图标脚本（可选）
├── lib/
│   ├── pannellum.js    全景渲染库（本地，无需联网）
│   └── pannellum.css
└── icons/              各尺寸图标
```

---

## 🧪 本地测试（部署前先验证）

> ⚠️ PWA 的「离线缓存」「安装为 App」功能**只在 http(s) 下生效**，
> 直接双击 `index.html`（`file://` 协议）这些功能会失效，但浏览功能仍可用。

### 方法一：用自带脚本（最简单）

在项目目录打开命令行（在该目录的地址栏输入 `cmd` 回车），执行：

```bash
py serve.py
```

它会打印两个地址：
- **本机访问**：`http://localhost:8000/`
- **手机访问**：`http://你的电脑IP:8000/`（手机需连同一 WiFi）

按 `Ctrl+C` 停止。

### 方法二：用 Python 内置命令

```bash
py -m http.server 8000
```

### 方法三：用 VS Code

安装「Live Server」扩展，右键 `index.html` → Open with Live Server。

---

## 🚀 部署到 GitHub Pages（免费，永久在线）

部署后你将获得一个 `https://你的用户名.github.io/panorama-viewer/` 的网址，
手机打开一次即可「安装为 App」，之后离线可用。

### 步骤

1. **注册 GitHub 账号**（如果没有）：https://github.com

2. **新建仓库**
   - 右上角 `+` → New repository
   - 名字随意，比如 `panorama-viewer`
   - 选 **Public**（私有仓库的 Pages 需要付费版）
   - 勾选「Add a README file」
   - 点 Create repository

3. **上传项目文件**
   - 进入仓库，点 `Add file` → `Upload files`
   - 把项目里**所有文件和文件夹**拖进去（包括 `index.html`、`manifest.json`、
     `sw.js`、`lib/`、`icons/`）
   - ⚠️ 注意：`lib/` 和 `icons/` 是文件夹，GitHub 网页上传时需要逐个文件传，
     或者用下面的 Git 命令行方式更省事：

   **命令行方式（推荐）：**
   ```bash
   cd D:\mjlwork\prj\panorama-viewer
   git init
   git add .
   git commit -m "全景浏览器 PWA"
   git branch -M main
   git remote add origin https://github.com/你的用户名/panorama-viewer.git
   git push -u origin main
   ```

4. **开启 GitHub Pages**
   - 仓库页面 → `Settings`（设置）→ 左侧 `Pages`
   - `Source` 选 **Deploy from a branch**
   - `Branch` 选 `main`，文件夹选 `/ (root)`
   - 点 Save

5. **等待 1-2 分钟**，访问：
   ```
   https://你的用户名.github.io/panorama-viewer/
   ```

### 其它免费托管平台（同样可用）

- **Vercel**：https://vercel.com —— 连 GitHub 后一键部署，速度更快
- **Netlify**：https://netlify.com —— 拖拽文件夹即可部署
- **Cloudflare Pages**：https://pages.cloudflare.com

---

## 📲 安装为手机 App

### 安卓（Chrome / Edge / 夸克 等）

1. 用浏览器打开部署后的网址
2. 等页面加载完，会看到顶部按钮 **「📲 安装到桌面」**，直接点
   - 或点浏览器菜单（⋮）→ **「添加到主屏幕」/「安装应用」**
3. 桌面出现「全景浏览」图标，点开就是全屏 App 体验，**断网也能用**

### iPhone / iPad（Safari）

iOS 不支持自动安装提示，需手动操作：

1. 用 **Safari** 打开网址（Chrome/微信内置浏览器不行）
2. 点底部 **「分享」按钮**（方框向上的箭头 ↑）
3. 选 **「添加到主屏幕」** → 「添加」
4. 桌面出现图标，点开即用

> iPhone 首次使用必须联网（下载缓存），之后可离线。

---

## 🎯 使用说明

| 操作 | 效果 |
|---|---|
| 拖动图片 | 360° 转动视角 |
| 双指捏合 / 滚轮 | 缩放（调整 FOV） |
| 顶部「打开图片」 | 选择本地全景图 |
| 直接拖图片到页面 | 上传图片 |
| 「示例」按钮 | 加载一张在线全景图体验 |
| 底部面板 ⟳ | 自动旋转 |
| 底部面板 🎯 | 复位视角 |
| 底部面板 📸 | **一键超清截屏**（导出当前视角照片，JPEG 格式，快捷键 S） |
| 底部面板 ⛶ | 全屏 |
| 底部面板 🔁 | 换一张图 |
| 键盘 ←→↑↓ + `+/-` | 桌面端调整视角（R 复位，S / C 一键截屏） |

### 关于全景图格式

- ✅ **标准全景**：宽高比约 2:1（如 8000×4000），上下有极点拉伸 → 完美显示
- ⚠️ **部分全景**：宽但不足 2:1 → 仍可显示，可能略有变形
- ❌ **普通照片**：非球面投影 → 强行套球面会变形，建议用普通看图软件

---

## ❓ 常见问题

**Q: 为什么我直接双击 index.html，安装按钮和离线功能用不了？**
A: PWA 必须 http(s) 环境。请用上面的本地服务器，或部署到 GitHub Pages。

**Q: 部署后手机打开一片空白？**
A: 检查 GitHub 上 `lib/` 和 `icons/` 文件夹是否都上传成功，浏览器 F12 看 Console 报错。

**Q: iPhone 上 Safari 没看到「安装」按钮？**
A: iOS 设计如此，需手动「分享」→「添加到主屏幕」（页面有提示文字）。

**Q: 图片会传到服务器吗？**
A: 不会。图片用浏览器的 `URL.createObjectURL` 在本地读取，离开你的设备。

**Q: 离线后还能看新图吗？**
A: 能。选图是本地读取，不依赖网络。「离线」指的是 App 本身（界面/库）断网也能打开。
