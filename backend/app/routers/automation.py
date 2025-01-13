from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db
from app.schemas.automation import (
    AutomationRule,
    AutomationRuleCreate,
    AutomationRuleUpdate,
    EmailTemplate,
    EmailTemplateCreate,
    EmailTemplateUpdate,
    CampaignAutomation,
    CampaignAutomationCreate,
)
from app.crud import automation as crud

router = APIRouter(prefix="/automation", tags=["automation"])

# Automation Rules endpoints
@router.get("/rules", response_model=List[AutomationRule])
def get_automation_rules(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get all automation rules."""
    return crud.get_automation_rules(db, skip=skip, limit=limit)

@router.post("/rules", response_model=AutomationRule, status_code=status.HTTP_201_CREATED)
def create_automation_rule(
    rule: AutomationRuleCreate, db: Session = Depends(get_db)
):
    """Create a new automation rule."""
    return crud.create_automation_rule(db, rule)

@router.get("/rules/{rule_id}", response_model=AutomationRule)
def get_automation_rule(rule_id: int, db: Session = Depends(get_db)):
    """Get a specific automation rule by ID."""
    db_rule = crud.get_automation_rule(db, rule_id)
    if not db_rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Automation rule not found"
        )
    return db_rule

@router.patch("/rules/{rule_id}", response_model=AutomationRule)
def update_automation_rule(
    rule_id: int, rule: AutomationRuleUpdate, db: Session = Depends(get_db)
):
    """Update a specific automation rule."""
    db_rule = crud.update_automation_rule(db, rule_id, rule)
    if not db_rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Automation rule not found"
        )
    return db_rule

@router.delete("/rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_automation_rule(rule_id: int, db: Session = Depends(get_db)):
    """Delete a specific automation rule."""
    success = crud.delete_automation_rule(db, rule_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Automation rule not found"
        )

# Email Templates endpoints
@router.get("/templates", response_model=List[EmailTemplate])
def get_email_templates(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Get all email templates."""
    return crud.get_email_templates(db, skip=skip, limit=limit)

@router.post("/templates", response_model=EmailTemplate, status_code=status.HTTP_201_CREATED)
def create_email_template(
    template: EmailTemplateCreate, db: Session = Depends(get_db)
):
    """Create a new email template."""
    return crud.create_email_template(db, template)

@router.get("/templates/{template_id}", response_model=EmailTemplate)
def get_email_template(template_id: int, db: Session = Depends(get_db)):
    """Get a specific email template by ID."""
    db_template = crud.get_email_template(db, template_id)
    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email template not found"
        )
    return db_template

@router.patch("/templates/{template_id}", response_model=EmailTemplate)
def update_email_template(
    template_id: int, template: EmailTemplateUpdate, db: Session = Depends(get_db)
):
    """Update a specific email template."""
    db_template = crud.update_email_template(db, template_id, template)
    if not db_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email template not found"
        )
    return db_template

@router.delete("/templates/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_email_template(template_id: int, db: Session = Depends(get_db)):
    """Delete a specific email template."""
    success = crud.delete_email_template(db, template_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email template not found"
        )

# Campaign Automation endpoints
@router.get("/campaigns/{campaign_id}/automations", response_model=List[CampaignAutomation])
def get_campaign_automations(campaign_id: int, db: Session = Depends(get_db)):
    """Get all automations for a specific campaign."""
    return crud.get_campaign_automations(db, campaign_id)

@router.post("/campaigns/{campaign_id}/automations", response_model=CampaignAutomation, status_code=status.HTTP_201_CREATED)
def create_campaign_automation(
    campaign_id: int, automation: CampaignAutomationCreate, db: Session = Depends(get_db)
):
    """Create a new automation for a specific campaign."""
    return crud.create_campaign_automation(db, campaign_id, automation)

@router.patch("/campaigns/{campaign_id}/automations/{automation_id}/status", response_model=CampaignAutomation)
def update_campaign_automation_status(
    campaign_id: int, automation_id: int, is_active: bool, db: Session = Depends(get_db)
):
    """Update the status of a specific campaign automation."""
    db_automation = crud.update_campaign_automation_status(
        db, campaign_id, automation_id, is_active
    )
    if not db_automation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign automation not found"
        )
    return db_automation

@router.delete("/campaigns/{campaign_id}/automations/{automation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign_automation(
    campaign_id: int, automation_id: int, db: Session = Depends(get_db)
):
    """Delete a specific campaign automation."""
    success = crud.delete_campaign_automation(db, campaign_id, automation_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign automation not found"
        ) 