#!/usr/bin/env python
"""
Simple script to run the Telegram bot.
This is a convenience script that imports and runs the main function from main.py.
"""

import logging
import asyncio
from main import main

if __name__ == "__main__":
    logging.info("Starting FoodCalc Telegram Bot...")
    asyncio.run(main())
    logging.info("Bot stopped.")