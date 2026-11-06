import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openrouter import OpenRouter
from gtts import gTTS
import pygame
import os

# pip install pocketsphinx

recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5

newsapi = "16720680bace4571941c9313b3973006"
client = OpenRouter(api_key="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")

def speak_old(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    completion = client.chat.send(
        model="gemini-3.6-flash",
        messages=[
            {"role": "system", "content": "You are JARVIS, a concise and intelligent virtual assistant."},
            {"role": "system", "content": "Answer naturally and directly. "},
            {"role": "system", "content": "Your responses are spoken aloud, so avoid markdown, lists, "},
            {"role": "system", "content": "long explanations, emojis, and unnecessary words. "},
            {"role": "system", "content": "Keep responses under 30 words whenever possible."},
            {"role": "user", "content": command}
        ],
        max_completion_tokens=9971
    )
    return completion.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        speak("Opening Google.")
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        speak("Opening Facebook.")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        speak("Opening LinkedIn.")
        webbrowser.open("https://linkedin.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get('articles', [])

            # Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    with sr.Microphone() as source:
        print("Calibrating microphone...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Microphone ready.")
    speak("Initializing Jarvis....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
        


        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
            word = r.recognize_google(audio)
            if (word.lower() == "jarvis"):
                speak("Yes")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source, timeout=5, phrase_time_limit=8)
                    command = r.recognize_google(audio) 

                    processCommand(command)

        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            print("Couldn't understand.")
        except sr.RequestError as e:
            print("Speech recognition service error:", e)
        except Exception as e:
            print("Unexpected error:", e)
