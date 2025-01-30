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


###########  TEST ##################
import asyncio
import os
import pygame
import edge_tts

async def TextToAudioFile(text: str, file_path: str = r"Data\speech.mp3") -> None:
    """Generates an audio file from text using edge-tts."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Ensure 'Data' directory exists

    if os.path.exists(file_path):
        os.remove(file_path)  # Remove existing file to prevent conflicts

    AssistantVoice = "en-CA-LiamNeural"  # Adjust the voice as needed
    tts = edge_tts.Communicate(text, AssistantVoice, pitch="+5Hz", rate="+13%")
    
    await tts.save(file_path)  # Save generated speech

def TTS(text: str, func=lambda _: True):
    """Manages text-to-speech playback, calling func(False) when playback stops."""
    try:
        # Ensure event loop is handled properly
        if asyncio.get_event_loop().is_running():
            asyncio.ensure_future(TextToAudioFile(text))
        else:
            asyncio.run(TextToAudioFile(text))

        # Initialize pygame mixer for audio playback
        pygame.mixer.init()

        # Load and play the generated speech file
        audio_path = r"Data\speech.mp3"
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

        clock = pygame.time.Clock()  # Create a clock instance

        # Loop until the audio is playing or func() signals stop
        while pygame.mixer.music.get_busy():
            if not func():  # If func() returns False, stop playback
                break
            clock.tick(10)  # Limit loop to 10 ticks per second

        return True

    except Exception as e:
        print(f"Error in TTS: {e}")

    finally:
        try:
            func(False)  # Signal the end of TTS
            pygame.mixer.music.stop()
            pygame.mixer.quit()

        except Exception as e:
            print(f"Error in finally block: {e}")

########### TEST DONE #################

# # Asynchronous function to convert a text to audio file format
# async def TextToAudioFile(text)->None:
#     file_path = r"Data\speech.mp3" # Define the path where the audio file will be written
    
    
#     if os.path.exists(file_path): 
#         # if the audio file already exists then remove it for overwriting error 
#         os.remove(file_path)
    
#     # Create the communicate object to generate the speech
#     communicate = edge_tts.communicate(text,AssistantVoice, pitch = "+5Hz", rate ="+13%" )
#     await communicate.save(file_path)

# print("Text to audio file created")


# # Function to manage speech to text functionality 
# def TTS(Text, func = lambda r = None:True):
#     while True:
#         try:
#             asyncio.run(TextToAudioFile(Text))
            
#             # Intialize pygame mixer for audio playback
#             pygame.mixer.init()
            
#             # Load the generated speech file to pygame mixer
#             pygame.mixer.music.load(r"Data\speech.mp3")
#             pygame.mixer.music.play()
            
#             # Loop unitil the audio is playing or the function is stops
#             while pygame.mixer.music.get_busy():
#                 # Check if the external function returns false
#                 if func() == False:
#                     break
#                 pygame.time.Clock.tick(10) # Limit the loop to 10 ticks per second
                
#             return True
        
#         except Exception as e:
#             print(f"Error in TTS:{e}")
            
#         finally:
#             try:
#                 # Call the provided function with false to Signal the end of TTS
#                 func(False)
#                 pygame.mixer.music.stop()
#                 pygame.mixer.quit()
            
#             except Exception as e:
#                 print(f"Error in finally Block: {e}")
                

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

print("TextToSpeech Done")
    
# Main Execution Block 
if __name__ == "__main__":
    while True:
        # Prompt user for input and pass it to TextToSpeech function
        TextToSpeech(input("Enter your query: "))
            
            
print("Main Execution Block Done")            