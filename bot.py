#!/usr/bin/env python3

import requests, json, logging
import numpy as np
from collections import OrderedDict

import telebot
import configparser

config = configparser.ConfigParser()
config.read('config.ini')


logger = logging.getLogger()
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler() # messages show up in terminal
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s') # format the message for the terminal output

stream_handler.setFormatter(formatter) # add formatter to the stream handler
stream_handler.setLevel(logging.INFO)

logger.addHandler(stream_handler)

# Keys
key_telegram_bot = config['DEFAULT']['SECRET_KEY_T']
key_weather_api = config['DEFAULT']['SECRET_KEY_W']

# Initiate bot
bot = telebot.TeleBot(key_telegram_bot, parse_mode=None)

class Weather:
  def __init__(self):
    self.__base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    self.__api_key = key_weather_api

    self.parameters = OrderedDict()

    logger.info('Weather class was initiated.')

  def __make_request(self, method: str):
    if method == 'GET':
      try:
        response = requests.get(self.__base_url, params=self.parameters)
        #print(response.url)
      except Exception as e:
        logger.error(f"Connection error while making {method} request to {self.parameters} with {e}.")
        return None

    elif method == 'POST':
      raise ValueError

    else:
      raise ValueError

    if response.status_code == 200:
      return response.json()
    else:
      raise logger.error(f"{method} request was not successful. Status code {response.status_code}")

  def current(self, city: str):
    self.parameters['q']= city
    self.parameters['appid'] = self.__api_key # always last in HTTP request
    #print(self.parameters)

    response = dict(self.__make_request('GET'))
    logger.info('Current weather was requested.')

    city_name = response['name']
    kelvin = response['main']['temp']
    celsius = np.round(kelvin - 273.15, 3)
    leiras = response['weather'][0]['description']

    return city_name, celsius, leiras


# TELEGRAM BOT
@bot.message_handler(commands=['weather'])
def covid_data(message):
  w = Weather()
  city, celsius, leiras = w.current('Debrecen')

  bot.send_message(message.chat.id, f"Weather in {city} is {celsius} celsius and {leiras}.")


bot.polling()



