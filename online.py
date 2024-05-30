import requests
from email.message import EmailMessage
import smtplib
from decouple import config


EMAIL = "SIKANDARSHAIKH1999"
PASSWORD = "4930 " #add security key not password


def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()

def send_email(reciever_add,subject,message):
    try:
        email=EmailMessage()
        email['to'] = reciever_add
        email['Subject'] = subject
        email['From']=EMAIL

        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL,PASSWORD)
        s.send_message(email)
        return  True

    except Exception as e:
        print(e)
        return False

def get_news():
    news_headline=[]
    result=requests.get(f"https://newsapi.org/v2/top-headlines?country=in&category=general&apiKey"
                        f"=f62502e34ba74696b1724e98eb7c252b").json()
    articles=result["articles"]
    for article in articles:
        news_headline.append(article["title"])
    return news_headline

def weather_forcast(city):
    res = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=7d5545cafd6b4f719e00b33fb7ca4bf4"
    ).json()
    weather  = res["weather"][0]["main"]
    temp = res ["main"]["temp"]
    feels_like=res["main"]["feels_like"]
    return weather,f"{temp}",f"{feels_like}`C"






