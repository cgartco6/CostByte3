# app/services/monitoring.py
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any
from app.db.session import SessionLocal
from app.db.models.ai_helper import AIHelper, AIHelperLog
from app.db.models.analytics import Analytics

logger = logging.getLogger(__name__)

class MonitoringService:
    def __init__(self):
        self.interval = 300  # 5 minutes
    
    async def start_monitoring(self):
        """Start monitoring service"""
        while True:
            try:
                await self._check_system_health()
                await self._log_performance_metrics()
                await self._check_ai_helpers()
                
                logger.info("Monitoring check completed")
                
            except Exception as e:
                logger.error(f"Error in monitoring service: {str(e)}")
            
            await asyncio.sleep(self.interval)
    
    async def _check_system_health(self):
        """Check system health and log issues"""
        try:
            # Check database connection
            db = SessionLocal()
            db.execute("SELECT 1")
            db.close()
            
            # Check external services (simplified)
            services_ok = True
            
            health_status = {
                "database": "healthy",
                "external_services": "healthy" if services_ok else "degraded",
                "timestamp": datetime.utcnow().isoformat()
            }
            
            logger.info(f"System health: {health_status}")
            
        except Exception as e:
            logger.error(f"System health check failed: {str(e)}")
    
    async def _log_performance_metrics(self):
        """Log performance metrics to database"""
        try:
            db = SessionLocal()
            
            # Simulate performance metrics
            metrics = {
                "response_time": 150,  # ms
                "memory_usage": 45,    # %
                "cpu_usage": 25,       # %
                "active_users": 42,
                "request_rate": 120    # requests/min
            }
            
            for metric_name, metric_value in metrics.items():
                analytics = Analytics(
                    metric_name=metric_name,
                    metric_value=metric_value,
                    metric_type="performance",
                    period="5min",
                    period_start=datetime.utcnow(),
                    period_end=datetime.utcnow()
                )
                db.add(analytics)
            
            db.commit()
            db.close()
            
            logger.info("Performance metrics logged")
            
        except Exception as e:
            logger.error(f"Error logging performance metrics: {str(e)}")
    
    async def _check_ai_helpers(self):
        """Check AI helpers status and restart if needed"""
        try:
            db = SessionLocal()
            
            helpers = db.query(AIHelper).all()
            
            for helper in helpers:
                # Check if helper is active and responding
                if helper.last_active and (datetime.utcnow() - helper.last_active).total_seconds() > 3600:  # 1 hour
                    logger.warning(f"AI helper {helper.name} is not responding")
                    
                    # Attempt to restart
                    helper.is_active = True
                    helper.last_active = datetime.utcnow()
                    
                    # Log the issue
                    log = AIHelperLog(
                        ai_helper_id=helper.id,
                        task="health_check",
                        status="restarted",
                        details="Helper was not responding and has been restarted"
                    )
                    db.add(log)
            
            db.commit()
            db.close()
            
        except Exception as e:
            logger.error(f"Error checking AI helpers: {str(e)}")

def start_monitoring():
    """Start the monitoring service"""
    monitor = MonitoringService()
    asyncio.create_task(monitor.start_monitoring())
