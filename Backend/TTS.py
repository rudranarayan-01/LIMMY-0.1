import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import load_dotenv

load_dotenv()

# Load environment variables from .env file
AssistantVoice = os.getenv("ASSISTANT_VOICE")
# print(AssistantVoice)


# Asynchronous function to convert a text to audio file formatasync def TextToAudioFile(text):
async def TextToAudioFile(text):
    file_path = os.path.join("Data", "speech.mp3")
    
    try:
        if os.path.exists(file_path):
            os.remove(file_path)  # Remove existing file to prevent overwriting errors
        
        communicate = edge_tts.Communicate(text, AssistantVoice, pitch="+5Hz", rate="+0%")
        await communicate.save(file_path)
    
    except Exception as e:
        print(f"Error generating audio file: {e}")


# print("Text to audio file created")


# Function to manage speech to text functionality 
def TTS(Text, func=lambda r=None: True):
    file_path = os.path.join("Data", "speech.mp3")
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(TextToAudioFile(Text))

        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            if not func():
                break
            clock.tick(10)

    except Exception as e:
        print(f"Error in TTS: {e}")
    
    finally:
        func(False)
        pygame.mixer.music.stop()
        pygame.mixer.quit()


# print("TTS DONE")
        

# Function to manage text to speech with additional response 
def TextToSpeech(Text, func = lambda r = None:True):
    Data = str(Text).split(".")
    
    # List predefined responses for class where the text is too long
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]
    
    # If the text is very long (more than 4 sentences)
    if len(Data) > 4 and len(Text) >= 250:
        TTS(" ".join(Text.split(".")[0:2]) + ". " + random.choice(responses), func )
    
    # Otherwise just play the whole text
    else:
        TTS(Text, func)

# print("TextToSpeech Done")
    
# Main Execution Block 
if __name__ == "__main__":
    while True:
        # Prompt user for input and pass it to TextToSpeech function
        TextToSpeech(input("Enter your query: "))
            
            
# print("Main Execution Block Done")            