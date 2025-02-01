import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep
from dotenv import load_dotenv
load_dotenv()



# Function to open and display images based on given prompt
def open_images(prompt):
    folder_path = r"Data"  # Folder where the images are stored
    prompt = prompt.replace(" ", "_")
    
    # Generate the file for the images 
    Files = [f"{prompt}{i}.jpg" for i in range(1,5)]
    
    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        
        try:
            # Try to open and display the image
            img = Image.open(image_path)
            print(f"Opening Image")
            img.show()
            sleep(1) # Pause for 1 second before showing the next image
        
        except IOError:
            print(f"Unable to open {image_path}")
            
print("Image Opened")  

HuggingFaceAPIKey = os.getenv("HuggingFaceAPIKey")  

# API details for the Hugging Face Stable diffusion model          
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization":f"Bearer {HuggingFaceAPIKey}"}

print(HuggingFaceAPIKey)

## Async function to send a query to the Hugging face API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

print("Query")

# Async function to generate image based on the given prompt
async def generate_images(prompt: str):
    tasks = []
    
    # Create 4 tasks to generate images
    for i in range(4):
       payload = {
           "inputs": f"{prompt}, quality=4K, sharpness = maximum, Ultra high details, high resolution, seed = {randint(0, 1000000)} "
       }
       task = asyncio.create_task(query(payload))
       tasks.append(task)
       
    ### Wait for all tasks to complete
    image_bytes_list = await asyncio.gather(*tasks)
    
    # Save the generated images to files
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(" ","_")}{i+1}.jpg", "wb") as f:
            f.write(image_bytes)

            
# Wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)
    

print("Generate Images Done")


### Main Loop to monitor for image generation requests
while True:
    try:
        # Read the status and prompt from the data file
        with open(r"Frontend\Files\ImageGeneration.data","r") as f:
            Data:str = f.read()
        
        Prompt, Status = Data.split(",")
        
        # If the status indicates an image generation request
        if Status == "True":
            print("Generating Images...")
            ImageStatus = GenerateImages(prompt=Prompt)
            
            # Reset the status in the file after generating images
            with open(r"Frontend\Files\ImageGeneration.data","w") as f:
                f.write("False, False")
                break
        else:
            sleep(1)
    except:
        pass
    
print("Done")