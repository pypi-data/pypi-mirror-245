import asyncio
from abc import ABC, abstractmethod
from typing import List


class Embeddings(ABC):
    """Interface for embedding models."""

    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs."""

    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Embed query text."""

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """Asynchronous Embed search docs."""
        return await asyncio.get_running_loop().run_in_executor(
            None, self.embed_documents, texts
        )

    async def aembed_query(self, text: str) -> List[float]:
        """Asynchronous Embed query text."""
        return await asyncio.get_running_loop().run_in_executor(
            None, self.embed_query, text
        )

class LMEmbedding(Embeddings):
    from modelscope.pipelines import pipeline
    from modelscope.utils.constant import Tasks
    pipeline_se = pipeline(Tasks.sentence_embedding,model='thomas/text2vec-base-chinese', model_revision='v1.0.0',device="cuda")


    def _costruct_inputs(self,texts):

        inputs = {
                "source_sentence": texts
            }

        return inputs

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs."""

        inputs = self._costruct_inputs(texts)
        result_embeddings = self.pipeline_se(input=inputs)
        return result_embeddings["text_embedding"]

    def embed_query(self, text: str) -> List[float]:
        """Embed query text."""
        inputs = self._costruct_inputs([text])
        result_embeddings = self.pipeline_se(input=inputs)
        return result_embeddings["text_embedding"]


if __name__ == '__main__':
    inputs = "不可以，早晨喝牛奶不科学"
    print(LMEmbedding().embed_query(inputs).shape)


