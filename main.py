import os
import speech_recognition as sr
from groq import Groq
from dotenv import load_dotenv
import edge_tts
import pygame
import pyttsx3

load_dotenv()
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Checking the outside noise...Just wait a second")
    r.adjust_for_ambient_noise(source, duration=1)

    print("Yea, you can talk now")
    r.pause_threshold = 1
    audio = r.listen(source)

try:
    text = r.recognize_google(audio, language="en-US")
    print(f"U said: {text}")

except sr.UnknownValueError:
    print("I could not understand what you just said, try louder")
except sr.RequestError as e:
    print(f"Error to connect to the google service available; {e}")



client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": text
        }
    ],
    model="openai/gpt-oss-20b",

)

print(chat_completion.choices[0].message.content)
