
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.environ["GROQ_API_KEY"]

# Construct the absolute path to the FAISS index
SCRIPT_DIR = os.path.dirname(__file__)
FAISS_INDEX_PATH = os.path.join(SCRIPT_DIR, "faiss_index")

def get_rag_chain():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()

    # Initialize the LLM (using Groq for now, assuming API key is set in .env)
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        groq_api_key = groq_api_key
    )

    # Create a prompt template for the RAG chain
    prompt = ChatPromptTemplate.from_template(
        """You are a helpful assistant providing flood relief information. Use the provided context to answer the user's question about flood shelters, safety measures, and emergency resources. Provide specific details from the context when available.

    If the user asks about flood-related emergencies, respond with a calm, reassuring, and informative tone appropriate for crisis situations. If the user engages in casual conversation, respond politely while gently steering the conversation toward flood relief topics.

    Context: {context}

    Question: {input}"""
    )

    # Create a document combining chain (stuff documents into the prompt)
    document_chain = create_stuff_documents_chain(llm, prompt)

    # Create the retrieval chain
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    return retrieval_chain

