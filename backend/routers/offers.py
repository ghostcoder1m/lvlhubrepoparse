from fastapi import APIRouter

router = APIRouter()

@router.get("/offers")
async def get_offers():
    return [{"id": 1, "name": "Offer 1"}, {"id": 2, "name": "Offer 2"}]

@router.post("/offers")
async def create_offer(offer: dict):
    return {"id": 3, "name": offer["name"]}
