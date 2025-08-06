import pyttsx4
import speech_recognition as sr
import datetime
import webbrowser
import wikipedia
import os
import pyautogui
import pywhatkit
import pyjokes
import json
import psutil
import subprocess
from googletrans import Translator
import audioop
import pyaudio
import time

STATUS_FILE = "jarvis_status.json"
WAKE_WORD = "jarvis"

engine = pyttsx4.init()
engine.setProperty('rate', 180)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def update_status(status=None, amplitude=None):
    data = {
        "status": status if status else "Waiting...",
        "time": time.strftime("%H:%M:%S"),
        "amplitude": amplitude if amplitude else 0
    }
    with open(STATUS_FILE, "w") as f:
        json.dump(data, f)

def execute_command(query):
    update_status(f"Executing: {query}")
    if "time" in query:
        speak(datetime.datetime.now().strftime("%H:%M:%S"))
    elif "date" in query:
        speak(datetime.datetime.now().strftime("%Y-%m-%d"))
    elif "open notepad" in query:
        os.startfile("notepad.exe")
    elif "open chrome" in query:
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        speak(wikipedia.summary(query, sentences=2))
    elif "play" in query:
        song = query.replace("play", "")
        pywhatkit.playonyt(song)
        speak(f"Playing {song} on YouTube.")
    elif "joke" in query:
        speak(pyjokes.get_joke())
    elif "screenshot" in query:
        pyautogui.screenshot("screenshot.png")
        speak("Screenshot saved.")
    elif "shutdown" in query:
        os.system("shutdown /s /t 5")
    elif "restart" in query:
        os.system("shutdown /r /t 5")
    elif "sleep" in query:
        subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
    elif "volume up" in query:
        pyautogui.press("volumeup")
    elif "volume down" in query:
        pyautogui.press("volumedown")
    elif "mute" in query:
        pyautogui.press("volumemute")
    elif "translate" in query:
        speak("What should I translate?")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
        text = r.recognize_google(audio, language='en-in')
        translator = Translator()
        translation = translator.translate(text, dest='hi')
        speak(f"In Hindi: {translation.text}")
    else:
        speak("I am not programmed for that yet.")
    update_status("Listening for wake word...")

def start_backend():
    speak("Jarvis v4 online. Waiting for wake word...")
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    while True:
        data = stream.read(1024, exception_on_overflow=False)
        rms = audioop.rms(data, 2)
        update_status(amplitude=rms)

        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = r.listen(source, phrase_time_limit=2)
                if WAKE_WORD in r.recognize_google(audio, language='en-in').lower():
                    speak("Yes?")
                    update_status("Wake word detected. Listening for command...")
                    audio_cmd = r.listen(source, phrase_time_limit=5)
                    try:
                        query = r.recognize_google(audio_cmd, language='en-in').lower()
                        execute_command(query)
                    except:
                        update_status("Could not understand command")
            except:
                pass

if __name__ == "__main__":
    start_backend()
