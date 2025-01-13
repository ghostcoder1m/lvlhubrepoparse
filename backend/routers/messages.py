from fastapi import APIRouter

router = APIRouter()

@router.get("/messages")
async def get_messages():
    return [{"id": 1, "content": "Hello, World!"}, {"id": 2, "content": "Welcome to the API!"}]

@router.post("/messages")
async def create_message(message: dict):
    return {"id": 3, "content": message["content"]}
