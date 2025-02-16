# Limmy Version 0.1 : AI Assistant

## Overview
This AI Assistant is a powerful virtual assistant built using Python that can process user queries and respond intelligently. It utilizes **Selenium WebDriver** for text-to-speech (TTS) and speech-to-text (STT) conversions. The assistant is designed to categorize user queries into three types:

1. **General Queries** - General knowledge or fact-based questions.
2. **System Queries** - Commands related to system operations (e.g., opening applications, system information, etc.).
3. **Realtime Queries** - Queries requiring real-time data retrieval from the internet.

To enhance its capabilities, the assistant integrates **Groq** and **Cohere** for natural language processing (NLP) and generative AI responses. **Multithreading** is used to optimize performance, ensuring faster response times and seamless execution of concurrent tasks.

---

## Features
- **Speech-to-Text (STT) & Text-to-Speech (TTS)** via **Selenium WebDriver**.
- **Categorized Query Processing**:
  - General Queries: Fact-based answers.
  - System Queries: Perform system-level operations.
  - Realtime Queries: Fetch live data from the web.
- **Groq & Cohere Integration** for enhanced NLP and AI-driven responses.
- **Multithreading Implementation** for improved speed and responsiveness.
- **Error Handling & Logging** to ensure stability.
- **Customizable Responses** to improve user interaction.

---

## Tech Stack
- **Python** (Core programming language)
- **Selenium WebDriver** (For STT & TTS processing)
- **Groq API** (For AI-based responses)
- **Cohere API** (For text generation and NLP capabilities)
- **Multithreading** (For faster execution)
- **SpeechRecognition & pyttsx3** (For additional speech processing support)
-  **PyQt5** (For making GUI Desktop Application)

---

## Installation
### Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### Step 1: Clone the Repository
```bash
https://github.com/rudranarayan-01/LIMMY-0.1
cd LIMMY-0.1
```

### Step 2: Install Dependencies
```bash
pip install -r Requirements.txt
```

### Step 3: Set Up WebDriver
Download and set up **Selenium WebDriver** for your browser.

### Step 4: Configure API Keys
Create a **.env** file and add your API keys:
```env
GROQ_API_KEY=your_groq_api_key
COHERE_API_KEY=your_cohere_api_key
ASSISTANT_NAME = your_assistant_name
Username  = username
```

---

## Usage
### Running the Assistant
```bash
python Main.py
```

### Interacting with the Assistant
- Speak or type your query.
- The assistant will identify the **category** of the query.
- It will **process the request** accordingly using Groq, Cohere, or system operations.
- The response will be spoken back using **TTS**.

Example commands:
- **General Query**: "Who is the president of the USA?"
- **System Query**: "Open Notepad"
- **Realtime Query**: "What is the weather in New York?"

---

## Code Structure
```
├── Backend/
│   ├── Data/
      ├── ChatLog.json
      ├── Voice.html
│   ├── Automation.py      
│   ├── Chatbot.py 
│   ├── ImageGeneration.py
│   ├── Model.py 
│   ├── TTS.py         
│   ├── SpeechToText.py
|   |── RealTimeSearchEngine.py      
├── Frontend/
    ├── Files
      ├── Database.data
      ├── Responses.data
      ├── Min.data
      ├── Status.data
      ├── ImageGeneration.data
    ├── Graphics
      images...
    GUI.py
|── GeneratedImages/


```

---

## Performance Optimization with Multithreading
To ensure faster response times, **Python's threading module** is used. This allows:
- **Simultaneous execution** of speech recognition and query processing.
- **Background processing** of text-to-speech while fetching real-time data.


## Future Enhancements
- **Integration with OpenAI GPT** for more advanced AI responses.
- **Voice Activation** (e.g., "Hey Assistant!")
- **Better Error Handling & Logging Mechanism**

---

## Contributors
- **Name** - Rudranarayan Sahu
- **Website** - https://akash0101.pythonanywhere.com/

---

## License
This project is licensed under the **MIT License**.

Feel free to connect ✨✨

---

## Contact
For any queries or contributions, contact **rudranarayansahu.tech@gmail.com** or visit **[GitHub](https://github.com/rudranarayan-01)**.

