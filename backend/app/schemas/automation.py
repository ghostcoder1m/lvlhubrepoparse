from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class TriggerType(str, Enum):
    lead_created = "lead_created"
    lead_updated = "lead_updated"
    score_changed = "score_changed"
    event_occurred = "event_occurred"

class ActionType(str, Enum):
    send_email = "send_email"
    update_lead = "update_lead"
    add_to_campaign = "add_to_campaign"
    notify_team = "notify_team"

class Operator(str, Enum):
    equals = "equals"
    contains = "contains"
    greater_than = "greater_than"
    less_than = "less_than"

class Condition(BaseModel):
    field: str
    operator: Operator
    value: Any

class Action(BaseModel):
    type: ActionType
    params: Dict[str, Any]

class AutomationRuleBase(BaseModel):
    name: str
    trigger_type: TriggerType
    conditions: List[Condition]
    actions: List[Action]
    is_active: bool = True

class AutomationRuleCreate(AutomationRuleBase):
    pass

class AutomationRuleUpdate(BaseModel):
    name: Optional[str] = None
    trigger_type: Optional[TriggerType] = None
    conditions: Optional[List[Condition]] = None
    actions: Optional[List[Action]] = None
    is_active: Optional[bool] = None

class AutomationRule(AutomationRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EmailTemplateBase(BaseModel):
    name: str
    subject: str
    content: str
    variables: List[str]

class EmailTemplateCreate(EmailTemplateBase):
    pass

class EmailTemplateUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    variables: Optional[List[str]] = None

class EmailTemplate(EmailTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AutomationSchedule(BaseModel):
    start_date: datetime
    frequency: str = Field(..., pattern="^(once|daily|weekly)$")
    end_date: Optional[datetime] = None

class CampaignAutomationCreate(BaseModel):
    template_id: int
    schedule: AutomationSchedule

class CampaignAutomation(CampaignAutomationCreate):
    id: int
    campaign_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 