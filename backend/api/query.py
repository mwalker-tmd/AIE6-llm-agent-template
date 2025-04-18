from fastapi import APIRouter, Form
from fastapi.responses import StreamingResponse, JSONResponse
from core.chatmodel import ChatOpenAI
from core.vector_store import VectorStore
from prompts.prompt_manager import PromptManager

router = APIRouter()
llm = ChatOpenAI()
vector_store = VectorStore()
prompt_manager = PromptManager()

@router.post("/query")
async def query(question: str = Form(...)):
    if not vector_store.is_initialized:
        return JSONResponse(
            status_code=400, 
            content={"error": "No file uploaded yet."}
        )

    context_list = vector_store.search(question)
    context_prompt = "\n".join([ctx[0] for ctx in context_list])
    messages = prompt_manager.create_messages(question, context_prompt)

    async def response_stream():
        async for chunk in llm.astream(messages):
            yield chunk

    return StreamingResponse(response_stream(), media_type="text/plain") 