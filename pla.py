from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


from yt_dlp import YoutubeDL
import os, sys, time, shutil

# Open AI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key = OPENAI_API_KEY)

class chatBot:
    def __init__(self,system_role = {"role": "system", "content": "You are Jarvis, my personal assistant. please answer question in professional way"} , max_length=30):
        self.history = [system_role]
        self.max_length = max_length  # Maximum allowed length of the history
    def inference(self, user_input):        
        # Add user input to history
        self.history.append({"role": "user", "content": user_input})
        # Generate completion
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.history
        )
        # Extract and save the assistant's response
        assistant_reply = completion.choices[0].message.content
        self.history.append({"role": "assistant", "content": assistant_reply})
        self.history = self.history[-10:]  # Keep only the last 10 messages
        return assistant_reply
    def get_history(self):
        return self.history


Router_bot = chatBot(system_role = {
    "role": "system", 
    "content": '''Classify the request as ONE of the following classes based on the context. DO NOT say anthing else:
    - "NORMAL CHAT" : for normal chat request 
    - "OPERATOR" : for request relating to operations like open garage close garage
    - "YOUTUBER" : for requests relating to you tube'''})


print(Router_bot.inference('convert this youtube url to audio'))