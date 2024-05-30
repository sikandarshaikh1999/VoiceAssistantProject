import datetime
import os
import subprocess as sp
import webbrowser
from random import choice
import imdb
import keyboard
import speech_recognition as sr
import win32com.client
from decouple import config

from con import random_text
from online import find_my_ip, send_email, get_news, weather_forcast

speaker = win32com.client.Dispatch("SAPI.SpVoice")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said:{query}")
            if 'stop' in query.lower() or 'exit' in query.lower():
                hour = datetime.now().hour
                if 21 <= hour < 6:
                    speaker.speak("Good night sir, Take care")
                else:
                    speaker.speak("Have a good day sir!")
                exit()
            else:
                speaker.speak(choice(random_text))


        except Exception as e:
            speaker.Speak(" Sorry Say that again please")
            return "Some Error Occured sorry from Desktop Assitant"
        return query


USER = config('USER')
HOSTNAME = ('Sikandar')

listening = False


def start_listening():
    global listening
    listening = True
    print("Started Listening...")


def pause_listening():
    global listening
    listening = False
    print("Stopped  Listening...")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


def wish():
    hour = int(datetime.datetime.now().hour)

    if hour > 0 and hour <= 12:
        speaker.Speak("Good Morning")
    elif hour > 12 and hour < 18:
        speaker.Speak("Good Afternoon")
    else:
        speaker.Speak("Good Evening")
    s = (f"Hello {HOSTNAME} I am your Desktop Assistant How may I help you?")
    speaker.Speak(s)
    print("Press ctr+alt+k to start")
    print("Press ctr+alt+p to pause")


if __name__ == '__main__':
    wish()

    while True:
        if listening:
            print("Listneing...")
            query = takeCommand().lower()
            sites = [["youtube", "https://youtube.com"],
                     ["wikipedia", "https://wikipedia.com"],
                     ["google", "https://google.com"]]

            for site in sites:
                if f"open {site[0]}".lower() in query:
                    try:
                        webbrowser.open(site[1])
                        speaker.Speak(f"Opening {site[0]} Sir")
                    except Exception as e:
                        print(f"Error opening {site[0]}")
            if "open music" in query:

                musicPath = r"d:\Home theater\english\01 - Baby (Baby On Bed Mix) [www.DJMaza.Com].mp3"

                try:
                    os.startfile(musicPath)
                except Exception as e:
                    print("Error opening music file:", e)

            if "the time" in query:
                strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                speaker.Speak(f"Sir the time is {strfTime}")
            elif "open command prompt" in query:
                speaker.speak("Opening command prompt     sir")
                os.system('start cmd')
            elif "open camera" in query.lower():
                speaker.speak("Opening camera sir")
                sp.run('powershell -Command "Start-Process microsoft.windows.camera:"', shell=True)
            elif "ip address" in query.lower():
                ip_address = find_my_ip()
                speaker.Speak(f"Your IP Adress is {ip_address}")
                print(print(f"Your Ip adress is {ip_address}"))
            elif "send email" in query.lower():
                speaker.Speak("To which emai you want to send sir?")
                receiver_add = input("Email address:")
                speaker.Speak("What should be the subject sir?")
                subject = takeCommand().capitalize()
                speaker.Speak("What is the message sir?")
                message = takeCommand().capitalize()
                if send_email(receiver_add, subject, message):
                    speaker.Speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speaker.Speak("Something went wrong please check the log")
            elif "news" in query.lower():
                speaker.Speak("I am reading the latest headline of today")
                news_headlines = get_news()
                news_text = '\n'.join(news_headlines)
                speaker.speak(news_text)
                speaker.Speak("Printing it on screen")
                print(*get_news(), sep='/n')

            elif "movie" in query:
                movies_db = imdb.IMDb()
                speaker.Speak("Please tell me the movie name")
                text = takeCommand()
                movies = movies_db.search_movie(text)
                speaker.Speak("Searching for " + text)
                if movies:
                    movie = movies[0]
                    title = movie.get("title", "Unknown Title")
                    year = movie.get("year", "Unknown Year")
                    speaker.Speak(f"{title} - {year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    rating = movie_info.get("rating", "Rating not available")
                    cast = movie_info.get("cast", ["Cast not available"])
                    actor = cast[:5] 
                    plot = movie_info.get("plot outline", "Plot summary not available")
                    speaker.Speak(f"{title} was released in {year}. It has an IMDb rating of {rating}. "
                                  f"The cast includes: {actor}. The plot summary is: {plot}")
                    print(f"{title} was released in {year}. It has an IMDb rating of {rating}. "
                          f"The cast includes: {actor}. The plot summary is: {plot}")
                else:
                    speaker.Speak("Sorry, I couldn't find any information for that movie.")

            apps = [["notepad", r"C:\Windows\notepad.exe"]]
            for app in apps:
                if f"open{app[0]}".lower() in query.lower():
                    os.startfile(app[1])
                    speaker.Speak(f"Opening {app[0]} sir")
