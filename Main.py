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