# from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

print("import done")

# Load environment variables from .env file
load_dotenv()

GroqAPIKey = os.getenv("GROQ_API_KEY")
print("GroqAPIKey")

# Define CSS classes for parsing specific elements in HTML content
classes = ["zCubwf", "hgKElc", "LTKOO sy7ric", "Z0Lcw", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", "IZ6rdc",
           "O5uRd LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers_table", "dDoNo ikb4Bb gsrt", "sXLaOe", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a web agent for making web requests
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 "

# Initialize groq client 
client = Groq(api_key = GroqAPIKey)

# Predefined professional responses for user interactions
professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there anything else I can help you with",
    "I'm at your service for any additional questions or supports you may need. Don't hesitate to ask ",
]

# List of messages 
messages = []

# System messages for providing context to chatbot
SystemChatBot = [{"role": "system", "content": f"Hello, I'm {os.getenv['Username']}, You are a content writter. You have to write content like letter"}]


# Function to perform google search 
def GoogleSearch(Topic):
    search(Topic) # use pywhatkit search funtion to perform a google search
    return True

# GoogleSearch("Rudranarayan Sahu")

# Function to generate content using AI and save it to a file
# def Content(Topic):
#     # Nested function to open a file in Notepad
#     def OpenNotepad(File):
#         default_text_editor = "notepad.exe"
#         subprocess.Popen([default_text_editor,File])
    
#     # Nested function to generate Content using AI Chatbot
#     def ContentWritterAI(prompt):
#         messages.append({"role":"user", "content":f"{prompt}"})
        
#         completions = client.chat.completions.create(
#             model="mixtral-8x7b-32768",
#             messages= SystemChatBot + messages,
#             max_tokens= 2048,
#             temperature=0.7,
#             top_p=1,
#             stream=True,
#             stop=None
#         )
        
#         Answer = ""
        
#         # Process streamed response chunks
#         for chunk in completions:
#             if chunk.choices[0].delta.content:
#                 Answer += chunk.choices[0].delta.content
        
#         Answer = Answer.replace("</s>","")
#         messages.append({"role":"assistant", "content": Answer})
#         return Answer
    
#     Topic: str = Topic.replace("Content", "")
#     ContentByAI = ContentWritterAI(Topic)
    
#     # Save the generated content to a file
#     with open(rf"Data\{Topic.lower().replace(' ','')}.txt","w", encoding="utf-8") as file:
#         file.write(ContentByAI)
#         file.close()
        
#     OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt") # Open the generated content in Notepad
#     return True

