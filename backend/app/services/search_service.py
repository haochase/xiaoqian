"""搜索服务 — 根据话题类别调用对应的搜索 API"""
import json
from typing import Optional
import httpx

from app.core.config import settings


async def search_by_topic(
    category: str,
    keywords: list[str],
    search_window_days: int = 3,
) -> dict:
    """根据话题类别执行搜索，返回结构化结果
    
    Returns:
        {
            "category": str,
            "results": [{"title": str, "content": str, "url": str, "date": str}, ...],
            "raw_summary": str,
        }
    """
    if category == "weather":
        return await _search_weather(keywords)
    elif category == "price":
        return await _search_tavily(keywords, search_window_days, "今日价格 最新行情")
    elif category == "celebrity":
        return await _search_tavily(keywords, max(search_window_days, 7), "最新动态 新闻")
    elif category == "news":
        return await _search_tavily(keywords, search_window_days, "最新资讯 行业动态")
    else:  # custom
        return await _search_tavily(keywords, search_window_days, "")


async def _search_tavily(
    keywords: list[str],
    search_window_days: int,
    extra_query: str,
) -> dict:
    """使用 Tavily Search API 检索"""
    query = " ".join(keywords)
    if extra_query:
        query = f"{query} {extra_query}"

    # 如果配置了 Tavily API key
    if hasattr(settings, "TAVILY_API_KEY") and settings.TAVILY_API_KEY:
        try:
            from tavily import TavilyClient
            client = TavilyClient(api_key=settings.TAVILY_API_KEY)
            response = client.search(
                query=query,
                search_depth="basic",
                max_results=5,
                days=search_window_days,
            )
            results = [
                {
                    "title": r.get("title", ""),
                    "content": r.get("content", ""),
                    "url": r.get("url", ""),
                    "date": "",
                }
                for r in (response.get("results", []) or [])
            ]
            return {
                "category": "search",
                "results": results,
                "raw_summary": response.get("answer", "") or _format_summary(results),
            }
        except Exception:
            pass

    # 降级：返回模拟数据（开发阶段或 API 不可用时）
    return _mock_search(keywords, search_window_days)


async def _search_weather(keywords: list[str]) -> dict:
    """天气查询 — 优先使用和风天气 API"""
    city = keywords[0] if keywords else "北京"

    if hasattr(settings, "QWEATHER_API_KEY") and settings.QWEATHER_API_KEY:
        try:
            async with httpx.AsyncClient() as client:
                # 先查城市 ID
                geo_resp = await client.get(
                    "https://geoapi.qweather.com/v2/city/lookup",
                    params={"location": city, "key": settings.QWEATHER_API_KEY},
                )
                geo_data = geo_resp.json()
                if geo_data.get("code") == "200" and geo_data.get("location"):
                    location_id = geo_data["location"][0]["id"]

                    # 查 3 天天气
                    weather_resp = await client.get(
                        "https://devapi.qweather.com/v7/weather/3d",
                        params={"location": location_id, "key": settings.QWEATHER_API_KEY},
                    )
                    weather_data = weather_resp.json()
                    if weather_data.get("code") == "200":
                        daily = weather_data.get("daily", [])
                        results = [
                            {
                                "title": f"{d.get('fxDate', '')} {city}天气",
                                "content": f"{d.get('textDay', '')}，{d.get('tempMin', '')}°C ~ {d.get('tempMax', '')}°C，{d.get('windDirDay', '')}{d.get('windScaleDay', '')}级",
                                "url": "",
                                "date": d.get("fxDate", ""),
                            }
                            for d in daily
                        ]
                        return {
                            "category": "weather",
                            "results": results,
                            "raw_summary": _format_summary(results),
                        }
        except Exception:
            pass

    # 降级：返回模拟数据
    return _mock_weather(city)


def _format_summary(results: list[dict]) -> str:
    """格式化搜索结果为摘要文本"""
    if not results:
        return "暂无相关内容"
    parts = [f"- {r['title']}: {r['content'][:100]}" for r in results[:5]]
    return "\n".join(parts)


def _mock_search(keywords: list[str], days: int) -> dict:
    """开发阶段模拟搜索结果"""
    kw = "、".join(keywords)
    return {
        "category": "search",
        "results": [
            {
                "title": f"关于「{kw}」的最新信息",
                "content": f"这是关于「{kw}」的模拟检索结果。在生产环境中，这里会是从搜索引擎获取的真实新闻、价格或资讯数据。检索窗口：近 {days} 天。",
                "url": "https://example.com/news/1",
                "date": "2026-04-30",
            },
            {
                "title": f"「{kw}」相关动态",
                "content": f"第二条关于「{kw}」的模拟内容。涵盖了近期的相关动态和变化趋势。",
                "url": "https://example.com/news/2",
                "date": "2026-04-29",
            },
        ],
        "raw_summary": f"今日「{kw}」相关资讯共 2 条，涵盖最新动态。",
    }


def _mock_weather(city: str) -> dict:
    """开发阶段模拟天气数据"""
    return {
        "category": "weather",
        "results": [
            {
                "title": f"{city} 今日天气",
                "content": "晴转多云，18°C ~ 26°C，东南风 2-3 级",
                "url": "",
                "date": "2026-04-30",
            },
            {
                "title": f"{city} 明日天气",
                "content": "多云，16°C ~ 24°C，东北风 1-2 级",
                "url": "",
                "date": "2026-05-01",
            },
        ],
        "raw_summary": f"{city}最近两天天气以晴和多云为主，温度在 16-26°C 之间，适宜出行。",
    }
