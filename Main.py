from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    SetMicrophoneStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    AnswerModifier,
    GetAssistantStatus,
    GetMicrophoneStatus
)

from Backend.Model import FirstLayerDMM
from Backend.RealTimeSearchEngine import RealtimeSearchEngine
from Backend. Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TTS import TextToSpeech
from dotenv import load_dotenv
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

load_dotenv()

AssistantName = os.getenv("Assistantname")
Username = os.getenv("Username")
default_message = f'''{Username} : Hello {AssistantName}, How are you?{AssistantName} : Welcome {Username}. I'm doing well. How may I help you ?'''
subprocess = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def ShowDefaultChatIfNoChats():
    File = open(r"Data\ChatLog.json", "r", encoding="utf-8")
    if len(File.read())<5:
        with open(TempDirectoryPath("Database.data"), "w", encoding="utf-8") as file:
            file.write("")
        with open(TempDirectoryPath("Responces.data"), "w", encoding="utf-8") as file:
            file.write(default_message)

def ReadChatLogJson():
    with open(r"Data\ChatLog.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def ChatLogIntegration():
    json_data = ReadChatLogJson() 
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"{Username}: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"{AssistantName}: {entry['content']}\n"
    formatted_chatlog = formatted_chatlog.replace("User", Username + " " )
    formatted_chatlog = formatted_chatlog.replace("Assistant", AssistantName + " " )
    
    with open (TempDirectoryPath("Database.data"), "w", encoding="utf-8") as file:
        file.write(AnswerModifier(formatted_chatlog))
        
def ShowChatsOnGUI():
    File = open (TempDirectoryPath("Database.data"), "r", encoding="utf-8")
    Data = File.read()
    if len(str(Data)) > 0:
        lines = Data.split("\n")
        results = "\n".join(lines)
        File.close()
        File = open(TempDirectoryPath("Responces.data"), "w", encoding="utf-8")
        File.write(results)
        File.close()
        
def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()
    
InitialExecution()

def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""
    
    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username}:{Query}")
    SetAssistantStatus("Thinking...")
    Decision = FirstLayerDMM(Query)
    
    print("")
    print(f"Decision: {Decision}")
    print("")
    
    G = any([i for i in Decision if i.startswith("general")])
    R = any([i for i in Decision if i.startswith("realtime")])
    
    