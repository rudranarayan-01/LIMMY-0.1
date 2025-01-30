from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv,dotenv_values
import os
import mtranslate as mt

load_dotenv()

# Load environment variables from .env file
env_vars = dotenv_values(".env")

InputLanguage = os.getenv("INPUT_LANGUAGE")
# print(InputLanguage)

HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Replace the language setting in the HTML code with input language from the environment variable
HtmlCode = str(HtmlCode).replace("recognition.lang = ''; ", f"recognition.lang = '{InputLanguage}';" )

# Write the modified HTML code to a file 
with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

# Get the current working directory
current_dir = os.getcwd()

# Generate the file path for the HTML file
Link = f"{current_dir}/Data/Voice.html"

# print("Web driver connecting")

# Set Chrome options for the web driver
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f'--user-agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-devices-for-media-stream")
chrome_options.add_argument("--headless=new")  # Use --headless if issues arise



# Initialize the chrome webdriver using the Chrome Driver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# print("Web driver connection established")

# Define the path for temporary files
TempDirPath = rf"{current_dir}/Frontend/Files"

# Function to set assistant status by writing to it a file 
def SetAssistantStatus(Status):
    with open(rf"{TempDirPath}/Status.data", "w", encoding='utf-8') as file:
        file.write(Status)

# Function to modify a query to ensure proper punctuation and formatting
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how" ,"what" , "who", "where",  "when", "why", "which", "whose", "whom", "can you", "what's", "who's", "where's" ]
    
    # Check if the query is questioned and add the question mark to it
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?' , '!']:
            new_query = new_query [:-1] + "?"
        else:
            new_query += "?" 
    else:
        # Add a period to the end of the query if it doesn't end with one
        if query_words[-1][-1] not in ['.', '?' , '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    
    return new_query.capitalize()


# Function to translate text into english using mtranslate library
def UniversalTranslater(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Function to perform speech recognition using webDriver
def SpeechRecognition():
    # Open the HTML file in the browser
    driver.get("file:///"+Link)
    # Start the recognition by clicking on the start button
    driver.find_element(by=By.ID, value= "start").click()
    
    while True:
        try:
            # get the recognised text from the HTML output file
            Text = driver.find_element(by=By.ID, value="output").text
            
            if Text:
                # Stop the recognition by clicking on the stop button
                driver.find_element(by=By.ID, value="end").click()
                
                # If the input was in English then return the modified query
                if InputLanguage.lower() == "en" or "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else: 
                    # If the language is not English then translate it
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslater(Text))
                
        except Exception as e:
            pass
    
# Main execution block
if __name__ == "__main__":
    while True:
        print("Say something...")
        # Continously perform speech recognition and print results
        Text = SpeechRecognition()
        print(Text)