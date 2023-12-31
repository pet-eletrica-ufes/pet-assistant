import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config
from bs4 import BeautifulSoup
# from selenium import webdriver


USERNAME = config("USER")
BOTNAME = config("BOTNAME")
EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")
NEWS_API_KEY = config("NEWS_API_KEY")
OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")


def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]


def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results


def play_on_youtube(video):
    kit.playonyt(video)


def search_on_google(query):
    kit.search(query)


def send_email(receiver_address, subject, message): #alterar para leitura de arquivos (modelo de email, lista de pessoas, etc.)
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_latest_news():
    news_headlines = []
    res = requests.get(
        f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]


def get_weather_report(city):
    response = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric")
    
    print(response)
    
    res = response.json()
    print(res)

  
    if response.status_code == 200:
        weather = res["weather"][0]["main"]
        temperature = res["main"]["temp"]
        feels_like = res["main"]["feels_like"]
        return weather, f"{temperature}℃", f"{feels_like}℃"

    else:
        return None, f"{None}℃", f"{None}℃"


def get_random_joke(): #fazer um ambiente de commits de piadas próprias para alimentar a Faraday 
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]


def get_random_advice(): #mesma ideia da função de piadas
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']


def cardapio_RU(url, hora):

    # URL do cardápio
    url_cardapio = url
    response = requests.get(url)

    page = response.content

    soup = BeautifulSoup(page, 'html.parser')
    
    list_item = soup.find('div', class_= 'view-content')

    cardapio = list_item.text.strip()
    
    # print(cardapio)
    
    if hora < 15:
        return (cardapio[:(cardapio.find('Jantar'))])
    else:
        return (cardapio[(cardapio.find('Jantar')):])
    
    
    



'''url_cardapio = 'https://ru.ufes.br/cardapio'
cardapio_RU(url_cardapio, 14)'''



# Bom dia Faraday - revisão do clima, horário, emails não lidos e cumprimentos. Possível reconhecimento de pessoas por voz (Vik - Librosa)
# https://subscription.packtpub.com/book/data/9781787125193/9/ch09lvl1sec61/identifying-speakers-with-voice-recognition
# Faraday, se apresente - 'Olá, eu sou a Faraday, a assistente virtual do PET...'
# Interação com a sala inteligente, 'tour' pelas funcionalidades

# LED responsivo 
# Escrever em um txt as coisas que pedirem para ela. Ex "faraday anota isso" "ok estou esctando" "bla bla bla"

# Adicionar piadas
# Só acionar a leitura stt quando chamada 'Faraday'

# Comandos de acionamento serão adicionados a medida de aceesibilidade ao servidor e necessidade dos disposotivos de automatização da sala

# Integração com holograma será adaptada ao Hardware disponível (ventoinha ou box)

# Abrir sites diretos por atalhos salvos no servidor

