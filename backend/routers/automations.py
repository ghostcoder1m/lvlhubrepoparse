from fastapi import APIRouter

router = APIRouter()

@router.get("/automations")
async def get_automations():
    return [{"id": 1, "name": "Automation 1"}, {"id": 2, "name": "Automation 2"}]

@router.post("/automations")
async def create_automation(automation: dict):
    return {"id": 3, "name": automation["name"]}
