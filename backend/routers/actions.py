from fastapi import APIRouter

router = APIRouter()

@router.get("/actions")
async def get_actions():
    return [{"id": 1, "name": "Action 1"}, {"id": 2, "name": "Action 2"}]

@router.post("/actions")
async def create_action(action: dict):
    return {"id": 3, "name": action["name"]}
