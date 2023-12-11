# LM AI Similarity Search
import torch
import math


class LMASS:
    def __init__(self):
        super().__init__()
        self.texts = []
        self.vectors = []
        self.embedding_class = None

    def from_documents(self,docs,embedding_class):

        texts =  [doc.page_content for doc in docs]
        self.texts = texts
        self.docs = docs
        self.embedding_class = embedding_class

        self.vectors = embedding_class.embed_documents(texts)
        return self.vectors

    def get_relevant_documents(self,query,k = 3):
        query_vector = self.embedding_class.embed_query(query)
        sorted_index = self.get_similarity_vector_indexs(query_vector,self.vectors,k = k)
        sorted_docs = [self.docs[id] for id in sorted_index]

        return sorted_docs


    def get_similarity_vector_indexs(self, query_vector ,vectors, k: int = 3,  ):
        similarity = self._cosine_similaritys(query_vector,vectors)

        #这里是按分值从大到小的进行排序
        # 使用sort()函数对tensor进行降序排序，并返回排序后的tensor和索引
        sorted_tensor, sorted_indices = torch.sort(similarity, descending=True)
        return sorted_indices[:k].numpy()


    def _cosine_similaritys(self, query_vector, vectors):
        query_vector = torch.from_numpy(query_vector)
        vectors = torch.from_numpy(vectors)
        similarity_matrix = torch.nn.functional.cosine_similarity(query_vector, vectors, dim=-1)
        return similarity_matrix

        #CosineSimilarity
    def cosine_similarity(self, query_vector, tensor_2):
        normalized_tensor_1 = query_vector / query_vector.norm(dim=-1, keepdim=True)
        normalized_tensor_2 = tensor_2 / tensor_2.norm(dim=-1, keepdim=True)
        return (normalized_tensor_1 * normalized_tensor_2).sum(dim=-1)

    #DotProductSimilarity
    def dot_product_similarity(self, query_vector, tensor_2, scale_output = True):
        result = (query_vector * tensor_2).sum(dim=-1)
        if scale_output:
            # TODO why allennlp do multiplication at here ?
            result /= math.sqrt(query_vector.size(-1))
        return result


if __name__ == '__main__':
    v1 = torch.randn(size=(1,768))
    v2 = torch.randn(size=(4,768))
    lmass = LMASS()
    #print(lmass.dot_product_similarity(v1, v2))
    #print(lmass.cosine_similarity(v1, v2))
    sim_index = lmass.get_similarity_vector_indexs(v1,v2)


