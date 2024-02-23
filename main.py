import pyttsx3
import speech_recognition as sr
from database import add_data
from API_functionalities import googleSearch, youtube
from system_operations import get_general_response

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 185)

def speak(text):
    print("ASSISTANT -> " + text)
    try:
        engine.say(text)
        engine.runAndWait()
    except (KeyboardInterrupt, RuntimeError):
        return

def record():
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic)
        recognizer.dynamic_energy_threshold = True
        print("Listening...")
        audio = recognizer.listen(mic)
        try:
            text = recognizer.recognize_google(audio, language='en-US').lower()
            print("USER -> " + text)
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
    return None

def chat(query):
    # Implement your chat functionality here using NLP or external APIs
    return "dummy_intent"

def main(query):
    add_data(query)
    intent = chat(query)
    done = False
    if "google" in query:
        googleSearch(query)
        done = True
    elif "youtube" in query:
        youtube(query)
        done = True
    # Add more conditions for handling different intents
    if not done:
        answer = get_general_response(query)
        if answer:
            speak(answer)
        else:
            speak("Sorry, not able to answer your query")

if __name__ == "__main__":
    try:
        while True:
            response = record()
            if response is not None:
                main(response)
    except KeyboardInterrupt:
        print("EXITED")
