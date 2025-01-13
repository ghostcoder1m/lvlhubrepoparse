from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db  # Updated to relative import
from ..models.workflow import Workflow as DBWorkflow
from ..schemas.workflow import Workflow, WorkflowCreate

router = APIRouter(prefix="/api/workflows", tags=["workflows"])

@router.get("/", response_model=list[Workflow])
def get_workflows(db: Session = Depends(get_db)):
    workflows = db.query(DBWorkflow).all()
    return workflows

@router.post("/", response_model=Workflow)
def create_workflow(workflow: WorkflowCreate, db: Session = Depends(get_db)):
    db_workflow = DBWorkflow(**workflow.dict())
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    return db_workflow