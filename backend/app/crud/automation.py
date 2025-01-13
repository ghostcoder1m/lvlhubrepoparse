from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

from app.models.automation import AutomationRule, EmailTemplate, CampaignAutomation
from app.schemas.automation import (
    AutomationRuleCreate,
    AutomationRuleUpdate,
    EmailTemplateCreate,
    EmailTemplateUpdate,
    CampaignAutomationCreate,
)

# Automation Rules CRUD
def get_automation_rule(db: Session, rule_id: int) -> Optional[AutomationRule]:
    return db.query(AutomationRule).filter(AutomationRule.id == rule_id).first()

def get_automation_rules(
    db: Session, skip: int = 0, limit: int = 100
) -> List[AutomationRule]:
    return (
        db.query(AutomationRule)
        .order_by(desc(AutomationRule.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_automation_rule(
    db: Session, rule: AutomationRuleCreate
) -> AutomationRule:
    db_rule = AutomationRule(
        **rule.model_dump(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

def update_automation_rule(
    db: Session, rule_id: int, rule: AutomationRuleUpdate
) -> Optional[AutomationRule]:
    db_rule = get_automation_rule(db, rule_id)
    if not db_rule:
        return None
    
    update_data = rule.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(db_rule, field, value)
    
    db.commit()
    db.refresh(db_rule)
    return db_rule

def delete_automation_rule(db: Session, rule_id: int) -> bool:
    db_rule = get_automation_rule(db, rule_id)
    if not db_rule:
        return False
    
    db.delete(db_rule)
    db.commit()
    return True

# Email Templates CRUD
def get_email_template(db: Session, template_id: int) -> Optional[EmailTemplate]:
    return db.query(EmailTemplate).filter(EmailTemplate.id == template_id).first()

def get_email_templates(
    db: Session, skip: int = 0, limit: int = 100
) -> List[EmailTemplate]:
    return (
        db.query(EmailTemplate)
        .order_by(desc(EmailTemplate.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_email_template(
    db: Session, template: EmailTemplateCreate
) -> EmailTemplate:
    db_template = EmailTemplate(
        **template.model_dump(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

def update_email_template(
    db: Session, template_id: int, template: EmailTemplateUpdate
) -> Optional[EmailTemplate]:
    db_template = get_email_template(db, template_id)
    if not db_template:
        return None
    
    update_data = template.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(db_template, field, value)
    
    db.commit()
    db.refresh(db_template)
    return db_template

def delete_email_template(db: Session, template_id: int) -> bool:
    db_template = get_email_template(db, template_id)
    if not db_template:
        return False
    
    db.delete(db_template)
    db.commit()
    return True

# Campaign Automation CRUD
def get_campaign_automation(
    db: Session, campaign_id: int, automation_id: int
) -> Optional[CampaignAutomation]:
    return (
        db.query(CampaignAutomation)
        .filter(
            CampaignAutomation.campaign_id == campaign_id,
            CampaignAutomation.id == automation_id,
        )
        .first()
    )

def get_campaign_automations(
    db: Session, campaign_id: int
) -> List[CampaignAutomation]:
    return (
        db.query(CampaignAutomation)
        .filter(CampaignAutomation.campaign_id == campaign_id)
        .order_by(desc(CampaignAutomation.created_at))
        .all()
    )

def create_campaign_automation(
    db: Session, campaign_id: int, automation: CampaignAutomationCreate
) -> CampaignAutomation:
    db_automation = CampaignAutomation(
        **automation.model_dump(),
        campaign_id=campaign_id,
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_automation)
    db.commit()
    db.refresh(db_automation)
    return db_automation

def update_campaign_automation_status(
    db: Session, campaign_id: int, automation_id: int, is_active: bool
) -> Optional[CampaignAutomation]:
    db_automation = get_campaign_automation(db, campaign_id, automation_id)
    if not db_automation:
        return None
    
    db_automation.is_active = is_active
    db_automation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(db_automation)
    return db_automation

def delete_campaign_automation(
    db: Session, campaign_id: int, automation_id: int
) -> bool:
    db_automation = get_campaign_automation(db, campaign_id, automation_id)
    if not db_automation:
        return False
    
    db.delete(db_automation)
    db.commit()
    return True 