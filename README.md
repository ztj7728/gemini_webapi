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
- [配置说明](#配置说明)  
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

## 获取 API 凭证

> **注意**：此步骤需要有图形界面（GUI）的机器或服务器，用于弹出浏览器进行Gemini的web登录。

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
4. 浏览器会自动打开并跳转到 Gemini 登录页面，使用你的账号登录。
5. 登录完成后，回到终端，按下回车。
6. 脚本会在项目根目录生成一个 **`.env`** 文件，文件内容如下：

   ```dotenv
   SECURE_1PSID={}
   SECURE_1PSIDTS={}
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
5. 完成！

---


---

## 常见问题

1. **123？**

   * 123。

更多问题可提交 [Issues](https://github.com/ztj7728/gemini_webapi/issues)。

---

## 许可证

本项目遵循 MIT 许可证，详情见 [LICENSE](LICENSE)。
