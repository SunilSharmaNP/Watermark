"""
Keyboard layouts and UI components
Manages all inline and reply keyboards
"""

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Main menu with all options"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎨 Set Logo", callback_data="set_logo"),
            InlineKeyboardButton("📍 Set Position", callback_data="set_position")
        ],
        [
            InlineKeyboardButton("📏 Set Logo Size", callback_data="set_size"),
            InlineKeyboardButton("⚙️ My Settings", callback_data="my_settings")
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data="help")
        ]
    ])


def get_position_keyboard() -> InlineKeyboardMarkup:
    """9-position grid keyboard"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("↖️ Top Left", callback_data="pos_top_left"),
            InlineKeyboardButton("⬆️ Top", callback_data="pos_top"),
            InlineKeyboardButton("↗️ Top Right", callback_data="pos_top_right")
        ],
        [
            InlineKeyboardButton("⬅️ Left", callback_data="pos_middle_left"),
            InlineKeyboardButton("⏺️ Center", callback_data="pos_center"),
            InlineKeyboardButton("➡️ Right", callback_data="pos_middle_right")
        ],
        [
            InlineKeyboardButton("↙️ Bottom Left", callback_data="pos_bottom_left"),
            InlineKeyboardButton("⬇️ Bottom", callback_data="pos_bottom"),
            InlineKeyboardButton("↘️ Bottom Right", callback_data="pos_bottom_right")
        ],
        [
            InlineKeyboardButton("« Back", callback_data="back_to_menu")
        ]
    ])


def get_size_keyboard() -> InlineKeyboardMarkup:
    """Size selection keyboard"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("10%", callback_data="size_10"),
            InlineKeyboardButton("15%", callback_data="size_15"),
            InlineKeyboardButton("20%", callback_data="size_20")
        ],
        [
            InlineKeyboardButton("25%", callback_data="size_25"),
            InlineKeyboardButton("30%", callback_data="size_30")
        ],
        [
            InlineKeyboardButton("« Back", callback_data="back_to_menu")
        ]
    ])


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Simple back button"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("« Back to Menu", callback_data="back_to_menu")
        ]
    ])


def get_position_name(position_key: str) -> str:
    """Convert position key to readable name"""
    positions = {
        "top_left": "↖️ Top Left",
        "top": "⬆️ Top",
        "top_right": "↗️ Top Right",
        "middle_left": "⬅️ Middle Left",
        "center": "⏺️ Center",
        "middle_right": "➡️ Middle Right",
        "bottom_left": "↙️ Bottom Left",
        "bottom": "⬇️ Bottom",
        "bottom_right": "↘️ Bottom Right",
    }
    return positions.get(position_key, position_key)
