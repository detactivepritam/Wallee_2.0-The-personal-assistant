import speech_recognition as sr
import pyttsx3
import webbrowser

def speak(text):
    engine = pyttsx3.init()  
    engine.say(text)
    engine.runAndWait()
    

if __name__ == "__main__":
    speak("How may I help you, Pritam?")
