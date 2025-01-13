import logging
from typing import Dict, Any, List
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.automation import AutomationRule, EmailTemplate
from app.models.lead import Lead
from app.models.campaign import Campaign
from app.schemas.automation import TriggerType, ActionType, Operator
from app.services.email import send_email

logger = logging.getLogger(__name__)

def evaluate_condition(condition: Dict[str, Any], lead_data: Dict[str, Any]) -> bool:
    """Evaluate a single condition against lead data."""
    field = condition["field"]
    operator = condition["operator"]
    value = condition["value"]
    
    if field not in lead_data:
        return False
    
    lead_value = lead_data[field]
    
    if operator == Operator.equals:
        return lead_value == value
    elif operator == Operator.contains:
        return value in str(lead_value)
    elif operator == Operator.greater_than:
        return float(lead_value) > float(value)
    elif operator == Operator.less_than:
        return float(lead_value) < float(value)
    
    return False

def evaluate_conditions(conditions: List[Dict[str, Any]], lead_data: Dict[str, Any]) -> bool:
    """Evaluate all conditions for a rule. All conditions must be met (AND logic)."""
    return all(evaluate_condition(condition, lead_data) for condition in conditions)

def execute_action(
    db: Session,
    action: Dict[str, Any],
    lead: Lead,
    lead_data: Dict[str, Any]
) -> bool:
    """Execute a single action based on its type."""
    try:
        action_type = action["type"]
        params = action["params"]
        
        if action_type == ActionType.send_email:
            template_id = params.get("template_id")
            if not template_id:
                logger.error("No template_id provided for send_email action")
                return False
            
            template = db.query(EmailTemplate).filter(
                EmailTemplate.id == template_id
            ).first()
            if not template:
                logger.error(f"Email template {template_id} not found")
                return False
            
            # Replace variables in subject and content
            subject = template.subject
            content = template.content
            for var in template.variables:
                value = lead_data.get(var, "")
                subject = subject.replace(f"{{{var}}}", str(value))
                content = content.replace(f"{{{var}}}", str(value))
            
            send_email(lead.email, subject, content)
            
        elif action_type == ActionType.update_lead:
            update_fields = params.get("fields", {})
            for field, value in update_fields.items():
                if hasattr(lead, field):
                    setattr(lead, field, value)
            db.commit()
            
        elif action_type == ActionType.add_to_campaign:
            campaign_id = params.get("campaign_id")
            if not campaign_id:
                logger.error("No campaign_id provided for add_to_campaign action")
                return False
            
            campaign = db.query(Campaign).filter(
                Campaign.id == campaign_id
            ).first()
            if not campaign:
                logger.error(f"Campaign {campaign_id} not found")
                return False
            
            if lead not in campaign.leads:
                campaign.leads.append(lead)
                db.commit()
            
        elif action_type == ActionType.notify_team:
            # Implement team notification logic here
            # This could involve sending Slack messages, emails, or other notifications
            pass
        
        return True
        
    except Exception as e:
        logger.error(f"Error executing action: {str(e)}")
        return False

def execute_automation_rules(
    db: Session,
    trigger_type: TriggerType,
    lead: Lead,
    lead_data: Dict[str, Any]
) -> None:
    """Execute all active automation rules for a given trigger type."""
    try:
        # Get all active rules for the trigger type
        rules = db.query(AutomationRule).filter(
            AutomationRule.trigger_type == trigger_type,
            AutomationRule.is_active == True
        ).all()
        
        for rule in rules:
            try:
                # Evaluate conditions
                if evaluate_conditions(rule.conditions, lead_data):
                    # Execute actions
                    for action in rule.actions:
                        success = execute_action(db, action, lead, lead_data)
                        if not success:
                            logger.error(
                                f"Failed to execute action for rule {rule.id}"
                            )
            except Exception as e:
                logger.error(
                    f"Error processing rule {rule.id}: {str(e)}"
                )
                continue
                
    except Exception as e:
        logger.error(f"Error executing automation rules: {str(e)}")

def process_lead_created(db: Session, lead: Lead) -> None:
    """Process automation rules when a lead is created."""
    lead_data = {
        "id": lead.id,
        "first_name": lead.first_name,
        "last_name": lead.last_name,
        "email": lead.email,
        "phone": lead.phone,
        "company": lead.company,
        "job_title": lead.job_title,
        "lead_score": lead.lead_score,
        "created_at": lead.created_at.isoformat(),
    }
    execute_automation_rules(db, TriggerType.lead_created, lead, lead_data)

def process_lead_updated(db: Session, lead: Lead, updated_fields: List[str]) -> None:
    """Process automation rules when a lead is updated."""
    lead_data = {
        "id": lead.id,
        "first_name": lead.first_name,
        "last_name": lead.last_name,
        "email": lead.email,
        "phone": lead.phone,
        "company": lead.company,
        "job_title": lead.job_title,
        "lead_score": lead.lead_score,
        "updated_at": lead.updated_at.isoformat(),
        "updated_fields": updated_fields,
    }
    execute_automation_rules(db, TriggerType.lead_updated, lead, lead_data)

def process_score_changed(db: Session, lead: Lead, old_score: int) -> None:
    """Process automation rules when a lead's score changes."""
    lead_data = {
        "id": lead.id,
        "first_name": lead.first_name,
        "last_name": lead.last_name,
        "email": lead.email,
        "phone": lead.phone,
        "company": lead.company,
        "job_title": lead.job_title,
        "lead_score": lead.lead_score,
        "old_score": old_score,
        "score_change": lead.lead_score - old_score,
    }
    execute_automation_rules(db, TriggerType.score_changed, lead, lead_data)

def process_event_occurred(
    db: Session, lead: Lead, event_type: str, event_data: Dict[str, Any]
) -> None:
    """Process automation rules when an event occurs."""
    lead_data = {
        "id": lead.id,
        "first_name": lead.first_name,
        "last_name": lead.last_name,
        "email": lead.email,
        "phone": lead.phone,
        "company": lead.company,
        "job_title": lead.job_title,
        "lead_score": lead.lead_score,
        "event_type": event_type,
        "event_data": event_data,
        "event_time": datetime.utcnow().isoformat(),
    }
    execute_automation_rules(db, TriggerType.event_occurred, lead, lead_data) 