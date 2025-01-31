import subprocess
from dotenv import load_dotenv
import os
from groq import Groq


load_dotenv()


useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 "
GroqAPIKey = os.getenv("GROQ_API_KEY")
# Initialize groq client 
client = Groq(api_key = GroqAPIKey)

messages = []

SystemChatBot = [{"role": "system", "content": f"Hello, I'm {os.getenv('Username')}, You are a content writter. You have to write content like letter"}]


# Function to generate content using AI and save it to a file
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


print("Compile done")
Content("Write a application for sick leave")
print("Program Done")