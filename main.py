import pyttsx3
from datetime import datetime
import speech_recognition as sr
from random import choice
import requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad
from pprint import pprint
from decouple import config

USERNAME = config('USER')
BOTNAME = config('BOTNAME')


opening_text = [
    "Cool, I'm on it sir.",
    "Okay sir, I'm working on it.",
    "Just a second sir.",
]


def speak(engine, text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()


def greet_user(engine):
    """Greets the user according to the time"""

    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(engine, f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(engine, f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(engine, f"Good Evening {USERNAME}")

    speak(engine, f"I am {BOTNAME}. How may I assist you?")


def take_user_input(engine):
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        if not 'exit' in query or 'stop' in query:
            speak(engine, choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak(engine, "Good night sir, take care!")
            else:
                speak(engine, 'Have a good day sir!')
            exit()
    except Exception:
        speak(engine,
              'Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query


def main():
    engine = pyttsx3.init('sapi5')

    # Set Rate
    engine.setProperty('rate', 190)

    # Set Volume
    engine.setProperty('volume', 1.0)

    # Set Voice (Female)
    # The getProperty method returns a list of voices available in the system.
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    greet_user(engine)

    while True:
        query = take_user_input(engine).lower()

        if 'open notepad' in query:
            open_notepad()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(engine,
                  f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            speak(engine, 'What do you want to search on Wikipedia, sir?')
            search_query = take_user_input(engine).lower()
            results = search_on_wikipedia(search_query)
            speak(engine, f"According to Wikipedia, {results}")
            speak(engine, "For your convenience, I am printing it on the screen sir.")
            print(results)

        elif 'youtube' in query:
            speak(engine, 'What do you want to play on Youtube, sir?')
            video = take_user_input(engine).lower()
            play_on_youtube(video)

        elif 'search on google' in query:
            speak(engine, 'What do you want to search on Google, sir?')
            query = take_user_input(engine).lower()
            search_on_google(query)

        elif "send whatsapp message" in query:
            speak(engine,
                  'On what number should I send the message sir? Please enter in the console: ')
            number = input("Enter the number: ")
            speak(engine, "What is the message sir?")
            message = take_user_input(engine).lower()
            send_whatsapp_message(number, message)
            speak(engine, "I've sent the message sir.")

        elif "send an email" in query:
            speak(
                engine, "On what email address do I send sir? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak(engine, "What should be the subject sir?")
            subject = take_user_input(engine).capitalize()
            speak(engine, "What is the message sir?")
            message = take_user_input(engine).capitalize()
            if send_email(receiver_address, subject, message):
                speak(engine, "I've sent the email sir.")
            else:
                speak(engine,
                      "Something went wrong while I was sending the mail. Please check the error logs sir.")

        elif 'joke' in query:
            speak(engine, f"Hope you like this one sir")
            joke = get_random_joke()
            speak(engine, joke)
            speak(engine, "For your convenience, I am printing it on the screen sir.")
            pprint(joke)

        elif "advice" in query:
            speak(engine, f"Here's an advice for you, sir")
            advice = get_random_advice()
            speak(engine, advice)
            speak(engine, "For your convenience, I am printing it on the screen sir.")
            pprint(advice)

        elif 'news' in query:
            speak(engine, f"I'm reading out the latest news headlines, sir")
            speak(engine, get_latest_news())
            speak(engine, "For your convenience, I am printing it on the screen sir.")
            print(*get_latest_news(), sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(engine, f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(engine,
                  f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(engine, f"Also, the weather report talks about {weather}")
            speak(engine, "For your convenience, I am printing it on the screen sir.")
            print(
                f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")


if __name__ == '__main__':
    main()
