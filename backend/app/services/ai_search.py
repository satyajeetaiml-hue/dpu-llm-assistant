"""Azure AI Search client for hybrid (keyword + vector) retrieval."""
from __future__ import annotations

from functools import lru_cache
from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
    VectorSearch,
    VectorSearchProfile,
)
from azure.search.documents.models import VectorizedQuery

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@lru_cache
def _search_client() -> SearchClient:
    s = get_settings()
    return SearchClient(
        endpoint=s.azure_search_endpoint,
        index_name=s.azure_search_index_name,
        credential=AzureKeyCredential(s.azure_search_api_key),
    )


@lru_cache
def _index_client() -> SearchIndexClient:
    s = get_settings()
    return SearchIndexClient(
        endpoint=s.azure_search_endpoint,
        credential=AzureKeyCredential(s.azure_search_api_key),
    )


class AISearchService:
    """Wraps document upload, index creation and hybrid search."""

    def __init__(self) -> None:
        self._settings = get_settings()

    def ensure_index(self) -> None:
        """Create the search index if it does not already exist."""
        s = self._settings
        fields = [
            SimpleField(name="id", type=SearchFieldDataType.String, key=True),
            SearchableField(name="content", type=SearchFieldDataType.String),
            SimpleField(
                name="source", type=SearchFieldDataType.String, filterable=True
            ),
            SimpleField(
                name="category", type=SearchFieldDataType.String, filterable=True
            ),
            SimpleField(name="page", type=SearchFieldDataType.Int32),
            SearchField(
                name="content_vector",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=s.embedding_dimensions,
                vector_search_profile_name="default-profile",
            ),
        ]
        vector_search = VectorSearch(
            algorithms=[HnswAlgorithmConfiguration(name="default-hnsw")],
            profiles=[
                VectorSearchProfile(
                    name="default-profile",
                    algorithm_configuration_name="default-hnsw",
                )
            ],
        )
        index = SearchIndex(
            name=s.azure_search_index_name,
            fields=fields,
            vector_search=vector_search,
        )
        _index_client().create_or_update_index(index)
        logger.info("Ensured search index '%s'", s.azure_search_index_name)

    def upload_documents(self, documents: list[dict[str, Any]]) -> int:
        """Upsert documents into the index. Returns the number uploaded."""
        if not documents:
            return 0
        result = _search_client().merge_or_upload_documents(documents=documents)
        succeeded = sum(1 for r in result if r.succeeded)
        logger.info("Uploaded %d/%d documents", succeeded, len(documents))
        return succeeded

    def hybrid_search(
        self,
        query_text: str,
        query_vector: list[float],
        *,
        top_k: int | None = None,
        category: str | None = None,
    ) -> list[dict[str, Any]]:
        """Run a hybrid keyword + vector search and return matched documents."""
        top_k = top_k or self._settings.retrieval_top_k
        vector_query = VectorizedQuery(
            vector=query_vector,
            k_nearest_neighbors=top_k,
            fields="content_vector",
        )
        filter_expr = f"category eq '{category}'" if category else None
        results = _search_client().search(
            search_text=query_text,
            vector_queries=[vector_query],
            filter=filter_expr,
            top=top_k,
            select=["id", "content", "source", "category", "page"],
        )
        return [dict(r) for r in results]


@lru_cache
def get_search_service() -> AISearchService:
    return AISearchService()
