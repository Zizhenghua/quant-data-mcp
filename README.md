# Quant Data MCP Server

[![PyPI](https://img.shields.io/pypi/v/zizhenghua-mcp.svg)](https://pypi.org/project/zizhenghua-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/pypi/pyversions/zizhenghua-mcp.svg)](https://pypi.org/project/zizhenghua-mcp/)

MCP Server for [Quant Data API](https://zizhenghua.com).

让 Claude Desktop / Cursor 等 MCP 客户端能直接调 A 股数据。

---

## ✨ 功能

- 📈 个股实时行情
- 📊 个股 K 线
- 📉 市场统计
- 🏭 行业涨跌幅
- 🔍 多条件选股
- 💰 最新财务指标

---

## 📦 安装

```bash
pip install zizhenghua-mcp
```

或从源码：

```bash
git clone https://github.com/Zizhenghua/quant-data-mcp.git
cd quant-data-mcp
pip install -e .
```

---

## 🚀 配置

### Claude Desktop

编辑配置文件：

- **Windows**：`%APPDATA%\Claude\claude_desktop_config.json`
- **Mac**：`~/Library/Application Support/Claude/claude_desktop_config.json`

内容：

```json
{
  "mcpServers": {
    "quant-data": {
      "command": "python",
      "args": ["-m", "quant_data_mcp.server"],
      "env": {
        "QUANT_API_KEY": ""
      }
    }
  }
}
```

### Cursor

在 Cursor 设置里加 MCP Server，或编辑 `~/.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "quant-data": {
      "command": "python",
      "args": ["-m", "quant_data_mcp.server"],
      "env": {
        "QUANT_API_KEY": ""
      }
    }
  }
}
```

---

## 🔑 用 API Key

默认匿名调用（10 次/分钟）。

想提高限额，在配置里填 `QUANT_API_KEY`：

```json
{
  "env": {
    "QUANT_API_KEY": "your_api_key_here"
  }
}
```

注册获取 API Key：https://zizhenghua.com

---

## 💬 示例

配好后，在 Claude Desktop / Cursor 里问：

- "茅台现在多少钱？"
- "帮我看看 600519 最近的 K 线"
- "今天市场涨跌家数怎么样？"
- "哪些行业今天涨得最好？"
- "帮我筛选换手率大于 5% 的股票"
- "600519 最新的财务指标是什么？"

AI 会自动调对应的工具。

---

## 🛠️ 可用工具

| 工具 | 说明 |
|------|------|
| `get_stock_realtime` | 个股实时行情 |
| `get_stock_kline` | 个股 K 线 |
| `get_market_stats` | 市场统计 |
| `get_sector_performance` | 行业涨跌幅 |
| `filter_stocks` | 多条件选股 |
| `get_fin_latest` | 最新财务指标 |

---

## 🧪 开发

```bash
# 1. Clone
git clone https://github.com/Zizhenghua/quant-data-mcp.git
cd quant-data-mcp

# 2. 虚拟环境
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac / Linux

# 3. 安装
pip install -e ".[dev]"

# 4. 测试
python -m quant_data_mcp.server
```

---

## 📚 相关项目

- [quant-data-sdk](https://github.com/Zizhenghua/quant-data-sdk) — Python / JS SDK
- [Quant Data API](https://zizhenghua.com) — 数据接口

---

## 📄 License

[MIT](LICENSE)

---

## ⚠️ Disclaimer

数据仅供量化学习与策略回测研究之用，不构成任何投资建议。