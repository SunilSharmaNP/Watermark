"""
Image processing module
Handles watermarking and image manipulation using Pillow
"""

import os
from PIL import Image
from typing import Tuple, Optional
from config import THUMBNAIL_MAX_SIZE, LOGO_MAX_SIZE, QUALITY, TEMP_PATH
import logging

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Handles all image processing operations"""
    
    # Position coordinates mapping
    POSITIONS = {
        "top_left": (0, 0, "top_left"),
        "top": (0.5, 0, "top"),
        "top_right": (1, 0, "top_right"),
        "middle_left": (0, 0.5, "middle_left"),
        "center": (0.5, 0.5, "center"),
        "middle_right": (1, 0.5, "middle_right"),
        "bottom_left": (0, 1, "bottom_left"),
        "bottom": (0.5, 1, "bottom"),
        "bottom_right": (1, 1, "bottom_right"),
    }
    
    # Padding in pixels
    PADDING = 10
    
    @staticmethod
    def _calculate_position(
        thumbnail_size: Tuple[int, int],
        logo_size: Tuple[int, int],
        position: str
    ) -> Tuple[int, int]:
        """Calculate logo placement coordinates"""
        
        if position not in ImageProcessor.POSITIONS:
            position = "bottom_right"
        
        x_ratio, y_ratio, _ = ImageProcessor.POSITIONS[position]
        thumb_w, thumb_h = thumbnail_size
        logo_w, logo_h = logo_size
        
        # Calculate base positions
        x = int((thumb_w - logo_w) * x_ratio)
        y = int((thumb_h - logo_h) * y_ratio)
        
        # Apply padding based on position
        if x_ratio == 0:  # Left side
            x = ImageProcessor.PADDING
        elif x_ratio == 1:  # Right side
            x = thumb_w - logo_w - ImageProcessor.PADDING
        else:  # Center
            x = int((thumb_w - logo_w) / 2)
        
        if y_ratio == 0:  # Top side
            y = ImageProcessor.PADDING
        elif y_ratio == 1:  # Bottom side
            y = thumb_h - logo_h - ImageProcessor.PADDING
        else:  # Middle
            y = int((thumb_h - logo_h) / 2)
        
        # Ensure logo stays within bounds
        x = max(ImageProcessor.PADDING, min(x, thumb_w - logo_w - ImageProcessor.PADDING))
        y = max(ImageProcessor.PADDING, min(y, thumb_h - logo_h - ImageProcessor.PADDING))
        
        return (x, y)
    
    @staticmethod
    def resize_logo(logo_path: str, scale: int) -> Optional[Image.Image]:
        """Resize logo based on scale percentage"""
        try:
            logo = Image.open(logo_path).convert("RGBA")
            
            # Validate scale
            scale = max(5, min(50, scale))
            
            # Calculate new size (max dimension)
            max_dimension = max(LOGO_MAX_SIZE, 200)
            new_width = int(max_dimension * scale / 100)
            
            # Maintain aspect ratio
            ratio = new_width / logo.width
            new_height = int(logo.height * ratio)
            
            resized_logo = logo.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS
            )
            
            logger.info(f"Logo resized to {new_width}x{new_height}")
            return resized_logo
            
        except Exception as e:
            logger.error(f"Error resizing logo: {e}")
            return None
    
    @staticmethod
    def apply_watermark(
        thumbnail_path: str,
        logo_path: str,
        position: str,
        scale: int,
        output_path: str
    ) -> bool:
        """Apply watermark to thumbnail"""
        try:
            # Open thumbnail
            thumbnail = Image.open(thumbnail_path).convert("RGB")
            
            # Validate thumbnail size
            if max(thumbnail.size) > THUMBNAIL_MAX_SIZE:
                ratio = THUMBNAIL_MAX_SIZE / max(thumbnail.size)
                new_size = (
                    int(thumbnail.width * ratio),
                    int(thumbnail.height * ratio)
                )
                thumbnail = thumbnail.resize(
                    new_size,
                    Image.Resampling.LANCZOS
                )
                logger.info(f"Thumbnail resized to {new_size}")
            
            # Resize and prepare logo
            logo = ImageProcessor.resize_logo(logo_path, scale)
            if logo is None:
                logger.error("Failed to resize logo")
                return False
            
            # Calculate position
            position_coords = ImageProcessor._calculate_position(
                thumbnail.size,
                logo.size,
                position
            )
            
            # Create a transparent layer for the logo
            if logo.mode != 'RGBA':
                logo = logo.convert('RGBA')
            
            # Paste logo onto thumbnail
            thumbnail.paste(
                logo,
                position_coords,
                logo  # Use logo alpha channel as mask
            )
            
            # Save result
            thumbnail.save(output_path, "JPEG", quality=QUALITY, optimize=True)
            logger.info(f"Watermarked image saved to {output_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error applying watermark: {e}")
            return False
    
    @staticmethod
    def get_temp_path(user_id: int, filename: str = "output.jpg") -> str:
        """Get temporary file path for user"""
        return os.path.join(TEMP_PATH, f"{user_id}_{filename}")
    
    @staticmethod
    def cleanup_temp_file(file_path: str) -> None:
        """Remove temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Temp file cleaned: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning temp file: {e}")
