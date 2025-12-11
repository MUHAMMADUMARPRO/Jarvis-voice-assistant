from gtts import gTTS
import speech_recognition as sr
import pygame
import os
import webbrowser
import musicLibrary
from openai import OpenAI
import requests
def speak(text):
    tts = gTTS(text)
    filename = "voice.mp3"
    tts.save(filename)
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    os.remove(filename)
def aiProcess(command):
    apikey="Your AI API Key Here"
    client = OpenAI(api_key=f"{apikey}",
    )

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content
def take_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=3)
            text = r.recognize_google(audio)
            print("You said:", text)
            return text.lower()

        except sr.WaitTimeoutError:
            print("No speech detected in time.")
            return ""

        except sr.UnknownValueError:
            return ""  # will ask again without reactivating wake word

        except sr.RequestError:
            speak("Speech service error.")
            return ""
def process_command(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        url=musicLibrary.music[song]
        webbrowser.open(url)
    elif "umar" in c.lower():
        speak("Umar Is Creating me and i am personal Assistant of umar Umar is a great man ")
    elif "news" in c.lower():
       news_api="Your News APIKEY Here"
       news_url=('https://newsapi.org/v2/everything?''q=Apple&''from=2025-12-03&''sortBy=popularity&'
      'apiKey=5e58b91a17ef41549d011f0fcfc2fd76')
       response = requests.get(news_url)
       data = response.json()
       news_text = "Here are the top 5 news headlines. "
       try:
          if data["status"] == "ok":
              articles = data["articles"]
              count = 1

          for article in articles[:5]:  # top 5 news
              title = article.get("title")
              if title:
                  news_text += f"Headline {count}: {title}. "
                  count += 1
              else:
                  news_text = "Sorry, I could not fetch the news."

        # speak the news using your speak() function
          speak(news_text)
       except Exception as e:
               print(e)
    else:
        reply = aiProcess(command)
        speak(reply)
# ---------------- MAIN PROGRAM ----------------
if __name__ == "__main__":
    speak("Jarvis initializing. Say 'Jarvis' to activate me.")

    # --------- WAIT FOR WAKE WORD ONLY ONCE ---------
    while True:
        wake = take_audio()
        if "jarvis" in wake:
            speak("Jarvis activated. How can I help you?")
            break

    # --------- CONTINUOUS COMMAND LOOP ---------
    while True:
        command = take_audio()

        if command == "":
            speak("I did not understand. Please say your command again.")
            continue

        # Exit condition
        if "close jarvis" in command or "shutdown" in command:
            speak("Shutting down. Goodbye!")
            break

        process_command(command)

