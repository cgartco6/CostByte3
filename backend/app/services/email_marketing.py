# app/services/email_marketing.py
import logging
from typing import Dict, Any, List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
from app.helpers.email_service import EmailService

logger = logging.getLogger(__name__)

class EmailMarketer:
    def __init__(self):
        self.email_service = EmailService(
            smtp_server=settings.SMTP_SERVER,
            smtp_port=settings.SMTP_PORT,
            username=settings.SMTP_USERNAME,
            password=settings.SMTP_PASSWORD
        )
    
    async def send_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send email marketing campaign"""
        try:
            audience = campaign_data.get("audience", "all")
            template_name = campaign_data.get("template", "general")
            
            # Get recipients based on audience
            recipients = self._get_recipients(audience)
            
            # Get email content
            subject, html_content, text_content = self._get_email_content(template_name, audience)
            
            # Send emails
            results = []
            for recipient in recipients:
                result = self.email_service.send_email(
                    to_email=recipient["email"],
                    subject=subject,
                    html_content=html_content,
                    text_content=text_content
                )
                results.append({
                    "recipient": recipient["email"],
                    "status": "success" if result else "failed"
                })
            
            success_count = sum(1 for r in results if r["status"] == "success")
            
            return {
                "status": "success",
                "campaign": template_name,
                "audience": audience,
                "sent_count": success_count,
                "total_count": len(recipients),
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error sending email campaign: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _get_recipients(self, audience: str) -> List[Dict[str, str]]:
        """Get recipients based on audience type"""
        # This would typically query a database
        # For now, return sample data
        
        audiences = {
            "hotels": [
                {"email": "hotel1@example.com", "name": "Hotel Manager 1"},
                {"email": "hotel2@example.com", "name": "Hotel Manager 2"}
            ],
            "restaurants": [
                {"email": "restaurant1@example.com", "name": "Restaurant Owner 1"},
                {"email": "restaurant2@example.com", "name": "Restaurant Owner 2"}
            ],
            "catering": [
                {"email": "catering1@example.com", "name": "Catering Manager 1"},
                {"email": "catering2@example.com", "name": "Catering Manager 2"}
            ],
            "all": [
                {"email": "hotel1@example.com", "name": "Hotel Manager 1"},
                {"email": "restaurant1@example.com", "name": "Restaurant Owner 1"},
                {"email": "catering1@example.com", "name": "Catering Manager 1"}
            ]
        }
        
        return audiences.get(audience, [])
    
    def _get_email_content(self, template_name: str, audience: str) -> tuple:
        """Get email content based on template and audience"""
        templates = {
            "welcome": {
                "subject": f"Welcome to CostByte - Revolutionizing {audience.capitalize()} Food Cost Management",
                "html": f"""
                <h1>Welcome to CostByte!</h1>
                <p>Dear {audience} owner,</p>
                <p>We're excited to help you reduce food costs and improve efficiency.</p>
                <p>Our AI-powered platform can help you save up to 15% on food costs.</p>
                <a href="https://costbyte.co.za">Learn more</a>
                """
            },
            "promotion": {
                "subject": f"Special Offer for {audience.capitalize()} Businesses - Save 20% on CostByte",
                "html": f"""
                <h1>Special Limited Time Offer!</h1>
                <p>Dear {audience} owner,</p>
                <p>For a limited time, save 20% on CostByte subscription.</p>
                <p>Use code: SAVE20 at checkout.</p>
                <a href="https://costbyte.co.za/pricing">Get Started</a>
                """
            },
            "general": {
                "subject": "Improve Your Food Cost Management with CostByte",
                "html": """
                <h1>Transform Your Kitchen Operations</h1>
                <p>CostByte helps you reduce waste, track costs, and improve efficiency.</p>
                <a href="https://costbyte.co.za">Learn how</a>
                """
            }
        }
        
        template = templates.get(template_name, templates["general"])
        text_content = template["html"].replace("<h1>", "").replace("</h1>", "").replace("<p>", "").replace("</p>", "").replace("<a>", "").replace("</a>", "")
        
        return template["subject"], template["html"], text_content
