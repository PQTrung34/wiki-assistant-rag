import fastapi
from fastapi.middleware.cors import CORSMiddleware
from vector_store.vector_store import VectorStore
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer

app = fastapi.FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Vector store
vector_store = VectorStore().load_db()

# local model
MODEL_NAME = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
qa_pipeline = pipeline("text2text-generation", model=MODEL_NAME)

class SearchQuery(BaseModel):
    query: str
    k: int

@app.get("/test")
async def test():
    return {"message": "Hello World"}

class ChatQuery(BaseModel):
    query: str

@app.post("/search")
async def search(req: SearchQuery):
    # result = vector_store.similarity_search(req.query, k=req.k)
    retriever = vector_store.as_retriever(search_kwargs={"k": req.k})
    result = retriever.invoke(req.query)
    return {"result": result}

@app.post("/chat")
async def chat(req: ChatQuery):
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(req.query)

    # Context
    context = "\n".join([d.page_content for d in docs]) if docs else ""

    # System message
    system_message = (
        "Bạn là một trợ lý AI hữu ích. Luôn trả lời bằng tiếng Việt, ngắn gọn và rõ ràng.\n"
        "Chỉ trả lời dựa trên nội dung được cung cấp.\n"
        "Nếu thông tin không đủ, hãy trả lời 'Tôi không biết'."
    )

    # Tránh vượt quá max_length của model
    max_input_tokens = tokenizer.model_max_length - 128
    prompt = f"{system_message}\n\nNgữ cảnh:\n{context}\n\nCâu hỏi: {req.query}\n\nTrả lời:"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=max_input_tokens)

    # Sinh câu trả lời
    result = qa_pipeline(prompt, max_new_tokens=256, do_sample=False)
    return {
        "result": result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)