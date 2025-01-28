from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv,dotenv_values
import os
import mtranslate

load_dotenv()

# Load environment variables from .env file
env_vars = dotenv_values(".env")

Username = os.getenv("Username")
Assistantname = os.getenv("Assistantname")
GroqApiKey = os.getenv("GROQ_API_KEY")

print(Assistantname)