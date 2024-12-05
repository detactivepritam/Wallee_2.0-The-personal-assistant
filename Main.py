import speech_recognition as sr
import pyttsx3
import webbrowser
import MusicLibrary
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='1ee22953d011402789e2be6f95d819ff')
top_headlines = newsapi.get_top_headlines()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def processCommand(command):
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command.lower():
        webbrowser.open("https://linkedin.com")
    elif command.lower().startswith("play"):

        song = command.lower().replace("play", "").strip()
        
        match = next((key for key in MusicLibrary.songs if key.lower() == song), None)
    
        if match:
            link = MusicLibrary.songs[match]
            webbrowser.open(link)
            speak(f"Playing {match}")
        else:
            speak("Sorry, I couldn't find that song in the library.")
    elif "news" in command.lower():
        if 'articles' in top_headlines and top_headlines['articles']:
            speak("Here are the top news headlines:")
            for article in top_headlines['articles'][:5]:
                speak(article['title'])

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            word = recognizer.recognize_google(audio).lower()
            print(word)
            
            if "hello" in word or "jarvis" in word or "hellojarvis" in word:
                speak("Hello! How can I assist you?")
            elif "thanks" in word :
                speak("You're welcome!")
            else:
                processCommand(word)
                
        except sr.UnknownValueError:
            print("Could not understand the audio. Please speak again.")
        except sr.RequestError:
            print("Network error. Check your internet connection.")
        except Exception as e:
            print(f"An error occurred: {e}")