from fastapi import APIRouter

router = APIRouter()

@router.get("/pages")
async def get_pages():
    return [{"id": 1, "title": "Page 1"}, {"id": 2, "title": "Page 2"}]

@router.post("/pages")
async def create_page(page: dict):
    return {"id": 3, "title": page["title"]}
