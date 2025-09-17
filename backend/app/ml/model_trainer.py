# app/ml/model_trainer.py
import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import os
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self):
        self.models_dir = "app/ml/models"
        os.makedirs(self.models_dir, exist_ok=True)
    
    async def train_model(self, model_data: Dict[str, Any]) -> Dict[str, Any]:
        """Train a machine learning model"""
        try:
            model_type = model_data.get("model_type", "price_prediction")
            
            if model_type == "price_prediction":
                result = await self._train_price_prediction_model()
            elif model_type == "waste_prediction":
                result = await self._train_waste_prediction_model()
            else:
                result = {"status": "error", "message": f"Unknown model type: {model_type}"}
            
            return result
            
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _train_price_prediction_model(self) -> Dict[str, Any]:
        """Train price prediction model"""
        try:
            # Load or generate sample data
            X, y = self._generate_price_data()
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            
            # Save model
            model_path = os.path.join(self.models_dir, "price_model.pkl")
            joblib.dump(model, model_path)
            
            return {
                "status": "success",
                "model_type": "price_prediction",
                "metrics": {
                    "mae": mae,
                    "mse": mse,
                    "rmse": np.sqrt(mse)
                },
                "model_path": model_path,
                "trained_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error training price prediction model: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    async def _train_waste_prediction_model(self) -> Dict[str, Any]:
        """Train waste prediction model"""
        try:
            # Load or generate sample data
            X, y = self._generate_waste_data()
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            
            # Save model
            model_path = os.path.join(self.models_dir, "waste_model.pkl")
            joblib.dump(model, model_path)
            
            return {
                "status": "success",
                "model_type": "waste_prediction",
                "metrics": {
                    "mae": mae,
                    "mse": mse,
                    "rmse": np.sqrt(mse)
                },
                "model_path": model_path,
                "trained_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error training waste prediction model: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _generate_price_data(self):
        """Generate sample price data"""
        np.random.seed(42)
        n_samples = 1000
        
        # Features: season, supplier_rating, demand, previous_price
        X = np.random.rand(n_samples, 4)
        
        # Target: price change percentage
        y = 0.5 * X[:, 0] + 0.3 * X[:, 1] + 0.2 * X[:, 2] - 0.1 * X[:, 3] + np.random.normal(0, 0.1, n_samples)
        
        return X, y
    
    def _generate_waste_data(self):
        """Generate sample waste data"""
        np.random.seed(42)
        n_samples = 1000
        
        # Features: inventory_level, shelf_life, demand_prediction, season
        X = np.random.rand(n_samples, 4)
        
        # Target: waste percentage
        y = 0.6 * X[:, 0] + 0.2 * X[:, 1] - 0.4 * X[:, 2] + 0.1 * X[:, 3] + np.random.normal(0, 0.1, n_samples)
        
        return X, y
    
    def predict_price_change(self, features: List[float]) -> float:
        """Predict price change using trained model"""
        try:
            model_path = os.path.join(self.models_dir, "price_model.pkl")
            if os.path.exists(model_path):
                model = joblib.load(model_path)
                prediction = model.predict([features])[0]
                return prediction
            else:
                logger.warning("Price prediction model not found")
                return 0.0
        except Exception as e:
            logger.error(f"Error predicting price change: {str(e)}")
            return 0.0
    
    def predict_waste(self, features: List[float]) -> float:
        """Predict waste using trained model"""
        try:
            model_path = os.path.join(self.models_dir, "waste_model.pkl")
            if os.path.exists(model_path):
                model = joblib.load(model_path)
                prediction = model.predict([features])[0]
                return prediction
            else:
                logger.warning("Waste prediction model not found")
                return 0.0
        except Exception as e:
            logger.error(f"Error predicting waste: {str(e)}")
            return 0.0
