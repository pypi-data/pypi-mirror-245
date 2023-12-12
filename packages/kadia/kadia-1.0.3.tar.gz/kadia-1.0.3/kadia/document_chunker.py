import logging
from dataclasses import dataclass
from datetime import datetime
from typing import (
    List,
)

from izihawa_textutils.utils import remove_markdown
from stc_geck.advices import BaseDocumentHolder
from unstructured.cleaners.core import clean

from kadia.text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

BANNED_SECTIONS = {
    "author contribution",
    "data availability statement",
    "declaration of competing interest",
    "acknowledgments",
    "acknowledgements",
    "supporting information",
    "conflict of interest disclosures",
    "conflict of interest",
    "conflict of interest statement",
    "ethics statement",
    "references",
    "external links",
    "further reading",
    "works cited",
    "bibliography",
    "notes",
    "sources",
    "footnotes",
    "suggested readings",
}


@dataclass
class Chunk:
    document_id: str
    field: str
    chunk_id: int
    title: str
    text: str
    start_index: int
    length: int


@dataclass
class StoredChunk:
    document_id: str
    field: str
    chunk_id: int
    title: str
    start_index: int
    length: int


def extract_title_parts(document_holder, split):
    title_parts = [document_holder.title]
    for hn in range(6):
        if hn_value := split.metadata.get(f"h{hn}"):
            title_parts.append(hn_value)
    return title_parts


class DocumentChunker:
    def __init__(
        self,
        chunk_size: int = 1024,
        chunk_overlap: int = 128,
        add_metadata: bool = False,
        add_year: bool = True,
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            keep_separator=True,
            strip_whitespace=True,
            length_function=lambda text: len(remove_markdown(text)),
        )
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.add_metadata = add_metadata
        self.add_year = add_year

    def _splits_to_chunks(
        self, document_holder: BaseDocumentHolder, field: str, splits
    ):
        chunks = []
        for chunk_id, split in enumerate(splits):
            page_content = str(split.page_content)
            chunk_text = clean(
                remove_markdown(page_content),
                extra_whitespace=True,
                dashes=True,
                bullets=True,
                trailing_punctuation=True,
            )
            parts = [chunk_text]
            title_parts = extract_title_parts(document_holder, split)
            if len(chunk_text) < 128 or any(
                [title_part.lower() == "references" for title_part in title_parts]
            ):
                continue
            if self.add_metadata:
                parts.append(f'TITLE: {" ".join(title_parts)}')
                if document_holder.has_field("keywords"):
                    keywords = ", ".join(document_holder.keywords)
                    parts.append(f"KEYWORDS: {keywords}")
                if document_holder.has_field("tags"):
                    tags = ", ".join(document_holder.tags)
                    parts.append(f"TAGS: {tags}")
            if self.add_year and document_holder.has_field("issued_at"):
                issued_at = datetime.utcfromtimestamp(document_holder.issued_at)
                parts.append(f"YEAR: {issued_at.year}")
            text = "\n".join(parts)
            chunks.append(
                Chunk(
                    document_id=document_holder.get_id(),
                    field=field,
                    chunk_id=chunk_id,
                    title="\n".join(title_parts),
                    text=text,
                    start_index=split.metadata["start_index"],
                    length=len(page_content),
                )
            )
        return chunks

    def to_chunks(self, document_holder: BaseDocumentHolder) -> List[Chunk]:
        logging.getLogger("statbox").info(
            {
                "action": "chunking",
                "document_id": document_holder.get_id(),
                "mode": "kadia",
            }
        )
        document = document_holder.document
        abstract = document.get("abstract", "")
        content = document.get("content", "")

        headers_to_split_on = [
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
            ("####", "h4"),
            ("#####", "h5"),
            ("######", "h6"),
        ]

        # MD splits
        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on
        )
        md_abstract_header_splits = markdown_splitter.split_text(abstract)
        md_content_header_splits = markdown_splitter.split_text(content)

        # Split
        abstract_splits = self.text_splitter.split_documents(md_abstract_header_splits)
        content_splits = self.text_splitter.split_documents(md_content_header_splits)

        chunks = []
        chunks.extend(
            self._splits_to_chunks(document_holder, "abstract", abstract_splits)
        )
        chunks.extend(
            self._splits_to_chunks(document_holder, "content", content_splits)
        )

        return chunks
