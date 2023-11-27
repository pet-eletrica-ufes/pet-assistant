'''

import pyttsx3
from datetime import datetime
import speech_recognition as sr
from random import choice
import requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, cardapio_RU
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad
from decouple import config
import serial

class Assistant:
    def __init__(self):
        self.USERNAME = config('USER')
        self.BOTNAME = config('BOTNAME')
        self.RURL = config('RURL')
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty('rate', 210)
        self.engine.setProperty('volume', 1.5)
        self.voices = self.engine.getProperty('voices')
        self.set_voice()

        self.oracle = serial.Serial('COMX', 9600)

    def set_voice(self):
        for voice in self.voices:
            if "brazil" in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break

    def speak(self, text):
        """Used to speak whatever text is passed to it"""
        self.engine.say(text)
        self.engine.runAndWait()

    def greet_user(self):
        """Greets the user according to the time"""
        hour = datetime.now().hour
        if 6 <= hour < 12:
            self.speak(f"Bom dia {self.USERNAME}")
        elif 12 <= hour < 18:
            self.speak(f"Boa tarde {self.USERNAME}")
        elif hour >= 18:
            self.speak(f"Boa noitinha {self.USERNAME}")

        self.speak(f"Eu sou {self.BOTNAME}. Como posso te ajudar?")

    def take_user_input(self):
        """Takes user input, recognizes it using Speech Recognition module and converts it into text"""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Escutando....')
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print('Reconhecendo...')
            query = r.recognize_google(audio, language='pt-BR')
            if 'sair' not in query or 'pare' in query:
                self.speak(choice(opening_text))
                self.set_oracle(2)
            else:
                query = 'None'
        except Exception:
            query = 'None'
        return query

    def set_oracle(self, state):
        self.oracle.write(str(state).encode() + b'\n')

    def listen(self):
        """Takes user input, recognizes it using Speech Recognition module and converts it into text"""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            query = r.recognize_google(audio, language='pt-BR')
            print(query)
            if 'sair' not in query or 'pare' in query:
                pass
            else:
                print("Saindo...")
                exit()

        except Exception:
            query = 'None'
        return query

    def main():
        Faraday = Assistant()
        Faraday.greet_user()

        while True:
            query = Faraday.listen().lower()
            self.set_oracle(0)

            if 'faraday' in query or 'faradai' in query or 'faradei' in query:
                Faraday.speak(choice(listening_text))
                while True:
                    self.set_oracle(1)
                    query = Faraday.take_user_input().lower()
                    
                    # Resto do seu código...






'''