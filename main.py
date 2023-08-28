import pyttsx3
from datetime import datetime
import speech_recognition as sr
from random import choice
import requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad
from decouple import config

USERNAME = config('USER')
BOTNAME = config('BOTNAME')


dibas = "data/tdb.mp3"

opening_text = [
    "Ok, estou no processo.",
    "Beleza, já iniciei.",
    "Só um segundo.",
]

listening_text = [
    "Estou escutando.",
    "O que deseja?",
    "Eu!",
    ]



def speak(engine, text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()


def greet_user(engine):
    """Greets the user according to the time"""

    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(engine, f"Bom dia {USERNAME}")
    elif (hour >= 12) and (hour < 18):
        speak(engine, f"Boa tarde {USERNAME}")
    elif (hour >= 18):
        speak(engine, f"Boa noitinha {USERNAME}")

    speak(engine, f"Eu sou {BOTNAME}. Como posso te ajudar?")


def take_user_input(engine):
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Escutando....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Reconhecendo...')
        query = r.recognize_google(audio, language='pt-BR')
        if not 'sair' in query or 'pare' in query:
            speak(engine, choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak(engine, "Boa noite, cuide-se!")
            else:
                speak(engine, 'Tenha um bom dia!')
            exit()
    except Exception:
        speak(engine,
              'Desculpe, não consegui entender. Você poderia repetir?')
        query = 'None' 
    return query

def listen(engine):
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='pt-BR')
        print(query)
        if not 'sair' in query or 'pare' in query:
            pass
        else:
            hour = datetime.now().hour
            if hour >= 18 and hour < 6:
                speak(engine, "Boa noite, cuide-se!")
            else:
                speak(engine, 'Tenha um bom dia!')
            exit()
            
    except Exception:
        query = 'None' 
    return query


def main():


    esp_ip = "192.168.1.103"
    

    volume = 1.0

    engine = pyttsx3.init('sapi5')

    # Set Rate
    engine.setProperty('rate', 240)

    # Set Volume
    engine.setProperty('volume', volume)

    # Set Voice (Female)
    # The getProperty method returns a list of voices available in the system.
    voices = engine.getProperty('voices')
    '''engine.setProperty('voice', voices[1].id)'''
    for voice in voices:
        if "brazil" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    greet_user(engine)

    while True:
        query = listen(engine).lower()

        if 'faraday' in query or 'faradai' in query or 'faradei' in query:
            speak(engine, choice(listening_text))

            while True:
                
                query = take_user_input(engine).lower()
                '''f = open("stt.txt", "w")
                f.write(f'{query}')'''


                if 'abrir bloco de notas' in query:
                    open_notepad()
                    break

                elif 'abrir prompt de comando' in query or 'abrir cmd' in query:
                    open_cmd()
                    break

                # elif 'escreva' in query:
                #    if'ponto' in query:
                #      break
                #   f.write(f'{query}')

                elif 'volume' in query:
                    if 'aumentar' in query:
                        volume += 0.5
                        break
                    elif 'diminuir' in query or 'abaixar' in query:
                        volume -= 0.5
                        break
                
                elif 'se apresente' in query or 'apresente-se' in query:
                    speak(engine,
                        f'Olá, eu sou a Faraday, a assistente virtual do PET Elétrica Ufes. Caso deseje minha ajuda basta me chamar que eu atenderei. Se quiser uma lista dos possíveis comandos que eu executo, basta dizer Comandos que explicarei.')
                    break
                
                elif 'abrir camera' in query:
                    open_camera()
                    break
                
                # elif 'tamo junto' in query or 'ta de boas' in query or 'tade boas':
                #    playsound(dibas)
                #    break

                elif 'acender' in query:
                    url_on = f"http://{esp_ip}/H"
                    response_on = requests.get(url_on)
                    if response_on.status_code == 200:
                        print("LED aceso!")
                    else:
                        print("Falha ao acender o LED.")
                    break
                

                elif 'apagar' in query:
                    url_on = f"http://{esp_ip}/L"
                    response_on = requests.get(url_on)

                    if response_on.status_code == 200:
                        print("LED apagado!")
                    else:
                        print("Falha ao apagar o LED.")
                    break

                elif 'abrir calculadora' in query:
                    open_calculator()
                    break

                elif 'endereço de ip' in query:
                    ip_address = find_my_ip()
                    speak(engine,
                        f'Seu endereço de IP é: {ip_address}.\n TE EME JOTA')
                    print(f'Seu endereço de IP é: {ip_address}')
                    break

                elif 'wikipedia' in query:
                    speak(engine, 'O quê você quer pesquisar na Wikipedia?')
                    search_query = take_user_input(engine).lower()
                    results = search_on_wikipedia(search_query)
                    speak(engine, f"De acordo com a Wikipedia, {results}")
                    speak(engine, "Estou printando na tela.")
                    print(results)
                    break

                elif 'youtube' in query:
                    speak(engine, 'O quê você quer ver no YouTube?')
                    video = take_user_input(engine).lower()
                    play_on_youtube(video)
                    break

                elif 'pesquisar' in query:
                    speak(engine, 'O que vocÊ quer pesquisar no Google?')
                    query = take_user_input(engine).lower()
                    search_on_google(query)
                    break

                elif "enviar mensagem no whatsapp" in query:
                    speak(engine,
                        'Por favor, escreva o número para qual devo enviar a mensagem.')
                    number = input("Entre com o número: ")
                    speak(engine, "Qual a mensagem que deseja enviar?")
                    message = take_user_input(engine).lower()
                    send_whatsapp_message(number, message)
                    speak(engine, "Mensagem enviada.")
                    break

                elif "enviar email" in query:
                    speak(
                        engine, "Entre com o email para o qual deseja enviar.")
                    receiver_address = input("Entre ocm o endereço de email: ")
                    speak(engine, "Qual deve ser o assunto?")
                    subject = take_user_input(engine).capitalize()
                    speak(engine, "Qual é a mensagem?")
                    message = take_user_input(engine).capitalize()
                    if send_email(receiver_address, subject, message):
                        speak(engine, "Email enviado.")
                    else:
                        speak(engine,
                            "Algo deu errado enquanto enviava o email,por favor, cheque o log de erro.")
                    break

                elif 'piadoca' in query:
                    speak(engine, f"Espero que goste dessa.")
                    joke = get_random_joke()
                    speak(engine, joke)
                    speak(engine, "Estou printando na tela.")
                    break

                elif "conselho" in query:
                    speak(engine, f"Aqui vai um conselho para você.")
                    advice = get_random_advice()
                    speak(engine, advice)
                    speak(engine, "Estou printando na tela.")
                    break

                elif 'notícias' in query:
                    speak(engine, f"Estou lendo as últimas notícias.")
                    speak(engine, get_latest_news())
                    speak(engine, "Estou printando na tela.")
                    print(*get_latest_news(), sep='\n')
                    break

                elif 'tempo' in query:
                    ip_address = find_my_ip()
                    city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
                    speak(engine, f"Procurando o relatório do tempo de {city}.")
                    weather, temperature, feels_like = get_weather_report(city)
                    speak(engine,
                        f"A temperatura atual é {temperature}, com a sensação térmica de {feels_like}")
                    speak(engine, f"Também, é falado no relatório que {weather}")
                    speak(engine, "Estou printando na tela.")
                    print(
                        f"Descrição: {weather}\n Temperatura: {temperature}\n Sensação: {feels_like}")
                    break
                
                '''else:
                    speak(engine,
              'Desculpe, não consegui entender. Você poderia repetir?')'''


if __name__ == '__main__':
    main()

# variação de volume 
