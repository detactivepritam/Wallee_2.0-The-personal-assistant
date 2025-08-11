import speech_recognition as sr
import pyttsx3
import webbrowser
import MusicLibrary
from newsapi import NewsApiClient
import pyjokes
import requests
import random
from datetime import datetime

OPENWEATHER_API_KEY = 'your api key'
NEWS_API_KEY = 'your api key'

newsapi = NewsApiClient(api_key=NEWS_API_KEY)
top_headlines = newsapi.get_top_headlines()

science_qa = {
    "physics": {
        "speed of light": "The speed of light in a vacuum is approximately 299,792 kilometers per second.",
        "who discovered gravity": "Sir Isaac Newton formulated the laws of gravity in 1687.",
        "explain newton's first law": "Newton's first law states that an object in motion stays in motion unless acted upon by an external force.",
        "explain quantum mechanics": "Quantum mechanics is the branch of physics dealing with atomic and subatomic particles.",
        "explain the theory of relativity": "Einstein's theory of relativity describes the laws of physics in non-inertial frames of reference.",
        "explain black hole": "A black hole is a region of spacetime where gravity is so strong that nothing can escape.", 
    },
    "chemistry": {
        "what is an acid": "An acid is a substance that donates protons or accepts electrons in reactions.",
        "what is a chemical bond": "A chemical bond is the attraction between atoms that forms chemical substances.",
        "what is organic chemistry": "Organic chemistry studies carbon-containing compounds and their reactions.",
        "what is the ph scale": "The pH scale measures how acidic or basic a substance is from 0 to 14.",
        "what is a catalyst": "A catalyst is a substance that increases reaction rate without being consumed.",
    },
    "general": {
        "what is dna": "DNA is the molecule carrying genetic instructions for all living organisms.",
        "what is the big bang theory": "The Big Bang theory explains the expansion of the universe from a hot, dense state.",
        "what is artificial intelligence": "AI is the simulation of human intelligence processes by machines.",
    }
}
conversation_responses = {
    "what time is it": [f"The current time is {datetime.now().strftime('%H:%M')}"],
    "what day is it": [f"Today is {datetime.now().strftime('%A, %B %d')}"],
    "who made you": ["I was created by an ambitious developer to assist you!"],
    "thank you": ["You're welcome!", "My pleasure!", "Happy to help!"],
    "good morning": ["Good morning! Ready to tackle the day?"],
    "good night": ["Good night! Sleep well!"],
    "how r you": ["I'm functioning optimally, thank you!", "Just calculating the universe's mysteries, and you?"],
    "your name": ["I'm wallee, your virtual assistant.", "They call me Jarvis. How can I help?"],
}

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={OPENWEATHER_API_KEY}&q={city}&units=metric"
    
    try:
        response = requests.get(complete_url)
        data = response.json()
        
        if data.get("cod") != 404:
            main = data["main"]
            temperature = main["temp"]
            humidity = main["humidity"]
            weather_desc = data["weather"][0]["description"]
            
            weather_report = (f"The temperature in {city} is {temperature:.1f}°C with {weather_desc}. "
                             f"The humidity is {humidity}%.")
            return weather_report
        else:
            return "City not found. Please try again."
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return "Sorry, I couldn't fetch the weather information."

def handle_conversation(query):
    query = query.lower().strip()
  
    for category in science_qa:
        if query in science_qa[category]:
            return science_qa[category][query]
    
    for category in science_qa:
        for question in science_qa[category]:
            if question in query:
                return science_qa[category][question]
    
    for phrase in conversation_responses:
        if phrase in query:
            return random.choice(conversation_responses[phrase])
    
    return None

def processCommand(command):
    command = command.lower().strip()
    
    conversation_response = handle_conversation(command)
    if conversation_response:
        speak(conversation_response)
        return
    
    # Then process commands
    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
    elif command.startswith("play"):
        song = command.replace("play", "").strip()
        match = next((key for key in MusicLibrary.songs if key.lower() == song), None)
    
        if match:
            link = MusicLibrary.songs[match]
            webbrowser.open(link)
            speak(f"Playing {match}")
        else:
            speak("Sorry, I couldn't find that song in the library.")
    elif "news" in command:
        if 'articles' in top_headlines and top_headlines['articles']:
            speak("Here are the top news headlines:")
            for article in top_headlines['articles'][:5]:
                speak(article['title'])
    elif "joke" in command or "make me laugh" in command:
        joke = pyjokes.get_joke()
        print(joke)
        speak(joke)
    elif "weather" in command:
        speak("Which city's weather would you like to know?")
        try:
            with sr.Microphone() as source:
                print("Listening for city name...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                city = recognizer.recognize_google(audio)
                print(f"Getting weather for: {city}")
                weather_info = get_weather(city)
                speak(weather_info)
        except Exception as e:
            print(f"Error getting city: {e}")
            speak("Sorry, I didn't catch that. Please try again.")
    else:
        speak("I don't understand that command. Can you please repeat?")

if __name__ == "__main__":
    speak("Initializing wallee...")
    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            word = recognizer.recognize_google(audio).lower()
            print(word)
            
            if "hello" in word:
                speak(random.choice(["Hello! How can I assist you?", "Hi there! What can I do for you?"]))
            elif "thanks" in word or "thank" in word:
                speak(random.choice(["You're welcome!", "My pleasure!", "Happy to help!"]))
            elif "bye" in word or "goodbye" in word:
                speak("Goodbye! Have a great day!")
                break
            else:
                processCommand(word)
                
        except sr.UnknownValueError:
            print("Could not understand the audio. Please speak again.")
        except sr.RequestError:
            print("Network error. Check your internet connection.")
        except Exception as e:
            print(f"An error occurred: {e}")
