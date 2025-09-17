# app/helpers/ai_helpers.py
import logging
from datetime import datetime
from typing import List, Dict, Any
import asyncio
from app.core.config import settings
from app.services.content_creation import ContentCreator
from app.services.social_media import SocialMediaManager
from app.services.email_marketing import EmailMarketer
from app.ml.model_trainer import ModelTrainer

logger = logging.getLogger(__name__)

class AIHelper:
    def __init__(self, name: str, role: str, version: str = "1.0.0"):
        self.name = name
        self.role = role
        self.version = version
        self.last_active = None
        self.task_count = 0
        self.is_active = True
        
        # Initialize specialized helpers based on role
        if role == "content_creator":
            self.specialized_helper = ContentCreator()
        elif role == "social_media_manager":
            self.specialized_helper = SocialMediaManager()
        elif role == "email_marketer":
            self.specialized_helper = EmailMarketer()
        elif role == "model_trainer":
            self.specialized_helper = ModelTrainer()
    
    async def perform_task(self, task_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Perform a task based on the AI helper's role"""
        self.last_active = datetime.utcnow()
        self.task_count += 1
        
        try:
            if self.role == "content_creator":
                result = await self.specialized_helper.create_content(task_data)
            elif self.role == "social_media_manager":
                result = await self.specialized_handler.post_content(task_data)
            elif self.role == "email_marketer":
                result = await self.specialized_helper.send_campaign(task_data)
            elif self.role == "model_trainer":
                result = await self.specialized_helper.train_model(task_data)
            else:
                result = {"status": "error", "message": f"Unknown role: {self.role}"}
            
            logger.info(f"{self.name} completed task: {result.get('task', 'unknown')}")
            return result
            
        except Exception as e:
            logger.error(f"Error in AI helper {self.name}: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the AI helper"""
        return {
            "name": self.name,
            "role": self.role,
            "version": self.version,
            "last_active": self.last_active.isoformat() if self.last_active else None,
            "task_count": self.task_count,
            "is_active": self.is_active
        }

def create_ai_team() -> List[AIHelper]:
    """Create a team of AI helpers"""
    return [
        AIHelper("ContentBot", "content_creator"),
        AIHelper("SocialBot", "social_media_manager"),
        AIHelper("MailBot", "email_marketer"),
        AIHelper("ModelBot", "model_trainer"),
        AIHelper("DataBot", "data_analyst"),
        AIHelper("PriceBot", "cost_predictor"),
        AIHelper("InventoryBot", "inventory_manager"),
        AIHelper("SecurityBot", "security_guardian")
    ]

async def run_ai_tasks(team: List[AIHelper]):
    """Run tasks for all AI helpers continuously"""
    while True:
        for ai in team:
            if ai.is_active:
                try:
                    # Determine task based on role
                    task_data = {}
                    if ai.role == "content_creator":
                        task_data = {"content_type": "blog_post", "topic": "food cost management"}
                    elif ai.role == "social_media_manager":
                        task_data = {"platform": "linkedin", "content": "Latest insights on restaurant cost savings"}
                    elif ai.role == "email_marketer":
                        task_data = {"audience": "hotels", "template": "welcome"}
                    
                    # Perform task
                    await ai.perform_task(task_data)
                    
                except Exception as e:
                    logger.error(f"Error running task for {ai.name}: {str(e)}")
        
        # Wait before next iteration
        await asyncio.sleep(300)  # 5 minutes
