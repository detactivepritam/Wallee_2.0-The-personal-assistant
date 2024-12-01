import speech_recognition as sr
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak("Initializing Jarvis...")
    r = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
            
            word = r.recognize_google(audio).lower()
            print(word)
            
            # Respond to recognized words
            if "hello" in word:
                speak("Hello! How can I assist you?")
            
        
        except sr.UnknownValueError:
            print("Could not understand the audio. Please speak again.")
        except sr.RequestError:
            print("Network error. Check your internet connection.")
        except Exception as e:
            print(f"An error occurred: {e}")