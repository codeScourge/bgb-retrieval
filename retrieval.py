from sentence_transformers import CrossEncoder
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS


RERANK_MODEL = 'cross-encoder/ms-marco-TinyBERT-L-2-v2'
TOP_K = 20
TOP_N = 8

EMBEDDER = OpenAIEmbeddings()

# after retrieving the articles we need to rerank them using a BERT model with a binary-classification head on the content itself
# export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
cross_encoder = CrossEncoder(RERANK_MODEL)

def rerank(query, retrieved_documents):
    sentence_pairs = [[query, doc.metadata["content"]] for doc in retrieved_documents]
    rerank_scores = cross_encoder.predict(sentence_pairs)

    # add score to documents metadata
    for i in range(len(retrieved_documents)):
        retrieved_documents[i].metadata["rerank_score"] = rerank_scores[i]

    # sort documents by rerank score
    retrieved_documents = sorted(retrieved_documents, key=lambda x: x.metadata["rerank_score"], reverse=True)

    return retrieved_documents[:TOP_N]


def query_index(index, query):
    retrieved_documents = index.similarity_search(query, TOP_K)
    reranked_documents = rerank(query, retrieved_documents)
    return reranked_documents


def print_results(documents):
    for doc in documents:
        print("\n\n")
        print(doc.metadata["content"])


if __name__ == "__main__":
    index = FAISS.load_local('indexes/bgb', EMBEDDER)
    print_results(query_index(index, "GMBH gründen"))
