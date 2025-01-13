from fastapi import APIRouter

router = APIRouter()

@router.get("/aimodels")
async def get_aimodels():
    return [{"id": 1, "name": "AI Model 1"}, {"id": 2, "name": "AI Model 2"}]

@router.post("/aimodels")
async def create_aimodel(aimodel: dict):
    return {"id": 3, "name": aimodel["name"]}
