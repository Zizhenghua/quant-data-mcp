"""
Quant Data MCP Server

把 Quant Data API 包装成 MCP 工具。
"""

import asyncio
import json
from typing import Any, Dict, List

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server

from .client import QuantDataClient


# 创建 MCP Server
app = Server("quant-data-mcp")

# 全局 client
_client: QuantDataClient = None
_tools_cache: List[Dict[str, Any]] = []


def get_client() -> QuantDataClient:
    global _client
    if _client is None:
        _client = QuantDataClient()
    return _client


def load_tools() -> List[Dict[str, Any]]:
    """从后端加载工具列表"""
    global _tools_cache
    if not _tools_cache:
        client = get_client()
        _tools_cache = client.get_tools()
    return _tools_cache


@app.list_tools()
async def list_tools() -> List[types.Tool]:
    """MCP 协议：列出所有工具"""
    tools = load_tools()
    result = []
    for t in tools:
        fn = t.get("function", {})
        result.append(
            types.Tool(
                name=fn.get("name", ""),
                description=fn.get("description", ""),
                inputSchema=fn.get("parameters", {"type": "object", "properties": {}}),
            )
        )
    return result


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """MCP 协议：调用工具"""
    client = get_client()

    try:
        # 根据工具名，调对应的后端 API
        if name == "get_stock_realtime":
            code = arguments["code"]
            data = client.call("GET", f"/stock/realtime/{code}")

        elif name == "get_stock_kline":
            code = arguments["code"]
            params = {}
            if arguments.get("startDate"):
                params["startDate"] = arguments["startDate"]
            if arguments.get("endDate"):
                params["endDate"] = arguments["endDate"]
            data = client.call("GET", f"/stock/detail/{code}", params=params)

        elif name == "get_market_stats":
            data = client.call("GET", "/market/stats")

        elif name == "get_sector_performance":
            data = client.call("GET", "/sector/performance")

        elif name == "filter_stocks":
            data = client.call("POST", "/stock/filter", json=arguments)

        elif name == "get_fin_latest":
            code = arguments["code"]
            data = client.call("GET", f"/fin/latest/{code}")

        else:
            return [
                types.TextContent(
                    type="text",
                    text=f"未知工具: {name}",
                )
            ]

        return [
            types.TextContent(
                type="text",
                text=json.dumps(data, ensure_ascii=False, indent=2),
            )
        ]

    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"调用失败: {e}",
            )
        ]


async def run():
    """启动 MCP Server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


def main():
    """入口"""
    asyncio.run(run())


if __name__ == "__main__":
    main()