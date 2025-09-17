# app/services/content_creation.py
import logging
from typing import Dict, Any, List
import openai
from app.core.config import settings

logger = logging.getLogger(__name__)

class ContentCreator:
    def __init__(self):
        self.openai_api_key = settings.OPENAI_API_KEY
        openai.api_key = self.openai_api_key
    
    async def create_content(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create content using AI"""
        try:
            content_type = content_data.get("content_type", "blog_post")
            topic = content_data.get("topic", "food cost management")
            
            prompt = self._get_prompt_for_content_type(content_type, topic)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a content creator specializing in food cost management for restaurants and hotels."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            
            # Save content to database or file system
            result = {
                "status": "success",
                "content_type": content_type,
                "topic": topic,
                "content": content,
                "word_count": len(content.split())
            }
            
            logger.info(f"Created {content_type} about {topic}")
            return result
            
        except Exception as e:
            logger.error(f"Error creating content: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _get_prompt_for_content_type(self, content_type: str, topic: str) -> str:
        """Get appropriate prompt for different content types"""
        prompts = {
            "blog_post": f"Write a comprehensive blog post about {topic} for restaurant and hotel owners. Include practical tips and strategies.",
            "social_media": f"Create engaging social media content about {topic} for the hospitality industry. Make it catchy and informative.",
            "email_newsletter": f"Write an email newsletter about {topic} for restaurant and hotel managers. Focus on actionable insights.",
            "ad_copy": f"Create compelling ad copy for {topic} targeting hospitality businesses. Highlight benefits and ROI."
        }
        
        return prompts.get(content_type, f"Write about {topic} for the hospitality industry.")
    
    async def generate_content_ideas(self, category: str = "food cost") -> List[str]:
        """Generate content ideas using AI"""
        try:
            prompt = f"Generate 10 content ideas about {category} for restaurant and hotel businesses."
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a content strategist for the hospitality industry."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            ideas = response.choices[0].message.content.strip().split('\n')
            ideas = [idea for idea in ideas if idea.strip()]
            
            return ideas[:10]  # Return first 10 ideas
            
        except Exception as e:
            logger.error(f"Error generating content ideas: {str(e)}")
            return []
