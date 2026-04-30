"""向量服务 — Chroma 集成，用于内容去重"""
from typing import Optional

from app.core.config import settings


# 懒加载 Chroma 客户端
_chroma_client = None
_collection = None


def _get_collection():
    """获取或初始化 Chroma collection"""
    global _chroma_client, _collection
    if _collection is not None:
        return _collection

    try:
        import chromadb
        from chromadb.config import Settings as ChromaSettings

        # 本地持久化模式
        persist_dir = getattr(settings, "CHROMA_PERSIST_DIR", "./chroma_data")
        _chroma_client = chromadb.PersistentClient(
            path=persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        _collection = _chroma_client.get_or_create_collection(
            name="topic_history",
            metadata={"hnsw:space": "cosine"},
        )
        return _collection
    except Exception as e:
        print(f"Chroma 初始化失败: {e}，去重功能降级为简单模式")
        return None


def _get_embedding(text: str) -> Optional[list[float]]:
    """获取文本的向量嵌入"""
    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=settings.LLM_API_KEY,
            base_url=settings.LLM_API_BASE_URL,
        )

        # 截断过长文本
        truncated = text[:8000] if len(text) > 8000 else text

        response = client.embeddings.create(
            model=getattr(settings, "EMBED_MODEL", "text-embedding-3-small"),
            input=truncated,
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Embedding 生成失败: {e}")
        return None


def add_to_history(topic_id: str, summary: str) -> Optional[str]:
    """将聊天摘要存入向量库，返回 chroma_id"""
    collection = _get_collection()
    if not collection:
        return None

    embedding = _get_embedding(summary)
    if not embedding:
        return None

    import uuid
    chroma_id = f"topic_{topic_id}_{uuid.uuid4().hex[:8]}"

    try:
        collection.add(
            ids=[chroma_id],
            embeddings=[embedding],
            metadatas=[{"topic_id": topic_id, "summary": summary[:500]}],
        )
        return chroma_id
    except Exception as e:
        print(f"写入 Chroma 失败: {e}")
        return None


def check_duplicate(topic_id: str, content: str, threshold: float = 0.85) -> tuple[bool, Optional[float]]:
    """检查内容是否与历史重复
    
    Args:
        topic_id: 话题 ID
        content: 待检查的内容
        threshold: 相似度阈值，超过此值视为重复

    Returns:
        (is_duplicate, similarity_score)
    """
    collection = _get_collection()
    if not collection:
        return False, None

    # 查询该话题下的历史
    try:
        existing = collection.get(
            where={"topic_id": topic_id},
        )
    except Exception:
        return False, None

    if not existing or not existing.get("ids"):
        return False, None

    embedding = _get_embedding(content)
    if not embedding:
        return False, None

    try:
        results = collection.query(
            query_embeddings=[embedding],
            n_results=min(5, len(existing["ids"])),
            where={"topic_id": topic_id},
        )
    except Exception:
        return False, None

    if not results or not results.get("distances"):
        return False, None

    # distances 是余弦距离，越小越相似
    min_distance = min(results["distances"][0]) if results["distances"][0] else 1.0
    similarity = 1.0 - min_distance

    if similarity >= threshold:
        return True, similarity

    return False, similarity
