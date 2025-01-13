import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

logger = logging.getLogger(__name__)

# Email configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

def send_email(
    to_email: str,
    subject: str,
    content: str,
    html_content: Optional[str] = None
) -> bool:
    """
    Send an email using SMTP.
    
    Args:
        to_email: Recipient's email address
        subject: Email subject
        content: Plain text content
        html_content: Optional HTML content
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        if not all([SMTP_USERNAME, SMTP_PASSWORD, SENDER_EMAIL]):
            logger.error("Email configuration is incomplete")
            return False
            
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        
        # Add plain text content
        msg.attach(MIMEText(content, "plain"))
        
        # Add HTML content if provided
        if html_content:
            msg.attach(MIMEText(html_content, "html"))
            
        # Connect to SMTP server
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

def send_welcome_email(to_email: str, first_name: str) -> bool:
    """Send a welcome email to a new lead."""
    subject = "Welcome to Our Platform!"
    content = f"""
    Hi {first_name},
    
    Thank you for your interest in our platform. We're excited to have you on board!
    
    Our team will be in touch with you shortly to discuss how we can help you achieve your goals.
    
    Best regards,
    The Team
    """
    
    html_content = f"""
    <html>
        <body>
            <h2>Welcome to Our Platform!</h2>
            <p>Hi {first_name},</p>
            <p>Thank you for your interest in our platform. We're excited to have you on board!</p>
            <p>Our team will be in touch with you shortly to discuss how we can help you achieve your goals.</p>
            <br>
            <p>Best regards,<br>The Team</p>
        </body>
    </html>
    """
    
    return send_email(to_email, subject, content, html_content)

def send_lead_score_notification(
    to_email: str,
    first_name: str,
    lead_score: int,
    old_score: int
) -> bool:
    """Send a notification when a lead's score changes significantly."""
    score_change = lead_score - old_score
    change_type = "increased" if score_change > 0 else "decreased"
    
    subject = f"Lead Score Update: {change_type.title()} by {abs(score_change)} points"
    content = f"""
    Hi {first_name},
    
    Your lead score has {change_type} from {old_score} to {lead_score}.
    
    This change reflects your recent interactions with our platform.
    
    Best regards,
    The Team
    """
    
    html_content = f"""
    <html>
        <body>
            <h2>Lead Score Update</h2>
            <p>Hi {first_name},</p>
            <p>Your lead score has {change_type} from {old_score} to {lead_score}.</p>
            <p>This change reflects your recent interactions with our platform.</p>
            <br>
            <p>Best regards,<br>The Team</p>
        </body>
    </html>
    """
    
    return send_email(to_email, subject, content, html_content)

def send_campaign_invitation(
    to_email: str,
    first_name: str,
    campaign_name: str,
    campaign_description: str
) -> bool:
    """Send an invitation to join a campaign."""
    subject = f"Join Our Campaign: {campaign_name}"
    content = f"""
    Hi {first_name},
    
    We think you might be interested in our campaign: {campaign_name}
    
    {campaign_description}
    
    Let us know if you'd like to learn more!
    
    Best regards,
    The Team
    """
    
    html_content = f"""
    <html>
        <body>
            <h2>Join Our Campaign</h2>
            <p>Hi {first_name},</p>
            <p>We think you might be interested in our campaign: <strong>{campaign_name}</strong></p>
            <p>{campaign_description}</p>
            <p>Let us know if you'd like to learn more!</p>
            <br>
            <p>Best regards,<br>The Team</p>
        </body>
    </html>
    """
    
    return send_email(to_email, subject, content, html_content) 