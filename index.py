from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import json


# SET OPENAI_API_KEY ENVIRONMENT VARIABLE
EMBEDDER = OpenAIEmbeddings()

def create_index_from_json(path_data, path_index):
    with open(path_data, 'r') as infile:
        data = json.load(infile)

    # we query by the title
    texts = []
    metas = []

    for object in data:
        texts.append(object["title"])
        metas.append({"jurabk": object["jurabk"], "enbez": object["enbez"], "content": object["content"]})

    index = FAISS.from_texts(texts, EMBEDDER, metas)
    index.save_local(path_index)


if __name__ == "__main__":
    create_index_from_json('data/output/bgb.json', 'indexes/bgb')
