import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token_here')
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://your-domain.com')

# Database
DB_FILE = 'ayron_data.json'

# Flask
FLASK_PORT = int(os.getenv('PORT', 5000))
FLASK_HOST = '0.0.0.0'

# EGA ID
EGA_ID = int(os.getenv('EGA_ID', '8168552332'))
