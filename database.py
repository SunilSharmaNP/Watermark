"""
User data and settings management
Handles storage and retrieval of user settings
"""

import json
import os
from typing import Dict, Optional, Tuple
from config import SETTINGS_PATH, LOGOS_PATH
import logging

logger = logging.getLogger(__name__)


class UserDatabase:
    """Manages user settings and data"""
    
    @staticmethod
    def _get_user_file(user_id: int) -> str:
        """Get user settings file path"""
        return os.path.join(SETTINGS_PATH, f"{user_id}.json")
    
    @staticmethod
    def _get_logo_path(user_id: int) -> str:
        """Get user logo file path"""
        return os.path.join(LOGOS_PATH, f"{user_id}.png")
    
    @staticmethod
    def _load_user_data(user_id: int) -> Dict:
        """Load user settings from file"""
        file_path = UserDatabase._get_user_file(user_id)
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading user data for {user_id}: {e}")
                return UserDatabase._create_default_settings()
        
        return UserDatabase._create_default_settings()
    
    @staticmethod
    def _create_default_settings() -> Dict:
        """Create default user settings"""
        return {
            "position": "bottom_right",
            "scale": 20,
            "has_logo": False
        }
    
    @staticmethod
    def _save_user_data(user_id: int, data: Dict) -> bool:
        """Save user settings to file"""
        try:
            file_path = UserDatabase._get_user_file(user_id)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            logger.info(f"User {user_id} settings saved")
            return True
        except Exception as e:
            logger.error(f"Error saving user data for {user_id}: {e}")
            return False
    
    @staticmethod
    def set_position(user_id: int, position: str) -> bool:
        """Set logo position for user"""
        data = UserDatabase._load_user_data(user_id)
        data["position"] = position
        return UserDatabase._save_user_data(user_id, data)
    
    @staticmethod
    def set_scale(user_id: int, scale: int) -> bool:
        """Set logo scale percentage for user"""
        data = UserDatabase._load_user_data(user_id)
        data["scale"] = scale
        return UserDatabase._save_user_data(user_id, data)
    
    @staticmethod
    def set_logo(user_id: int, logo_path: str) -> bool:
        """Mark that user has uploaded a logo"""
        data = UserDatabase._load_user_data(user_id)
        data["has_logo"] = True
        success = UserDatabase._save_user_data(user_id, data)
        return success and os.path.exists(logo_path)
    
    @staticmethod
    def get_user_settings(user_id: int) -> Dict:
        """Get all user settings"""
        return UserDatabase._load_user_data(user_id)
    
    @staticmethod
    def has_logo(user_id: int) -> bool:
        """Check if user has uploaded a logo"""
        return os.path.exists(UserDatabase._get_logo_path(user_id))
    
    @staticmethod
    def get_logo_path(user_id: int) -> Optional[str]:
        """Get logo path if it exists"""
        logo_path = UserDatabase._get_logo_path(user_id)
        if os.path.exists(logo_path):
            return logo_path
        return None
