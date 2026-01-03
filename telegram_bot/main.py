import logging
import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

# Load environment variables from .env file
load_dotenv()

# Get configuration from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBSITE_URL = os.getenv("WEBSITE_URL")
WEB_APP_NAME = os.getenv("WEB_APP_NAME", "FoodCalc")
WEB_APP_DESCRIPTION = os.getenv("WEB_APP_DESCRIPTION", "Calculate and track your daily food intake")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Command handler for /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Handler for the /start command.
    Sends a welcome message with a button to open the web app.
    """
    # Create a keyboard with a button that opens the web app
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Open {WEB_APP_NAME}",
                    web_app=WebAppInfo(url=WEBSITE_URL)
                )
            ]
        ]
    )

    await message.answer(
        f"Welcome to {WEB_APP_NAME} Bot!\n\n"
        f"{WEB_APP_DESCRIPTION}\n\n"
        "Click the button below to open the app:",
        reply_markup=keyboard
    )

# Command handler for /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """
    Handler for the /help command.
    Provides information about how to use the bot.
    """
    help_text = (
        f"🤖 *{WEB_APP_NAME} Bot Help*\n\n"
        "Available commands:\n"
        "/start - Start the bot and get the main menu\n"
        "/help - Show this help message\n"
        "/about - Information about the app\n\n"
        "To use the app, simply click on the 'Open App' button that appears after the /start command."
    )

    await message.answer(help_text, parse_mode="Markdown")

# Command handler for /about
@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    """
    Handler for the /about command.
    Provides information about the app.
    """
    about_text = (
        f"📱 *About {WEB_APP_NAME}*\n\n"
        f"{WEB_APP_DESCRIPTION}\n\n"
        "This is a Telegram Mini App that allows you to access the full functionality "
        "of our web application directly within Telegram.\n\n"
        "Enjoy using our app!"
    )

    # Create a keyboard with a button that opens the web app
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Open {WEB_APP_NAME}",
                    web_app=WebAppInfo(url=WEBSITE_URL)
                )
            ]
        ]
    )

    await message.answer(about_text, parse_mode="Markdown", reply_markup=keyboard)

# Default message handler
@dp.message()
async def echo(message: types.Message):
    """
    Default handler for all other messages.
    Suggests using the /start command.
    """
    await message.answer(
        "I don't understand that command. Please use /start to access the app or /help for assistance."
    )

# Main function to start the bot
async def main():
    # Skip pending updates and start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.info("Starting bot...")
    asyncio.run(main())
