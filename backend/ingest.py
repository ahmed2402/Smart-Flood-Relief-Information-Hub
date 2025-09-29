
import json
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

DATA_PATH = "./data/shelters.json"
FAISS_INDEX_PATH = "./faiss_index"

def ingest_data():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        shelters_data = json.load(f)

    documents = []
    for shelter in shelters_data:
        content = f"Shelter Name: {shelter['name']}. Address: {shelter['address']}. City: {shelter['city']}. Capacity: {shelter['capacity']}. Services: {shelter['services']}. Notes: {shelter['notes']}"
        documents.append(Document(page_content=content, metadata={"id": shelter["id"], "name": shelter["name"], "city": shelter["city"]}))

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(FAISS_INDEX_PATH)
    print(f"FAISS index saved to {FAISS_INDEX_PATH}")

if __name__ == "__main__":
    ingest_data()
