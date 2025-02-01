import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("DEEPAI_API_KEY")

# Replace with your DeepAI API Key

TEXT_PROMPT = "A futuristic city skyline at sunset"

def generate_image(prompt):
    url = "https://api.deepai.org/api/text2img"
    headers = {"api-key": API_KEY}
    data = {"text": prompt}

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        result = response.json()
        image_url = result.get("output_url")
        print(f"Image URL: {image_url}")
    else:
        print("Error:", response.text)

generate_image(TEXT_PROMPT)

print (API_KEY)