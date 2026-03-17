"""
Message and callback handlers
Main event handling logic
"""

import os
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, CallbackQuery, User
from database import UserDatabase
from keyboards import (
    get_main_menu_keyboard,
    get_position_keyboard,
    get_size_keyboard,
    get_back_keyboard,
    get_position_name
)
from messages import *
from image_processor import ImageProcessor
from updater import restart_bot
from config import ADMIN_ID
import logging

logger = logging.getLogger(__name__)

# Dictionary to track user state
user_states = {}


def setup_handlers(app: Client):
    """Register all bot handlers"""
    
    @app.on_message(filters.command("start"))
    async def start_handler(client: Client, message: Message):
        """Handle /start command"""
        user_id = message.from_user.id
        logger.info(f"User {user_id} started bot")
        
        # Initialize user settings if needed
        UserDatabase.get_user_settings(user_id)
        
        await message.reply_text(
            get_welcome_message(),
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    @app.on_message(filters.command("help"))
    async def help_handler(client: Client, message: Message):
        """Handle /help command"""
        await message.reply_text(
            get_help_message(),
            reply_markup=get_back_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
    
    @app.on_message(filters.command("update"))
    async def update_handler(client: Client, message: Message):
        """Handle /update command (admin only)"""
        user_id = message.from_user.id
        
        # Check if user is admin
        if ADMIN_ID is None or user_id != ADMIN_ID:
            await message.reply_text(
                "❌ You do not have permission to use this command.",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Show processing message
        status_msg = await message.reply_text(
            "⏳ **Checking for updates...**",
            parse_mode=ParseMode.MARKDOWN
        )
        
        try:
            success, msg = await restart_bot()
            
            if success:
                await status_msg.edit_text(
                    f"✅ **Update Successful**\n\n{msg}\n\n"
                    "_The bot will need to be restarted to apply changes._",
                    parse_mode=ParseMode.MARKDOWN
                )
                logger.info(f"Bot update successful: {msg}")
            else:
                await status_msg.edit_text(
                    f"❌ **Update Failed**\n\n{msg}",
                    parse_mode=ParseMode.MARKDOWN
                )
                logger.error(f"Bot update failed: {msg}")
        
        except Exception as e:
            logger.error(f"Error during update: {e}")
            await status_msg.edit_text(
                f"❌ **Update Error**\n\nAn error occurred: {str(e)}",
                parse_mode=ParseMode.MARKDOWN
            )
    
    @app.on_callback_query()
    async def callback_handler(client: Client, callback_query: CallbackQuery):
        """Handle all callback queries from inline buttons"""
        user_id = callback_query.from_user.id
        data = callback_query.data
        
        await callback_query.answer()
        
        try:
            # Main Menu Navigation
            if data == "set_logo":
                user_states[user_id] = "waiting_for_logo"
                await callback_query.edit_message_text(
                    get_set_logo_message(),
                    reply_markup=get_back_keyboard(),
                    parse_mode=ParseMode.MARKDOWN
                )
            
            elif data == "set_position":
                await callback_query.edit_message_text(
                    get_set_position_message(),
                    reply_markup=get_position_keyboard(),
                    parse_mode=ParseMode.MARKDOWN
                )
            
            elif data == "set_size":
                await callback_query.edit_message_text(
                    get_set_size_message(),
                    reply_markup=get_size_keyboard(),
                    parse_mode=ParseMode.MARKDOWN
                )
            
            elif data == "my_settings":
                settings = UserDatabase.get_user_settings(user_id)
                has_logo = UserDatabase.has_logo(user_id)
                position_name = get_position_name(settings["position"])
                
                await callback_query.edit_message_text(
                    get_my_settings_message(
                        has_logo,
                        settings["position"],
                        settings["scale"],
                        position_name
                    ),
                    reply_markup=get_main_menu_keyboard(),
                    parse_mode=ParseMode.MARKDOWN
                )
            
            elif data == "help":
                await callback_query.edit_message_text(
                    get_help_message(),
                    reply_markup=get_back_keyboard(),
                    parse_mode=ParseMode.MARKDOWN
                )
            
            # Position Selection
            elif data.startswith("pos_"):
                position = data.replace("pos_", "")
                UserDatabase.set_position(user_id, position)
                position_name = get_position_name(position)
                
                await callback_query.edit_message_text(
                    get_position_saved_message(position_name),
                    reply_markup=get_main_menu_keyboard(),
                    parse_mode=ParseMode.MARKDOWN
                )
                logger.info(f"User {user_id} set position to {position}")
            
            # Size Selection
            elif data.startswith("size_"):
                size = int(data.replace("size_", ""))
                UserDatabase.set_scale(user_id, size)
                
                await callback_query.edit_message_text(
                    get_size_saved_message(size),
                    reply_markup=get_main_menu_keyboard(),
                    parse_mode=ParseMode.MARKDOWN
                )
                logger.info(f"User {user_id} set size to {size}%")
            
            # Back to Menu
            elif data == "back_to_menu":
                user_states.pop(user_id, None)
                await callback_query.edit_message_text(
                    get_welcome_message(),
                    reply_markup=get_main_menu_keyboard(),
                    parse_mode=ParseMode.MARKDOWN
                )
        
        except Exception as e:
            logger.error(f"Error in callback handler: {e}")
            await callback_query.edit_message_text(
                get_error_message("general"),
                reply_markup=get_main_menu_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
    
    @app.on_message(filters.photo | filters.document)
    async def image_handler(client: Client, message: Message):
        """Handle image uploads"""
        user_id = message.from_user.id
        
        try:
            # Check if user is waiting for logo upload
            if user_states.get(user_id) == "waiting_for_logo":
                await handle_logo_upload(client, message, user_id)
            
            # Check if user is uploading thumbnail for watermarking
            elif message.photo or (message.document and is_image_document(message.document)):
                await handle_thumbnail_watermarking(client, message, user_id)
            
            else:
                await message.reply_text(
                    get_invalid_input_message(),
                    reply_markup=get_main_menu_keyboard(),
                    parse_mode=ParseMode.MARKDOWN
                )
        
        except Exception as e:
            logger.error(f"Error in image handler: {e}")
            await message.reply_text(
                get_error_message("general"),
                reply_markup=get_main_menu_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
    
    @app.on_message(filters.text & filters.private & ~filters.regex(r'^/'))
    async def text_handler(client: Client, message: Message):
        """Handle text messages"""
        await message.reply_text(
            get_invalid_input_message(),
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )


async def handle_logo_upload(client: Client, message: Message, user_id: int):
    """Handle logo upload from user"""
    try:
        processing_msg = await message.reply_text(
            get_processing_message(),
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Get logo file
        if message.photo:
            file = await client.download_media(message.photo.file_id)
        else:
            file = await client.download_media(message.document.file_id)
        
        # Validate it's a PNG by checking magic bytes and opening with PIL
        try:
            from PIL import Image
            img = Image.open(file)
            if img.format != 'PNG':
                raise ValueError("Not a PNG image")
            # Check for alpha channel (transparency)
            if img.mode not in ('RGBA', 'PA', 'P'):
                # Convert to RGBA if needed
                img = img.convert('RGBA')
        except Exception as e:
            await processing_msg.delete()
            await message.reply_text(
                get_error_message("invalid_logo_format"),
                reply_markup=get_back_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
            if os.path.exists(file):
                os.remove(file)
            return
        
        # Save as user logo with proper .png extension
        from config import LOGOS_PATH
        logo_path = os.path.join(LOGOS_PATH, f"{user_id}.png")
        
        # If file doesn't have .png extension, rename it
        if not file.lower().endswith('.png'):
            os.rename(file, logo_path)
        else:
            os.rename(file, logo_path)
        
        # Update database
        UserDatabase.set_logo(user_id, logo_path)
        user_states.pop(user_id, None)
        
        # Notify user
        await processing_msg.delete()
        await message.reply_text(
            get_logo_saved_message(),
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )
        
        logger.info(f"Logo uploaded successfully for user {user_id}")
    
    except Exception as e:
        logger.error(f"Error uploading logo: {e}")
        await message.reply_text(
            get_error_message("general"),
            reply_markup=get_back_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )


async def handle_thumbnail_watermarking(client: Client, message: Message, user_id: int):
    """Handle thumbnail watermarking"""
    try:
        # Check if user has logo
        if not UserDatabase.has_logo(user_id):
            await message.reply_text(
                get_error_message("no_logo"),
                reply_markup=get_main_menu_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Show processing message
        processing_msg = await message.reply_text(
            get_processing_message(),
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Download thumbnail
        if message.photo:
            file = await client.download_media(message.photo.file_id)
        else:
            file = await client.download_media(message.document.file_id)
        
        # Get user settings
        settings = UserDatabase.get_user_settings(user_id)
        logo_path = UserDatabase.get_logo_path(user_id)
        
        # Process image
        output_path = ImageProcessor.get_temp_path(user_id)
        
        success = ImageProcessor.apply_watermark(
            file,
            logo_path,
            settings["position"],
            settings["scale"],
            output_path
        )
        
        # Clean up input file
        if os.path.exists(file):
            os.remove(file)
        
        if not success:
            await processing_msg.delete()
            await message.reply_text(
                get_error_message("processing_failed"),
                reply_markup=get_main_menu_keyboard(),
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        # Send result
        await processing_msg.delete()
        
        with open(output_path, 'rb') as result_file:
            await message.reply_photo(
                result_file,
                caption=get_success_message(),
                parse_mode=ParseMode.MARKDOWN
            )
        
        # Cleanup
        ImageProcessor.cleanup_temp_file(output_path)
        logger.info(f"Watermark applied successfully for user {user_id}")
    
    except Exception as e:
        logger.error(f"Error processing thumbnail: {e}")
        await message.reply_text(
            get_error_message("processing_failed"),
            reply_markup=get_main_menu_keyboard(),
            parse_mode=ParseMode.MARKDOWN
        )


def is_image_document(document) -> bool:
    """Check if document is an image"""
    if not document.mime_type:
        return False
    return document.mime_type.startswith('image/')
