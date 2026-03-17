"""
Message templates and text content
Centralized message management
"""


def get_welcome_message() -> str:
    """Welcome message when user starts bot"""
    return """🎨 **Welcome to Watermark Bot!**

I'll help you add professional watermarks to your thumbnails automatically.

**How it works:**
1. Upload your logo (PNG format)
2. Choose where to place it
3. Set the logo size
4. Send any thumbnail image and I'll add your watermark!

Let's get started! What would you like to do?"""


def get_set_logo_message() -> str:
    """Message when user selects Set Logo"""
    return """📸 **Upload Your Logo**

Please send a PNG image that you want to use as a watermark.

**Requirements:**
- Format: PNG (with transparency support)
- Max size: 5MB
- Recommended: Square format for best results

⏸️ *Press "« Back" to cancel*"""


def get_set_position_message() -> str:
    """Message when user selects Set Position"""
    return """📍 **Choose Logo Position**

Select where you want your logo to appear on the thumbnail:"""


def get_set_size_message() -> str:
    """Message when user selects Set Size"""
    return """📏 **Select Logo Size**

Choose what percentage of the thumbnail the logo should occupy:"""


def get_my_settings_message(has_logo: bool, position: str, scale: int, position_name: str) -> str:
    """Show current user settings"""
    logo_status = "✅ Logo uploaded" if has_logo else "❌ No logo set"
    
    return f"""⚙️ **Your Settings**

**Logo:** {logo_status}
**Position:** {position_name}
**Scale:** {scale}%

Your watermark is configured and ready to use!

Simply send any thumbnail image and I'll process it with your settings."""


def get_help_message() -> str:
    """Help message with instructions"""
    return """❓ **Help & Instructions**

**How to use:**
1. **Set Logo** - Upload a PNG image as your watermark
2. **Set Position** - Choose where the logo appears (9 positions available)
3. **Set Size** - Select logo size from 10% to 30%
4. **My Settings** - View your current configuration
5. **Auto Processing** - Send any image after setup and it will be watermarked

**Supported formats:**
- Input: JPG, PNG, WebP (any image format)
- Logo: PNG (recommended with transparency)
- Output: JPEG (high quality)

**Pro Tips:**
- Use PNG logos with transparent background for best results
- Choose a size that doesn't cover important content
- The logo will be automatically fitted to your selected scale

Need more help? Contact @support or visit our website."""


def get_logo_saved_message() -> str:
    """Message when logo is successfully saved"""
    return """✅ **Logo Saved Successfully!**

Your watermark logo has been uploaded and saved.

What would you like to do next?"""


def get_position_saved_message(position_name: str) -> str:
    """Message when position is saved"""
    return f"""✅ **Position Saved!**

Logo position set to: {position_name}

Ready to process thumbnails with this configuration."""


def get_size_saved_message(size: int) -> str:
    """Message when size is saved"""
    return f"""✅ **Size Saved!**

Logo size set to: {size}%

Ready to process thumbnails with this configuration."""


def get_processing_message() -> str:
    """Message shown while processing image"""
    return """⏳ **Processing your thumbnail...**

Adding watermark and optimizing image..."""


def get_success_message() -> str:
    """Message when watermark is applied successfully"""
    return """✅ **Watermark Applied Successfully!**

Your thumbnail is ready! Download the image below.

Want to process another image? Just send it!"""


def get_error_message(error_type: str = "general") -> str:
    """Error messages"""
    errors = {
        "general": "❌ An error occurred. Please try again.",
        "invalid_format": "❌ Invalid file format. Please send a valid image (JPG, PNG, WebP, etc.)",
        "invalid_logo_format": "❌ Logo must be in PNG format with transparency support.",
        "no_logo": "❌ Please set up your logo first using 'Set Logo' button.",
        "logo_too_large": "❌ Logo file is too large. Maximum 5MB.",
        "image_too_large": "❌ Image is too large. Maximum 4000x4000 pixels.",
        "processing_failed": "❌ Failed to process image. Please try again.",
    }
    return errors.get(error_type, errors["general"])


def get_invalid_input_message() -> str:
    """Message for invalid input"""
    return """⚠️ **Invalid Input**

Please use the buttons to navigate. Send images only when requested."""
