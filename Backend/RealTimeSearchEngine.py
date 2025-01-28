from googlesearch import search
from groq import Groq
from json import load, dump
import json
import datetime
from dotenv import dotenv_values, load_dotenv
import os

load_dotenv()

# Load environment variables from .env file
env_vars = dotenv_values(".env")

Username = os.getenv("Username")
Assistantname = os.getenv("Assistantname")
GroqApiKey = os.getenv("GROQ_API_KEY")



# Initialize groq client 
client = Groq(api_key = GroqApiKey)

# Define System instruction for chatbot
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Try to load the chat log from json file or create an empty one if doesn't exist

# Ensure the Data folder exists
os.makedirs("Data", exist_ok=True)

try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
        print("Chat log loaded successfully.")
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        json.dump( [], f)
        print("Chat log file not found. Created a new one.")
        
        
# Function to perform a google search nd format the results
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are: \n[start]\n"
    
    for i in results:
        Answer += f"Title:{i.title} \nDescription:{i.description}\n\n"
    
    Answer += "[end]"
    # print(Answer)
    # print(query)
    return Answer

# function to clean up the results by removing empty lines
def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer


# Predefined Chatbot conversation system messages and an initial user message
SystemChatBot = [
    {"role": "system", "content": System},
    {"role":"user", "content":"Hi"},
    {"role": "assistant", "content":"Hello, how Can I help you!"}
]

# Function to get realtime information like the current date and time
def Information():
    data =""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    data += f"Use the realtime information if needed: \n"
    data += f"Day{day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hour:{minute} minutes:{second} seconds.\n"
    return data

# Function to handle realtime-search and response generation
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages
    
    # Load the chatlog from the json file
    with open(r"Data\ChatLog.json", "r") as f:
        messages = json.load(f)
    # Append the current user message to the chatlog
    messages.append({"role": "user", "content": f"{prompt}"}) 
    
    # Add google search results to the system chatbot message
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})
    
    # Generate a response using the groq client 
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role":"system", "content": Information()}] + messages,
        max_tokens=2048,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None
    )
    
    Answer = ""
    
    
    # Concatenate response chunks from the streaming output
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
    
    # Cleanup response 
    Answer = Answer.strip().replace("<s>","")
    messages.append({"role":"assistant", "content": Answer})
    
    # Save the updated chatlog back to the json file
    with open(r"Data\ChatLog.json", "w") as f:
        json.dump(messages, f, indent=4)
    
    # Remove the most recent chat messages from the chatbot conversation
    SystemChatBot.pop()
    return AnswerModifier(Answer)

# Main entry point of the program for interactive querying
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt)) # prints categorised response
