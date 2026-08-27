import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN','').strip()
ADMIN_IDS = {int(x.strip()) for x in os.getenv('ADMIN_IDS','').split(',') if x.strip().isdigit()}
PANEL_URL = os.getenv('PANEL_URL','').rstrip('/')
PANEL_USERNAME = os.getenv('PANEL_USERNAME','')
PANEL_PASSWORD = os.getenv('PANEL_PASSWORD','')
PANEL_TOKEN = os.getenv('PANEL_TOKEN','')
TEMPLATE_BASIC = int(os.getenv('TEMPLATE_BASIC','0') or 0)
TEMPLATE_PREMIUM = int(os.getenv('TEMPLATE_PREMIUM','0') or 0)
TEMPLATE_VIP = int(os.getenv('TEMPLATE_VIP','0') or 0)
DB_PATH = os.getenv('DB_PATH','data/roxet.db')

BRAND = '🚀 RoXeT VpN'