############## OWN CONTENT ###########
def Content(Topic):
    # Nested function to open a file in Notepad
    def OpenNotepad(File):
        default_text_editor = "notepad.exe"
        subprocess.Popen([default_text_editor,File])
    
    # Nested function to generate Content using AI Chatbot
    def ContentWritterAI(prompt):
        messages.append({"role":"user", "content":f"{prompt}"})
        
        completions = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages= SystemChatBot + messages,
            max_tokens= 2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        
        Answer = ""
        
        # Process streamed response chunks
        for chunk in completions:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        
        Answer = Answer.replace("</s>","")
        messages.append({"role":"assistant", "content": Answer})
        return Answer
    
    Topic: str = Topic.replace("Content", "")
    ContentByAI = ContentWritterAI(Topic)
    
    # Save the generated content to a file
    with open(rf"Data\{Topic.lower().replace(' ','')}.txt","w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()
        
    OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt") # Open the generated content in Notepad
    return True


# print("Compile done")
# Content("Write a application for sick leave")
# print("Program Done")

#########################################################################################

# Function to search for a topic in the youtube
def YoutubeSearch(Topic): 
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

# Function to play a video in the youtube
def PlayYouTube(query):
    playonyt(query)
    return True

# Function to open a specific application or relevent page
# def OpenApp(app, sess = requests.session()):
#     try:
#         # appopen(app, match_closest=True, output=True, throw_error = True)
#         return True
#     except:
#         def extract_links(html):
#             if html is None:
#                 return []
#             soup = BeautifulSoup(html, 'html.parser')
#             links = soup.find_all('a', {'jsname':'UWckNb'})
#             return [link.get('href') for link in links]
        
#         # Nested function to perform google search and retrive HTML
#         def search_google(query):
#             url = "http://www.google.com/search?q={query}"
#             headers = {"User-Agent": useragent}
#             response = sess.get(url, headers=headers)
            
#             if response.status_code == 200:
#                 return response.text
#             else:
#                 print("Failed to retrieve search results")
#             return None
        
#         html = search_google(app)
#         if html:
#             link = extract_links(html)[0]
#             webopen(link)
        
#         return True


#### OPENING APPS USING OS ############

def OpenApp(app, sess = requests.session()):
    # Dictionary for official app download URLs
    app_websites = {
        'whatsapp': 'https://www.whatsapp.com/download',
        'spotify': 'https://www.spotify.com/download',
        'vlc': 'https://www.videolan.org/vlc/download-windows.html',
        'canva': 'https://www.canva.com/',
        'notepad': 'https://www.microsoft.com/en-us/p/notepad',
        'excel': 'https://www.microsoft.com/en-us/microsoft-365/excel',
        'powerpoint': 'https://www.microsoft.com/en-us/microsoft-365/powerpoint',
        'vscode': 'https://code.visualstudio.com/Download',
        'chrome': 'https://www.google.com/chrome/',
    }
    
    # Dictionary for executable names (used by subprocess)
    app_executables = {
        'whatsapp': 'whatsapp',
        'spotify': 'spotify',
        'vlc': 'vlc',
        'canva': 'canva',
        'notepad': 'notepad',
        'excel': 'excel',
        'powerpoint': 'powerpoint',
        'vscode': 'code',  # Visual Studio Code command is 'code'
        'chrome': 'chrome',  # Google Chrome
    }
    
    # Normalize app name to lowercase
    app = app.lower()

    # Try to open the app using subprocess (check if it's installed)
    try:
        # Try running the app executable (without path, assuming it's in PATH)
        subprocess.run([app_executables[app]], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{app.capitalize()} opened successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error opening {app.capitalize()}: {e}")
    except FileNotFoundError:
        print(f"{app.capitalize()} is not found in system PATH.")
    
    # If not found, search for the app and redirect to its website
    if app in app_websites:
        print(f"{app.capitalize()} is not installed. Redirecting to the official website...")
        webbrowser.open(app_websites[app])
        return True
    else:
        print(f"App '{app}' is not recognized, and no website is available for it.")
        return False

# Example usage:
# OpenApp('notepad')  # Try opening WhatsApp or redirect to its website



# Function to close the application
def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error = True)
            return True
        except: 
            return False
        
        
## Function to execute System level commands
def System(command):
    # Nested function to mute the system volume
    def mute():
        keyboard.press_and_release("volume mute")
    def unmute():
        keyboard.press_and_release("volume unmute")   
    def volume_up():
        keyboard.press_and_release("volume up")
    def volume_down():
        keyboard.press_and_release("volume down")
    
 ## Execute the appropriate commands
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume_up":
        volume_up()
    elif command == "volume_down":
        volume_down()
    
    return True


# Asynchronous function to translate and execute user commands
async def TranslateAndExecute(commands: list[str]):
    funcs = []
    
    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            if "open file" == command:
                pass
            
            else: 
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)
                
        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google_search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube_search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No functions found for command {command}")
            
    results = await asyncio.gather(*funcs)
    
    for result in results:
        if isinstance(result, str):
            yield result
        else: 
            yield result
            

## Asynchronous function to automate command execution
async def Automation (commands : list[str]):

    
    async for result in TranslateAndExecute(commands):
        pass
    return True # Indicates success
    
                     