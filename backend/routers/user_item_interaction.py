from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user_item_interaction import UserItemInteraction as DBUserItemInteraction
from ..schemas.user_item_interaction import UserItemInteraction, UserItemInteractionCreate

router = APIRouter(prefix="/user_item_interactions", tags=["user_item_interactions"])

@router.post("/", response_model=UserItemInteraction)
def create_user_item_interaction(interaction: UserItemInteractionCreate, db: Session = Depends(get_db)):
    db_interaction = DBUserItemInteraction(**interaction.dict())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

@router.get("/", response_model=list[UserItemInteraction])
def read_user_item_interactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    interactions = db.query(DBUserItemInteraction).offset(skip).limit(limit).all()
    return interactions
