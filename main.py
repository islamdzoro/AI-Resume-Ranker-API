# main.py
from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()
app = create_app()


