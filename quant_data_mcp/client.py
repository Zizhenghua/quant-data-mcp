"""
调后端 HTTP API 的客户端
"""

import os
from typing import Any, Dict, Optional

import httpx

DEFAULT_BASE_URL = "https://zizhenghua.com/api"
USER_AGENT = "quant-data-mcp/1.0.0"


class QuantDataClient:
    """调 Quant Data API 的客户端"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: int = 30,
    ):
        self.api_key = api_key or os.getenv("QUANT_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        headers = {"User-Agent": USER_AGENT}
        if self.api_key:
            headers["X-API-Key"] = self.api_key

        self._client = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout,
        )

    def _request(self, method: str, path: str, **kwargs) -> Any:
        resp = self._client.request(method, path, **kwargs)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict) and "success" in data:
            if not data["success"]:
                raise RuntimeError(data.get("message", "Unknown error"))
            return data.get("data")
        return data

    def get_tools(self) -> list:
        """获取工具列表"""
        data = self._request("GET", "/agent/tools")
        return data.get("tools", [])

    def call(self, method: str, path: str, **kwargs) -> Any:
        """通用请求"""
        return self._request(method, path, **kwargs)

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()