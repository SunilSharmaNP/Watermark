"""
Professional Telegram Watermark Bot
Main entry point and bot initialization
"""

import asyncio
import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import setup_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Initialize and run the bot"""
    app = Client(
        "watermark_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )
    
    # Setup all handlers
    setup_handlers(app)
    
    logger.info("🤖 Starting Watermark Bot...")
    
    async with app:
        logger.info("✅ Bot is running and listening for messages...")
        await app.run()


if __name__ == "__main__":
    asyncio.run(main())
