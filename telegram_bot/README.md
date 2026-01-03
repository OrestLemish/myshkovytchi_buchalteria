# FoodCalc Telegram Bot

This is a Telegram bot that allows users to access the FoodCalc web application as a Telegram Mini App.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- A Telegram account
- A deployed FoodCalc web application

### Step 1: Create a Telegram Bot
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send the command `/newbot` to BotFather
3. Follow the instructions to create a new bot
4. Once created, BotFather will provide you with a token. Save this token as you'll need it later.

### Step 2: Configure the Web App
1. Send the command `/newapp` to BotFather
2. Select your bot
3. Follow the instructions to create a new Web App
4. When asked for the Web App URL, provide the URL of your deployed FoodCalc application
5. Complete the setup process

### Step 3: Install Dependencies
1. Navigate to the `telegram_bot` directory
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Step 4: Configure the Bot
1. Copy the `.env.example` file to a new file named `.env`:
   ```
   cp .env.example .env
   ```
2. Open the `.env` file
3. Replace `your_bot_token_here` with the token provided by BotFather
4. Replace `https://your-deployed-website.com` with the URL of your deployed FoodCalc application
5. Optionally, customize the `WEB_APP_NAME` and `WEB_APP_DESCRIPTION` values

### Step 5: Run the Bot
1. Navigate to the `telegram_bot` directory
2. Run the bot using one of the following methods:

   Option 1: Run the main script directly:
   ```
   python main.py
   ```

   Option 2: Use the convenience script:
   ```
   python run_bot.py
   ```

## Usage
Once the bot is running, users can interact with it using the following commands:
- `/start` - Start the bot and get a button to open the FoodCalc web app
- `/help` - Display help information
- `/about` - Display information about the FoodCalc app

## Django Configuration
To allow your Django application to be embedded as a Telegram Mini App, you need to update the `ALLOWED_HOSTS` setting in your Django settings file to include the Telegram Web App domain:

```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    't.me',
    'telegram.org',
    'telegram.me',
    # Add your production domain when you deploy
]
```

Additionally, you may need to configure CORS (Cross-Origin Resource Sharing) to allow requests from Telegram domains.

## Deployment
For production deployment, it's recommended to:
1. Use environment variables for sensitive information (like the bot token)
2. Set up a proper web server (like Nginx) to serve your Django application
3. Use a process manager (like Supervisor) to keep the bot running

## Troubleshooting
- If the bot doesn't respond, check that it's running and that the token is correct
- If the web app doesn't open, check that the URL is correct and that your Django application is properly configured to allow embedding
- For more detailed logs, adjust the logging level in `main.py`
