from fastapi import APIRouter

router = APIRouter()

@router.get("/triggers")
async def get_triggers():
    return [{"id": 1, "name": "Trigger 1"}, {"id": 2, "name": "Trigger 2"}]

@router.post("/triggers")
async def create_trigger(trigger: dict):
    return {"id": 3, "name": trigger["name"]}
