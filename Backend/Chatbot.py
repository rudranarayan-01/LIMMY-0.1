from groq import Groq
from json import load, dump
import json
import datetime
from dotenv import dotenv_values, load_dotenv
import os

load_dotenv()

data_folder = "Data"
file_name = "ChatLog.json"

file_path = os.path.join(data_folder, file_name)
print(file_path)

# Load environment variables from .env file

env_vars = dotenv_values(".env")

# Retrive API keys
Username = os.getenv("Username")
Assistantname = os.getenv("Assistantname")
GroqApiKey = os.getenv("GROQ_API_KEY")



# Initialize groq client 
client = Groq(api_key = GroqApiKey)

# Initialize empty list to store chat messages
messages = []

# Define a system message that provides context to the AI chatbot about its role and behaviour
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {"role": "system", "content": "System",}
]

# Attempt to load the chat log from JSON file
# 
# Ensure the Data folder exists
os.makedirs("Data", exist_ok=True)
# Attempt to load the chat log from JSON file
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = json.load(f)
        print("Chat log loaded successfully.")
except FileNotFoundError:
    # If the file doesn't exist, create it
    messages = []
    with open(r"Data\ChatLog.json", "w") as f:
        json.dump(messages, f, indent=4)
        print("Chat log file not found. Created a new one.")
except json.JSONDecodeError:
    # Handle corrupted JSON file
    messages = []
    with open(r"Data\ChatLog.json", "w") as f:
        json.dump(messages, f, indent=4)
        print("Chat log file is corrupted. Reinitialized.")

# # Print the chat log structure
# print(messages)




# function to get real-time date and time information
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    
    # format the information into a string
    data = f"Please use the real-time information if needed, \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}"
    data += f"Time: {hour} hour:{minute} minutes:{second} seconds. \n"
    return data

# function to modify the chatbot's response for better formatting
def AnswerModifier(Answer):
    lines = Answer.split("\n") # Split the responses into lines
    non_empty_lines = [line for line in lines if line.strip()] # Remove empty lines
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Main chatbot function to handle user queries 
def ChatBot(Query):
    """ This function sends the user's query to the chatbot and returns the AI response """

    try:
        with open(r"Data\ChatLog.json", "r") as f:
            messages = load(f)
        
        # Append the user's query to the message list
        messages.append({"role": "user", "content": f"{Query}"})
        
        # Make a request to the Groq API for a response
        completion = client.chat.completions.create(
            model = "llama3-70b-8192",
            messages=SystemChatBot + [{"role":"system", "content":RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        Answer = "" # Initialized a empty string to store AI response
        
        # Process the streamed response chunks
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
                
        Answer = Answer.replace("</s>","")  # cleanup any unwanted tokens from the response
        
        messages.append({"role":"assistant", "content": Answer})
        
        # Save the updated chat log to JSON file
        with open(r"Data\ChatLog.json", "w") as f:
            dump(messages, f)
        
        return AnswerModifier(Answer)
    
    except Exception as e:
        # Handle errors by printing the exception and resetting the chat log
        print(f"Error: {e}")
        with open(r"Data\ChatLog.json", "w") as f:
            dump([],f, indent=4)
            
        return ChatBot(Query) # Retry the query after resetting the chat log
    
            


# Main Program enntry point 
if __name__ == "__main__":
    while True:
        user_input = input("Enter your Question: ")
        print(ChatBot(user_input)) # 
