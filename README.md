````markdown
# Gemini WebAPI 工具

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)  
基于 [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API) 的二次封装，提供一套在有 GUI 与无 GUI 环境下快速获取凭证并调用 Gemini API 的脚本。

---

## 目录

- [背景介绍](#背景介绍)  
- [功能亮点](#功能亮点)  
- [环境与依赖](#环境与依赖)  
- [获取 API 凭证](#获取-api-凭证)  
- [调用 API 示例](#调用-api-示例)  
- [配置说明](#配置说明)  
- [常见问题](#常见问题)  
- [许可证](#许可证)  

---

## 背景介绍

Gemini 是一款安全、专业的加密货币交易所，官方提供了 [Gemini-API](https://github.com/HanaokaYuzu/Gemini-API) Python 库。本项目在此基础上增加了自动化获取 API 凭证的脚本，并封装了一个轻量级的 `app.py` 示例程序，方便不同环境下快速接入。

---

## 功能亮点

- **自动化凭证获取**：一键在本地或服务器上启动浏览器登录，自动生成 `.env` 配置文件  
- **无 GUI 环境支持**：在无头（Headless）服务器上也能直接调用 API  
- **零依赖安装**：通过两份简单的 `requirements.txt` 分别管理凭证获取与 API 调用依赖  
- **示例清晰**：`app.py` 中包含基础的行情查询、下单等调用示例  

---

## 环境与依赖

- Python ≥ 3.8  
- 操作系统：Windows / Linux / macOS  
- 推荐使用虚拟环境（`venv`、`conda` 等）隔离项目依赖  

---

## 获取 API 凭证

> **注意**：此步骤需要有图形界面（GUI）的机器或服务器，用于弹出浏览器进行 OAuth 登录。

1. 克隆项目仓库  
   ```bash
   git clone https://github.com/ztj7728/gemini_webapi.git
   cd gemini_webapi
````

2. 安装凭证获取脚本依赖

   ```bash
   mv get_requirements.txt requirements.txt
   pip install -r requirements.txt
   ```
3. 启动凭证获取脚本

   ```bash
   python get.py
   ```
4. 浏览器会自动打开并跳转到 Gemini 登录页面，使用你的账号登录并允许授权
5. 登录完成后，回到终端，按下回车
6. 脚本会在项目根目录生成一个 **`.env`** 文件，文件内容如下：

   ```dotenv
   GEMINI_API_KEY=你的API_KEY
   GEMINI_API_SECRET=你的API_SECRET
   GEMINI_PASSPHRASE=（如适用）
   ```
7. 完成！

---

## 调用 API 示例

此步骤可在任意无 GUI 环境（例如 Linux 服务器、Docker 容器）中运行。

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
5. 根据脚本输出，查看行情、下单、查询订单状态等示例调用结果

---

## 配置说明

所有关键配置均来自项目根目录的 `.env` 文件，支持以下变量：

| 变量                  | 说明                   | 示例                       |
| ------------------- | -------------------- | ------------------------ |
| `GEMINI_API_KEY`    | 您的 Gemini API Key    | `abcd1234...`            |
| `GEMINI_API_SECRET` | 您的 Gemini API Secret | `wxyz5678...`            |
| `GEMINI_PASSPHRASE` | （可选）API Passphrase   | `my_passphrase`          |
| `GEMINI_API_URL`    | （可选）API 基础地址         | `https://api.gemini.com` |

可根据需要自行添加或覆盖环境变量。

---

## 常见问题

1. **获取凭证时浏览器未弹出？**

   * 请确认所在环境支持 GUI，如 X11 转发；或手动复制 `get.py` 中的授权 URL 到本地浏览器登录后，将回调中的 `code` 粘贴回终端。
2. **.env 无法生成或缺少变量？**

   * 检查 `get.py` 执行日志，确保 OAuth 流程正常完成。
3. **API 调用报错 401 Unauthorized？**

   * 确保 `.env` 中的 `GEMINI_API_KEY`/`SECRET` 正确无误，且账户已开通 API 权限。

更多问题可提交 [Issues](https://github.com/ztj7728/gemini_webapi/issues)。

---

## 许可证

本项目遵循 MIT 许可证，详情见 [LICENSE](LICENSE)。

---

> **小贴士**：
>
> * 强烈建议将 `.env` 文件加入 `.gitignore`，不要将凭证上传至公共仓库。
> * 如需扩展功能，可参考官方 [Gemini-API 文档](https://docs.gemini.com/)。

```
```
