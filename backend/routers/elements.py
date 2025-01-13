from fastapi import APIRouter

router = APIRouter()

@router.get("/elements")
async def get_elements():
    return [{"id": 1, "name": "Element 1"}, {"id": 2, "name": "Element 2"}]

@router.post("/elements")
async def create_element(element: dict):
    return {"id": 3, "name": element["name"]}
