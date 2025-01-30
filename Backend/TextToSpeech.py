import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables from .env file
AssistantVoice = os.getenv("ASSISTANT_VOICE")

# Asynchronous function to convert a text to audio file format
async def TextToAudioFile(text)->None:
    file_path = r"Data\speech.mp3" # Define the path where the audio file will be written
    
    
    if os.path.exists(file_path): 
        # if the audio file already exists then remove it for overwriting error 
        os.remove(file_path)
    
    # Create the communicate object to generate the speech
    communicate = edge_tts.communicate(text,AssistantVoice, pitch = "+5Hz", rate ="+13%" )
    await communicate.save(r"Data\speech.mp3")

# Function to manage speech to text functionality 
def TTS(Text, func = lambda r = None:True):
    while True:
        try:
            asyncio.run(TextToAudioFile(Text))
            
            # Intialize pygame mixer for audio playback
            pygame.mixer.init()
            
            # Load the generated speech file to pygame mixer
            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play()
            
            # Loop unitil the audio is playing or the function is stops
            while pygame.mixer.music.get_busy():
                # Check if the external function returns false
                if func() == False:
                    break
                pygame.time.Clock.tick(10) # Limit the loop to 10 ticks per second
                
            return True
        
        except Exception as e:
            print(f"Error in TTS:{e}")
            
        finally:
            try:
                # Call the provided function with false to Signal the end of TTS
                func(False)
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            
            except Exception as e:
                print(f"Error in finally Block: {e}")
        

# Function to manage text to speech with additional response 

            
            
            