from dataclasses import dataclass
from typing import (
    List,
    Optional,
    AsyncGenerator,
    AsyncIterator,
)


@dataclass
class SourceDocument:
    document: dict
    document_id: str


class BaseDataSource:
    def stream_documents(
        self,
        query: str,
        limit: int = 0,
    ) -> AsyncIterator[SourceDocument]:
        raise NotImplementedError()

    async def search_documents(
        self,
        query: str,
        limit: int = 5,
    ) -> List[SourceDocument]:
        raise NotImplementedError()
