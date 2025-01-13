import logging
from datetime import datetime, timedelta
import asyncio
from sqlalchemy.orm import Session
from typing import Dict, Any

from app.database import SessionLocal
from app.models.automation import CampaignAutomation, EmailTemplate
from app.models.campaign import Campaign
from app.services.email import send_email

logger = logging.getLogger(__name__)

async def process_campaign_automation(automation: CampaignAutomation, db: Session) -> None:
    """Process a single campaign automation."""
    try:
        # Get the campaign and template
        campaign = db.query(Campaign).filter(
            Campaign.id == automation.campaign_id
        ).first()
        template = db.query(EmailTemplate).filter(
            EmailTemplate.id == automation.template_id
        ).first()
        
        if not campaign or not template:
            logger.error(
                f"Campaign {automation.campaign_id} or template "
                f"{automation.template_id} not found"
            )
            return
        
        # Send emails to all leads in the campaign
        for lead in campaign.leads:
            # Prepare email variables
            variables = {
                "first_name": lead.first_name,
                "last_name": lead.last_name,
                "company": lead.company,
                "campaign_name": campaign.name,
            }
            
            # Replace variables in subject and content
            subject = template.subject
            content = template.content
            for var_name, var_value in variables.items():
                if var_value:
                    subject = subject.replace(f"{{{var_name}}}", str(var_value))
                    content = content.replace(f"{{{var_name}}}", str(var_value))
            
            # Send the email
            success = send_email(lead.email, subject, content)
            if not success:
                logger.error(f"Failed to send email to {lead.email}")
        
        # Update automation timestamp
        automation.updated_at = datetime.utcnow()
        db.commit()
        
    except Exception as e:
        logger.error(f"Error processing automation {automation.id}: {str(e)}")

async def check_campaign_automations() -> None:
    """Check and process campaign automations."""
    try:
        db = SessionLocal()
        
        # Get all active automations
        automations = db.query(CampaignAutomation).filter(
            CampaignAutomation.is_active == True
        ).all()
        
        for automation in automations:
            # Check if it's time to process this automation
            now = datetime.utcnow()
            
            # Skip if start date is in the future
            if automation.schedule.start_date > now:
                continue
                
            # Skip if end date is in the past
            if automation.schedule.end_date and automation.schedule.end_date < now:
                continue
            
            # Check frequency
            last_run = automation.updated_at or automation.created_at
            frequency = automation.schedule.frequency
            
            should_run = False
            
            if frequency == "once" and not automation.updated_at:
                # Run once if never updated
                should_run = True
            elif frequency == "daily":
                # Run if last run was more than 24 hours ago
                should_run = (now - last_run) > timedelta(days=1)
            elif frequency == "weekly":
                # Run if last run was more than 7 days ago
                should_run = (now - last_run) > timedelta(days=7)
            
            if should_run:
                await process_campaign_automation(automation, db)
        
    except Exception as e:
        logger.error(f"Error checking campaign automations: {str(e)}")
    finally:
        db.close()

async def run_automation_worker() -> None:
    """Run the automation worker continuously."""
    while True:
        try:
            await check_campaign_automations()
        except Exception as e:
            logger.error(f"Error in automation worker: {str(e)}")
        
        # Wait for 5 minutes before next check
        await asyncio.sleep(300)

def start_automation_worker() -> None:
    """Start the automation worker in the background."""
    loop = asyncio.get_event_loop()
    loop.create_task(run_automation_worker()) 