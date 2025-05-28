# Gemini WebAPI 工具

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)  
基于 [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API) 的修改。

---

## 目录

- [背景介绍](#背景介绍)  
- [功能亮点](#功能亮点)  
- [环境与依赖](#环境与依赖)  
- [获取 API 凭证](#获取-api-凭证)  
- [调用 API 示例](#调用-api-示例)  
- [常见问题](#常见问题)  
- [许可证](#许可证)  

---

## 背景介绍

快速接入。

---

## 功能亮点

- **自动化凭证获取**：一键在本地或服务器上启动浏览器登录，自动生成 `.env` 配置文件  
- **无 GUI 环境支持**：在无头（Headless）服务器上也能直接调用 API  
- **零依赖安装**：通过两份简单的 `requirements.txt` 分别管理凭证获取与 API 调用依赖  

---

## 环境与依赖

- Python ≥ 3.10 
- 操作系统：Windows / Linux / macOS  
- 推荐使用虚拟环境（`venv`、`conda` 等）隔离项目依赖  

---

## 使用脚本获取 Gemini 凭证

> **注意**：此步骤需要有图形界面（GUI）的机器或服务器，用于弹出浏览器进行Gemini的web登录。
> 
> 以下环境设置了代理`http://127.0.0.1:15665`，可自行在 `.env` 中修改。

1. 克隆项目仓库  
   ```bash
   git clone https://github.com/ztj7728/gemini_webapi.git
   cd gemini_webapi
   ````

2. 安装凭证获取脚本依赖

   ```bash
   mv get_requirements.txt requirements.txt
   pip install -r requirements.txt
   pip install -r requirements.txt
   playwright install chromium
   ```
3. 启动凭证获取脚本

   ```bash
   python get.py
   ```
4. 浏览器会自动打开并跳转到 Gemini 登录页面，使用你的账号登录。
5. 登录完成后，回到终端，按下回车。
6. 脚本会更新根目录下的 `.env` 文件凭证内容：

   ```dotenv
   SECURE_1PSID={}
   SECURE_1PSIDTS={}
   ```
7. 完成！

## 🚀 更优雅地手动获取 Gemini 凭证

> 适用于所有场景，特别是某些安全级别高的账号无法正常在 Playwright 中登录。


### 安装 Cookie Editor 插件

1. 打开浏览器扩展商店  
2. 搜索并安装 “Cookie Editor”  

- **Chrome**：  
  [chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)  
- **Edge**：  
  [microsoftedge.microsoft.com/addons/detail/cookieeditor/neaplmfkghagebokkhpjpoebhdledlfi](https://microsoftedge.microsoft.com/addons/detail/cookieeditor/neaplmfkghagebokkhpjpoebhdledlfi)  
- **Firefox**：  
  [addons.mozilla.org/addon/cookie-editor](https://addons.mozilla.org/addon/cookie-editor)  
- **Safari**：  
  [apps.apple.com/app/apple-store/id6446215341](https://apps.apple.com/app/apple-store/id6446215341)  
- **Opera**：  
  [addons.opera.com/en/extensions/details/cookie-editor-2](https://addons.opera.com/en/extensions/details/cookie-editor-2)  

---

### 登录 Gemini

1. 打开浏览器，访问：https://gemini.google.com  
2. 使用你的 Google 账号完成登录流程。

---

### 提取 Cookie 值

1. 点击浏览器工具栏中的 **Cookie Editor** 插件图标  
2. 在搜索框中输入 `SECURE-1PSID`，复制其 **Value**  
3. 同理，搜索并复制 `SECURE-1PSIDTS` 的 **Value**

---

### 配置 `.env` 文件

将值更新至项目根目录下的 `.env` 文件

```dotenv
# Gemini 凭证
SECURE_1PSID={}
SECURE_1PSIDTS={}
````


---

## 调用 API 示例

> 此步骤可在任意无 GUI 环境（例如 Linux 服务器、Docker 容器）中运行。
> 
> 以下环境设置了代理`http://127.0.0.1:15665`，可自行在 `.env` 中修改。

1. 克隆同一仓库（若尚未克隆）

   ```bash
   git clone https://github.com/ztj7728/gemini_webapi.git
   cd gemini_webapi
   ```
2. 安装 API 调用依赖

   ```bash
   mv app_requirements.txt requirements.txt
   pip install -r requirements.txt
   ```
3. 确保项目根目录已有前面步骤生成的 `.env` 文件
4. 运行示例脚本

   ```bash
   python app.py
   ```
5. 完成！

---

## 常见问题

1. **123？**

   * 123。

更多问题可提交 [Issues](https://github.com/ztj7728/gemini_webapi/issues)。

---

## 许可证

本项目遵循 MIT 许可证，详情见 [LICENSE](LICENSE)。
