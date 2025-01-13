from fastapi import APIRouter

router = APIRouter()

@router.get("/funnels")
async def get_funnels():
    return [{"id": 1, "name": "Funnel 1"}, {"id": 2, "name": "Funnel 2"}]

@router.post("/funnels")
async def create_funnel(funnel: dict):
    return {"id": 3, "name": funnel["name"]}
