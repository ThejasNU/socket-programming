import socket
import os
from _thread import *
import requests,json
import math
from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv

load_dotenv()
cg=CoinGeckoAPI()
ServerSideSocket = socket.socket()

host = ''
port = 2004
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(5)

def mad_libs(word):
    word_list=word.split(" ")
    madlib="After hiding the painting in his __ for two years, he grew __ and tried to sell it to a/an __ in Florence, but was caught."
    for i in range(len(word_list)):
        madlib=madlib.replace("__",word_list[i],1)
    return madlib

def crypto(coins_string):
    coins=coins_string.split(" ")
    output_string=""
    response=cg.get_price(ids=coins,vs_currencies=["usd","inr"])
    cryptos=list(response.keys())
    length=len(cryptos)
    for i in range(length):
        coin=cryptos[i]
        price_usd=response[cryptos[i]]['usd']
        price_inr=response[cryptos[i]]['inr']
        output_string=output_string+f"{coin} : ${price_usd} or ₹{price_inr}\n"
    return f"Current prices of the entered crypto currency/currencies:\n{output_string}"

def get_weather(city):
    API_KEY=os.getenv("API_KEY")
    response=requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}")
    if(response.status_code==200):
        data=response.json()
        main=data['main']
        temperature=main['temp']
        humidity=main['humidity']
        pressure=main['pressure']
        report=data['weather']
        wind=data["wind"]
        windspeed=wind['speed']
        return f"{city:-^30}"+"\n"+f"Temperature: {math.floor(temperature)-273}°C"+"\n"+f"Humidity: {humidity}"+"\n"+f"Pressure: {pressure}"+"\n"+f"Wind Speed: {windspeed}"+"\n"+f"Weather Report: {report[0]['description']}"
    else:
        return "Couldn't get data check the name of city entered"


def multi_threaded_client(connection):
    
    sentence = connection.recv(1024).decode()
    filled_sentence = mad_libs(sentence)
    connection.send(filled_sentence.encode())

    coins_string=connection.recv(1024).decode()
    coins_price=crypto(coins_string)
    connection.send(coins_price.encode())

    city=connection.recv(1024).decode()
    weather=get_weather(city)
    connection.send(weather.encode())

    connection.close()

while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()
