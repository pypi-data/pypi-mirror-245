from typing import List

from langchain.embeddings import (
    HuggingFaceBgeEmbeddings,
    HuggingFaceInstructEmbeddings,
    OpenAIEmbeddings,
)


class Embedder:
    """
    Utility class that manages all nested AI models required for Kadia to be functional.
    Mainly consists of configs and models instances.
    """

    def __init__(
        self, model_type: str, model_name: str, model_kwargs: dict | None = None
    ):
        self.model_name = model_name
        match model_type:
            case "instructor":
                self._embedder = HuggingFaceInstructEmbeddings(
                    model_name=model_name,
                    model_kwargs=model_kwargs,
                    embed_instruction="Represent science paragraph for retrieval",
                    query_instruction="Represent science question for retrieval",
                )
            case "bge":
                self._embedder = HuggingFaceBgeEmbeddings(
                    model_name=model_name,
                    model_kwargs=model_kwargs,
                    encode_kwargs={"normalize_embeddings": True},
                )
            case "openai":
                self._embedder = OpenAIEmbeddings(model=model_name)
            case _:
                raise ValueError("Unsupported embedding model")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed texts into vectors using selected models

        :param texts: a list of texts
        :return: list of vectors
        """
        return self._embedder.embed_documents(texts)

    def get_embeddings_id(self):
        return self.model_name.replace("/", "-")
