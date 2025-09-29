
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag import get_rag_chain

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],  # Adjust this to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for incoming queries
class QueryRequest(BaseModel):
    query: str

# Load the RAG chain once when the application starts
rag_chain = get_rag_chain()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/query")
async def query_rag(request: QueryRequest):
    try:
        response = rag_chain.invoke({"input": request.query})
        return {"answer": response["answer"]}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
