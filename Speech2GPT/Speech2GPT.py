"""This module is the guts of the Sppech2GPT project."""
# Speech2GPT/Speech2GPT.py

import speech_recognition as sr
import pyttsx3
import pyaudio
from dotenv import load_dotenv
import os
import openai

from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from Speech2GPT.database import DatabaseHandler, DB_READ_ERROR

r = sr.Recognizer()

# Load environment variables from .env folder (not supplied)
load_dotenv()

class CurrentSession(NamedTuple):
    """This class holds data for the current session of the Speech2GPT project."""
    session_notes: Dict[str, Any]
    error: int

class Speech2GPT:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, prompt: List[str], response: List[str]) -> CurrentSession:
        """Add a new to-do to the database."""
        prompt_text = " ".join(prompt)
        response_text = " ".join(response)
        if not prompt_text.endswith("."):
            prompt_text += "."
        if not response_text.endswith("."):
            response_text += "."
        s2gpt = {
            "Prompt": prompt_text,
            "Response": response_text,
        }
        read = self._db_handler.read_s2gpt()
        if read.error == DB_READ_ERROR:
            return CurrentSession(s2gpt, read.error)
        read.s2gpt_list.append(s2gpt)
        write = self._db_handler.write_s2gpt(read.s2gpt_list)
        return CurrentSession(s2gpt, write.error)

    def get_s2gpt_list(self) -> List[Dict[str, Any]]:
        """Return the current to-do list."""
        read = self._db_handler.read_s2gpt()
        return read.s2gpt_list

def SpeakText(command):

    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

    try:
        with sr.Microphone() as source2:

            r.adjust_for_ambient_noise(source2, duration=0.2)
 
            audio2 = r.listen(source2)

            MyText = r.recognize_google(audio2)                         
            print(f"Did you say {MyText}?")
                
            audio3 = r.listen(source2)
            MyAnswer = r.recognize_google(audio3)
            if MyAnswer == "yes":
                listenBool = False
                # SpeakText(MyText)
                wisdomFromOnHigh= passToOpenAI(MyText)
                print(f"\n{wisdomFromOnHigh}")
                engine.say(wisdomFromOnHigh)
            else:
                SpeakText("Please repeat.")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))                     
    except sr.UnknownValueError:                          
        print("unknown error occured")

def passToOpenAI(command):
    maxT = 4097
    print("Passing to OpenAI: "+command)

    # Get API key from environment variables, or put your own key here
    openai.api_key = os.environ["GPT_API"]
    usrPrompt = command

    remainderT = maxT-len(usrPrompt)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=usrPrompt,
        temperature=0.5,
        max_tokens=remainderT,
        top_p=1.0,
        frequency_penalty=0.52,
        presence_penalty=0.5
        )
 
    return response["choices"][0]["text"]

if __name__ == "__main__":
    SpeakText("Hello, how may I help you?")