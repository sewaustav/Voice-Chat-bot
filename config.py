import os

from dotenv import load_dotenv

load_dotenv()

PICOVOICETOKEN = os.getenv('PICOKELVIN')
PICPATH = os.getenv('PICPATH')
