import speech_recognition as sr
import pyttsx3
import webbrowser 

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

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    r = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
            
            word = r.recognize_google(audio).lower()
            print(word)
            
            
            
            if "hello" in word:
                speak("Hello! How can I assist you?")
            else:
                processCommand(word)
            
        
        except sr.UnknownValueError:
            print("Could not understand the audio. Please speak again.")
        except sr.RequestError:
            print("Network error. Check your internet connection.")
        except Exception as e:
            print(f"An error occurred: {e}")